import json
import random
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone

from .models import Language, Snippet, Attempt, UserProfile


def index(request):
    """Home page: language + difficulty picker."""
    languages = Language.objects.all()
    difficulty_choices = Snippet.DIFFICULTY_CHOICES

    # Check if this authenticated user has personal snippets imported from their repos
    has_my_snippets = False
    if request.user.is_authenticated:
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        if profile.get_repo_list():
            has_my_snippets = Snippet.objects.filter(imported_by=request.user).exists()

    return render(request, 'trainer/index.html', {
        'languages': languages,
        'difficulty_choices': difficulty_choices,
        'has_my_snippets': has_my_snippets,
    })


def exercise(request, snippet_id):
    """Typing exercise page."""
    snippet = get_object_or_404(Snippet, pk=snippet_id)
    response = render(request, 'trainer/exercise.html', {'snippet': snippet})
    # Prevent bfcache so navigating back doesn't restore frozen JS state
    response['Cache-Control'] = 'no-store'
    return response


def random_snippet(request):
    """Redirect to a random snippet based on language and difficulty filters."""
    language_slug = request.GET.get('language', '').strip()
    difficulty = request.GET.get('difficulty', '').strip()
    my_repos = request.GET.get('my_repos', '').strip()

    is_random_lang = not language_slug or language_slug.lower() == 'random'

    if my_repos and request.user.is_authenticated:
        user_snippets = Snippet.objects.filter(imported_by=request.user)
        if not user_snippets.exists():
            messages.warning(
                request,
                "You haven't imported any snippets from your repositories yet. "
                "Add your GitHub repos in Settings or uncheck 'From my repos'."
            )
            return redirect('index')

        lang_qs = user_snippets
        if not is_random_lang:
            lang_qs = user_snippets.filter(language__slug=language_slug)
            if not lang_qs.exists():
                lang_obj = Language.objects.filter(slug=language_slug).first()
                lang_name = lang_obj.name if lang_obj else language_slug.upper()
                messages.warning(
                    request,
                    f"No {lang_name} snippets found in your imported repositories. "
                    f"Import a repository containing {lang_name} in Settings, or uncheck 'From my repos'."
                )
                return redirect('index')

        # Try matching requested difficulty, or fall back to any available in user's repo
        target_qs = lang_qs
        if difficulty:
            diff_qs = lang_qs.filter(difficulty=difficulty)
            if diff_qs.exists():
                target_qs = diff_qs
            else:
                target_qs = lang_qs

        # When random language is selected, choose fairly across available languages
        if is_random_lang:
            available_langs = list(target_qs.values_list('language__slug', flat=True).distinct())
            if available_langs:
                chosen_slug = random.choice(available_langs)
                target_qs = target_qs.filter(language__slug=chosen_slug)

        snippet = random.choice(list(target_qs))
        return redirect('exercise', snippet_id=snippet.pk)

    # Standard snippets fallback
    qs = Snippet.objects.all()
    if not is_random_lang:
        qs = qs.filter(language__slug=language_slug)

    if difficulty:
        diff_qs = qs.filter(difficulty=difficulty)
        if diff_qs.exists():
            qs = diff_qs

    if not qs.exists() and not is_random_lang:
        qs = Snippet.objects.filter(language__slug=language_slug)

    if not qs.exists():
        messages.warning(request, "No snippets found for the selected criteria.")
        return redirect('index')

    if is_random_lang:
        available_langs = list(qs.values_list('language__slug', flat=True).distinct())
        if available_langs:
            chosen_slug = random.choice(available_langs)
            qs = qs.filter(language__slug=chosen_slug)

    snippet = random.choice(list(qs))
    return redirect('exercise', snippet_id=snippet.pk)


