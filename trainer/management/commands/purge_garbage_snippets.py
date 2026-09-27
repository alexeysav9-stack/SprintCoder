"""
Management command: purge_garbage_snippets
------------------------------------------
Scans the Snippet database and purges low-quality / garbage snippets:
- Pure docstrings and comments (e.g. __init__.py docstrings)
- Unbalanced curly braces / orphan braces (e.g. UncheckedInterruptedException.java)
- Incomplete syntax or cut-off fields
- Jinja templates stored as SQL
- Snippets from excluded test/locale/config files

Usage:
    python manage.py purge_garbage_snippets [--dry-run]
"""

from django.core.management.base import BaseCommand
from trainer.models import Snippet
from trainer.snippet_validator import is_valid_snippet, is_excluded_file_path


class Command(BaseCommand):
    help = "Purge low-quality or broken code snippets from the database."

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show snippets that would be purged without actually deleting them.",
        )
        parser.add_argument(
            "--purge-all-gh",
            action="store_true",
            help="Purge all GitHub-sourced snippets ([GH]).",
        )

    def handle(self, *args, **options):
        dry_run = options.get("dry_run", False)
        purge_all_gh = options.get("purge_all_gh", False)

        all_snippets = Snippet.objects.all()
        to_delete = []
        stats_by_lang = {}
        reasons_count = {}

        self.stdout.write(f"Auditing {all_snippets.count()} snippets in database...")

        for s in all_snippets:
            # Never purge standard seed snippets
            is_seed = (s.imported_by is None and "[GH]" not in s.title)
            if is_seed:
                continue

            if purge_all_gh and "[GH]" in s.title:
                to_delete.append((s, "purge_all_gh"))
                lang = s.language.slug
                stats_by_lang[lang] = stats_by_lang.get(lang, 0) + 1
                reasons_count["purge_all_gh"] = reasons_count.get("purge_all_gh", 0) + 1
                continue

            # Check for excluded file names in title
            title_lower = s.title.lower()
            if any(f in title_lower for f in ("__init__.py", "__version__.py", "setup.py", "conftest.py", "moment — ")):
                to_delete.append((s, "excluded_filename"))
                lang = s.language.slug
                stats_by_lang[lang] = stats_by_lang.get(lang, 0) + 1
                reasons_count["excluded_filename"] = reasons_count.get("excluded_filename", 0) + 1
                continue

            # Validate code
            ok, reason = is_valid_snippet(s.code, s.language.slug)
            if not ok:
                to_delete.append((s, reason))
                lang = s.language.slug
                stats_by_lang[lang] = stats_by_lang.get(lang, 0) + 1
                r_key = reason.split(":")[0]
                reasons_count[r_key] = reasons_count.get(r_key, 0) + 1

        self.stdout.write(f"\nFound {len(to_delete)} garbage snippet(s) to purge:")
        for r, cnt in sorted(reasons_count.items(), key=lambda x: x[1], reverse=True):
            self.stdout.write(f"  - {r}: {cnt}")

        self.stdout.write("\nBreakdown by language:")
        for lang, cnt in sorted(stats_by_lang.items(), key=lambda x: x[1], reverse=True):
            self.stdout.write(f"  - {lang}: {cnt}")

        if dry_run:
            self.stdout.write(self.style.WARNING("\n[DRY RUN] No snippets were deleted."))
        else:
            deleted_ids = [s.id for s, _ in to_delete]
            deleted_count, _ = Snippet.objects.filter(id__in=deleted_ids).delete()
            self.stdout.write(
                self.style.SUCCESS(f"\nSuccessfully purged {deleted_count} snippet(s) from database!")
            )
