import json
import random
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from .models import Language, Snippet, Attempt


def index(request):
    """Home page: language + difficulty picker."""
    languages = Language.objects.all()
    difficulty_choices = Snippet.DIFFICULTY_CHOICES
    return render(request, 'trainer/index.html', {
        'languages': languages,
        'difficulty_choices': difficulty_choices,
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
    language_slug = request.GET.get('language', '')
    difficulty = request.GET.get('difficulty', '')

    qs = Snippet.objects.all()
    if language_slug:
        qs = qs.filter(language__slug=language_slug)
    if difficulty:
        qs = qs.filter(difficulty=difficulty)

    if not qs.exists():
        return redirect('index')

    snippet = random.choice(list(qs))
    return redirect('exercise', snippet_id=snippet.pk)


@require_POST
def save_attempt(request):
    """Save a completed attempt via JSON POST."""
    try:
        data = json.loads(request.body)
        snippet_id = data.get('snippet_id')
        snippet = get_object_or_404(Snippet, pk=snippet_id)

        wpm         = float(data.get('wpm', 0))
        cpm         = float(data.get('cpm', 0))
        accuracy    = float(data.get('accuracy', 0))
        time_secs   = float(data.get('time_seconds', 0))

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
    from django.db.models import Max, Avg, Count, Min
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