@require_POST
def save_attempt(request):
    """Save a completed attempt via JSON POST."""
    try:
        data = json.loads(request.body)
        snippet_id = data.get('snippet_id')
        snippet = get_object_or_404(Snippet, pk=snippet_id)

        wpm       = float(data.get('wpm', 0))
        cpm       = float(data.get('cpm', 0))
        accuracy  = float(data.get('accuracy', 0))
        time_secs = float(data.get('time_seconds', 0))

        # Sanity checks — reject paste/automation exploits
        if time_secs < 3:
            return JsonResponse({'status': 'error', 'message': 'Time too short — no cheating!'}, status=400)
        if wpm > 300:
            return JsonResponse({'status': 'error', 'message': 'WPM unrealistically high.'}, status=400)

        attempt = Attempt.objects.create(
            user=request.user if request.user.is_authenticated else None,
            snippet=snippet,
            wpm=wpm,
            cpm=cpm,
            accuracy=accuracy,
            time_seconds=time_secs,
            errors_json=data.get('errors_json', {}),
        )
        return JsonResponse({'status': 'ok', 'attempt_id': attempt.pk})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


def result(request, attempt_id):
    """Result page after completing an exercise."""
    attempt = get_object_or_404(Attempt, pk=attempt_id)
    # Sort errors by frequency descending
    errors = sorted(attempt.errors_json.items(), key=lambda x: x[1], reverse=True)
    return render(request, 'trainer/result.html', {
        'attempt': attempt,
        'errors': errors[:10],  # top 10 most mistyped chars
    })


@login_required
def history(request):
    """User's attempt history."""
    attempts = request.user.attempts.select_related('snippet__language').all()[:50]
    return render(request, 'trainer/history.html', {'attempts': attempts})


@login_required
def profile(request):
    """Profile page with per-language stats and WPM progress charts."""
    from collections import defaultdict

    user = request.user
    all_attempts = (
        user.attempts
        .select_related('snippet__language')
        .order_by('created_at')
    )

    # Aggregate stats per language
    lang_stats = {}
    lang_history = defaultdict(list)  # slug -> [{date, wpm}]

    for attempt in all_attempts:
        lang = attempt.snippet.language
        slug = lang.slug

        if slug not in lang_stats:
            lang_stats[slug] = {
                'language': lang,
                'count': 0,
                'best_wpm': 0,
                'total_wpm': 0,
                'total_acc': 0,
            }

        s = lang_stats[slug]
        s['count'] += 1
        s['total_wpm'] += attempt.wpm
        s['total_acc'] += attempt.accuracy
        if attempt.wpm > s['best_wpm']:
            s['best_wpm'] = attempt.wpm

        lang_history[slug].append({
            'date': attempt.created_at.strftime('%Y-%m-%d %H:%M'),
            'wpm': round(attempt.wpm, 1),
        })

    # Compute averages and sort by count descending (most used language first)
    for slug, s in lang_stats.items():
        s['avg_wpm'] = round(s['total_wpm'] / s['count'], 1)
        s['avg_acc'] = round(s['total_acc'] / s['count'], 1)
        s['best_wpm'] = round(s['best_wpm'], 1)

    lang_stats = dict(sorted(lang_stats.items(), key=lambda x: x[1]['count'], reverse=True))

    # Overall totals
    total_attempts = sum(s['count'] for s in lang_stats.values())
    overall_best_wpm = max((s['best_wpm'] for s in lang_stats.values()), default=0)
    overall_avg_wpm = (
        round(sum(s['total_wpm'] for s in lang_stats.values()) /
              max(total_attempts, 1), 1)
    )

    return render(request, 'trainer/profile.html', {
        'lang_stats': lang_stats,
        'lang_history_json': json.dumps(dict(lang_history)),
        'total_attempts': total_attempts,
        'overall_best_wpm': overall_best_wpm,
        'overall_avg_wpm': overall_avg_wpm,
    })


@login_required
def settings_view(request):
    """User settings — manage GitHub repositories for personal snippet import."""
    import os

    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        raw_repos = request.POST.get('github_repos', '').strip()
        profile.github_repos = raw_repos
        profile.save()

        repo_list = profile.get_repo_list()

        if not repo_list:
            messages.success(request, 'Settings saved. No repositories to import.')
            return redirect('settings')

        # Check for GitHub token
        token = os.environ.get('GITHUB_TOKEN', '')
        if not token:
            try:
                from decouple import config
                token = config('GITHUB_TOKEN', default='')
            except Exception:
                pass

        if not token:
            messages.warning(
                request,
                'Repositories saved, but GITHUB_TOKEN is not configured on the server — '
                'snippets cannot be imported right now.'
            )
            return redirect('settings')

        # Import snippets from the user's repos
        try:
            imported = _import_user_repos(request.user, profile, token)
            profile.last_import_at = timezone.now()
            profile.save()
            messages.success(request, f'Done! Imported {imported} new snippets from your repositories.')
        except Exception as e:
            messages.error(request, f'Import error: {e}')

        return redirect('settings')

    my_snippets_count = Snippet.objects.filter(imported_by=request.user).count()
    return render(request, 'trainer/settings.html', {
        'profile': profile,
        'my_snippets_count': my_snippets_count,
    })


