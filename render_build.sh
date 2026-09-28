#!/usr/bin/env bash
# exit on error
set -o errexit

echo "==> Upgrading pip..."
pip install --upgrade pip

echo "==> Installing Python dependencies..."
pip install -r requirements.txt

echo "==> Collecting and compressing static files (WhiteNoise)..."
python manage.py collectstatic --noinput

echo "==> Applying database migrations on Neon PostgreSQL..."
python manage.py migrate --noinput

echo "==> Checking starter code snippets in database..."
python manage.py shell -c "
from trainer.models import Snippet
count = Snippet.objects.count()
if count == 0:
    print('==> Empty database detected. Seeding starter snippets...')
    from django.core.management import call_command
    call_command('seed_snippets')
    print('==> Seeding completed successfully!')
else:
    print(f'==> Database already contains {count} snippets. Skipping seed.')
" || true

echo "==> Render build finished successfully!"