def _extract_css_chunks(text: str) -> dict:
    """
    Parse CSS text into clean rule blocks and group them into easy, medium, and hard chunks.
    """
    lines = text.splitlines()
    rules = []
    current = []
    depth = 0
    for line in lines:
        stripped = line.strip()
        if depth == 0 and (not stripped or (stripped.startswith('/*') and stripped.endswith('*/'))):
            continue
        current.append(line)
        depth += line.count('{') - line.count('}')
        if depth <= 0 and current:
            rule_text = '\n'.join(current).strip()
            if rule_text and '{' in rule_text and '}' in rule_text:
                rules.append(rule_text)
            current = []
            depth = 0

    chunks = {'easy': [], 'medium': [], 'hard': []}

    # 1. Easy: single rules with 4..10 lines
    for r in rules:
        n = len(r.splitlines())
        if 4 <= n <= 10:
            chunks['easy'].append(r)

    # 2. Medium: single rules with 11..20 lines, or pairs of short rules with 11..20 lines
    i = 0
    while i < len(rules):
        r1 = rules[i]
        n1 = len(r1.splitlines())
        if 11 <= n1 <= 20:
            chunks['medium'].append(r1)
            i += 1
        elif i + 1 < len(rules):
            combo = r1 + '\n\n' + rules[i + 1]
            n_combo = len(combo.splitlines())
            if 11 <= n_combo <= 20:
                chunks['medium'].append(combo)
                i += 2
            else:
                i += 1
        else:
            i += 1

    # 3. Hard: combinations of 2-4 rules with 21..35 lines
    i = 0
    while i < len(rules):
        combo_rules = [rules[i]]
        j = i + 1
        while j < len(rules) and len(('\n\n'.join(combo_rules)).splitlines()) < 21:
            combo_rules.append(rules[j])
            j += 1
        combo = '\n\n'.join(combo_rules)
        n = len(combo.splitlines())
        if 21 <= n <= 35:
            chunks['hard'].append(combo)
            i = j
        else:
            i += 1

    # Fallbacks if any category is empty
    if not chunks['easy'] and rules:
        chunks['easy'] = [r for r in rules if len(r.splitlines()) >= 3][:10]
    if not chunks['medium'] and rules:
        chunks['medium'] = [r for r in rules if len(r.splitlines()) >= 6][:10]

    return chunks


def _extract_code_chunks(text: str, slug: str) -> dict:
    """
    Extract easy, medium, and hard snippets from source code.
    """
    lines = text.splitlines()
    if not lines or any(len(l) > 300 for l in lines[:20]):
        return {'easy': [], 'medium': [], 'hard': []}

    chunks = {'easy': [], 'medium': [], 'hard': []}
    targets = [
        ('easy', 5, 10, 8),
        ('medium', 12, 19, 10),
        ('hard', 21, 32, 14),
    ]

    for diff, min_l, max_l, step in targets:
        for i in range(0, len(lines), step):
            window = lines[i:i + max_l]
            while window and not window[-1].strip():
                window.pop()
            while window and not window[0].strip():
                window.pop(0)
            chunk = '\n'.join(window).strip()
            w_lines = chunk.splitlines()
            if min_l <= len(w_lines) <= max_l:
                code_lines = [l for l in w_lines if not l.strip().startswith(('#', '//', '/*'))]
                if len(code_lines) >= min_l // 2:
                    chunks[diff].append(chunk)

    return chunks


def _import_user_repos(user, profile, token: str, max_per_lang: int = 18) -> int:
    """
    Fetch code snippets from user's GitHub repos and save them with imported_by=user.
    Ensures fair distribution across all languages and difficulty levels (easy, medium, hard).
    Returns number of newly created snippets.
    """
    import time
    import requests as req

    repo_list = profile.get_repo_list()
    if not repo_list:
        return 0

    EXT_TO_SLUG = {
        '.py': 'python',
        '.js': 'javascript', '.ts': 'javascript', '.jsx': 'javascript', '.tsx': 'javascript',
        '.java': 'java',
        '.cpp': 'cpp', '.cc': 'cpp', '.cxx': 'cpp', '.h': 'cpp', '.hpp': 'cpp',
        '.go': 'go',
        '.sql': 'sql',
        '.css': 'css', '.scss': 'css', '.sass': 'css', '.less': 'css',
    }

    session = req.Session()
    session.headers.update({
        'Authorization': f'Bearer {token}',
        'Accept': 'application/vnd.github+json',
        'X-GitHub-Api-Version': '2022-11-28',
    })

    # Cache Language objects
    lang_cache = {lang.slug: lang for lang in Language.objects.all()}

    # Safely clear previously imported snippets that have no user attempts,
    # so re-importing replaces obsolete/chopped snippets with fresh, balanced ones.
    user.imported_snippets.filter(attempts__isnull=True).delete()

    created_count = 0
    target_per_difficulty = max(max_per_lang // 3, 4)

    for repo in repo_list:
        try:
            # Get default branch
            r = session.get(f'https://api.github.com/repos/{repo}', timeout=10)
            if r.status_code == 404:
                continue
            r.raise_for_status()
            branch = r.json().get('default_branch', 'main')

            # List files
            r = session.get(
                f'https://api.github.com/repos/{repo}/git/trees/{branch}',
                params={'recursive': '1'}, timeout=10
            )
            r.raise_for_status()
            tree = r.json().get('tree', [])

            # Collect files per language
            files_by_lang: dict = {}
            skip_dirs = ('test', 'tests', '__tests__', 'vendor', 'node_modules', 'dist', 'build', 'migrations', '.git', '.vscode')
            for item in tree:
                if item.get('type') != 'blob':
                    continue
                path = item['path']
                path_lower = path.lower()
                parts = path_lower.split('/')
                if any(p in skip_dirs for p in parts[:-1]):
                    continue
                if any(skip in parts[-1] for skip in ('test', 'spec', '.min.')):
                    continue

                ext = '.' + path.rsplit('.', 1)[-1] if '.' in path else ''
                slug = EXT_TO_SLUG.get(ext.lower())
                if not slug:
                    continue
                files_by_lang.setdefault(slug, []).append(path)

            for slug, paths in files_by_lang.items():
                lang_obj = lang_cache.get(slug)
                if not lang_obj:
                    continue

                random.shuffle(paths)
                lang_candidates = {'easy': [], 'medium': [], 'hard': []}

                for path in paths[:6]:
                    raw_url = f'https://raw.githubusercontent.com/{repo}/{branch}/{path}'
                    rc = session.get(raw_url, timeout=10)
                    if not rc.ok or len(rc.text) > 400_000:
                        continue

                    file_name = path.split('/')[-1]
                    repo_name = repo.split('/')[-1]

                    if slug == 'css':
                        extracted = _extract_css_chunks(rc.text)
                    else:
                        extracted = _extract_code_chunks(rc.text, slug)

                    for diff in ('easy', 'medium', 'hard'):
                        for chunk in extracted.get(diff, []):
                            lang_candidates[diff].append((repo_name, file_name, chunk))

                    if all(len(lang_candidates[d]) >= target_per_difficulty for d in ('easy', 'medium', 'hard')):
                        break

                for diff in ('easy', 'medium', 'hard'):
                    candidates = lang_candidates[diff]
                    random.shuffle(candidates)
                    for repo_name, file_name, chunk in candidates[:target_per_difficulty]:
                        title = f'[MY] {repo_name} — {file_name}'
                        _, was_created = Snippet.objects.get_or_create(
                            language=lang_obj,
                            title=title,
                            code=chunk,
                            imported_by=user,
                            defaults={'difficulty': diff},
                        )
                        if was_created:
                            created_count += 1

            time.sleep(0.2)
        except Exception:
            continue

    return created_count
