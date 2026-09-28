# 🚀 Инструкция по развёртыванию SprintCoder на сервере

Данное руководство описывает варианты публикации веб-приложения **SprintCoder** в продакшен.

---

## 📋 Чек-лист: Что нужно подготовить пользователю перед запуском

Вам потребуется создать файл `.env` на сервере (на основе шаблона `.env.example`) и заполнить следующие параметры:

1. **Сгенерировать боевой `SECRET_KEY`**:
   Сгенерируйте надёжный случайный ключ одной командой в терминале:
   ```bash
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```
   Вставьте результат в `SECRET_KEY=...`.

2. **Отключить режим отладки**:
   ```ini
   DEBUG=False
   ```

3. **Указать ваш домен или IP-адрес сервера**:
   В `ALLOWED_HOSTS` перечислите через запятую все домены/IP, с которых будет открываться сайт:
   ```ini
   ALLOWED_HOSTS=sprintcoder.ru,www.sprintcoder.ru,185.xxx.xxx.xxx
   ```
   В `CSRF_TRUSTED_ORIGINS` укажите HTTPS-адрес вашего сайта:
   ```ini
   CSRF_TRUSTED_ORIGINS=https://sprintcoder.ru,https://www.sprintcoder.ru
   ```

4. **Задать данные базы данных PostgreSQL**:
   - При использовании Docker или локального PostgreSQL:
     ```ini
     DB_NAME=sprintcoder
     DB_USER=sprintcoder
     DB_PASSWORD=придумайте_сложный_пароль_здесь
     DB_HOST=db       # для Docker оставьте 'db', для обычного сервера 'localhost'
     DB_PORT=5432
     ```
   - Если используется облачная база (Neon, Supabase, Railway):
     ```ini
     DATABASE_URL=postgresql://user:password@ep-xxx.neon.tech/sprintcoder?sslmode=require
     ```

5. **Настройки безопасности HTTPS (включать после настройки SSL-сертификата)**:
   ```ini
   SECURE_SSL_REDIRECT=True
   SESSION_COOKIE_SECURE=True
   CSRF_COOKIE_SECURE=True
   ```

6. **(Опционально) GitHub Personal Access Token**:
   Для импорта сниппетов из публичных репозиториев:
   ```ini
   GITHUB_TOKEN=ghp_ваш_токен_с_github
   ```

---

## Вариант 1 (Рекомендуемый): Развёртывание через Docker Compose

Самый простой и изолированный способ. Сервер поднимает Django (Gunicorn + WhiteNoise) и базу данных PostgreSQL 16 в связанных контейнерах.

### 1. Клонирование репозитория на сервер
```bash
git clone https://github.com/ваше_имя/SprintCoder.git /var/www/sprintcoder
cd /var/www/sprintcoder
```

### 2. Настройка файла переменных окружения
```bash
cp .env.example .env
nano .env
```
*(заполните `SECRET_KEY`, `ALLOWED_HOSTS`, `DB_PASSWORD`)*

### 3. Запуск контейнеров
```bash
docker compose up -d --build
```
Docker автоматически:
- Соберёт образ с Python 3.12 и зависимостями;
- Запустит контейнер PostgreSQL 16 с постоянным дисковым хранилищем;
- Применит все миграции базы данных;
- Соберёт и сожмёт статические файлы через WhiteNoise;
- Запустит Gunicorn на 3 воркера.

### 4. Создание администратора
```bash
docker compose exec web python manage.py createsuperuser
```

### 5. Первичное наполнение сниппетами
```bash
docker compose exec web python manage.py seed_snippets
```

---

## Вариант 2: Классическое развёртывание на Linux VPS (Ubuntu / Debian + Nginx)

Если вы предпочитаете прямое окружение на сервере без Docker.

### 1. Установка системных пакетов
```bash
sudo apt update && sudo apt install -y python3 python3-venv python3-pip postgresql postgresql-contrib nginx certbot python3-certbot-nginx git curl
```

### 2. Создание базы данных PostgreSQL
```bash
sudo -u postgres psql
```
```sql
CREATE DATABASE sprintcoder;
CREATE USER sprintcoder WITH PASSWORD 'ваш_надежный_пароль';
ALTER ROLE sprintcoder SET client_encoding TO 'utf8';
ALTER ROLE sprintcoder SET default_transaction_isolation TO 'read committed';
ALTER ROLE sprintcoder SET timezone TO 'Europe/Moscow';
GRANT ALL PRIVILEGES ON DATABASE sprintcoder TO sprintcoder;
\q
```

### 3. Клонирование и настройка виртуального окружения
```bash
sudo git clone https://github.com/ваше_имя/SprintCoder.git /var/www/sprintcoder
cd /var/www/sprintcoder
sudo chown -R www-data:www-data /var/www/sprintcoder
sudo chmod -R 775 /var/www/sprintcoder

# Создание venv от имени www-data
sudo -u www-data python3 -m venv venv
sudo -u www-data ./venv/bin/pip install --upgrade pip
sudo -u www-data ./venv/bin/pip install -r requirements.txt
```

### 4. Настройка .env и применение миграций
```bash
sudo -u www-data cp .env.example .env
sudo -u www-data nano .env

# Применение миграций и сбор статики
sudo -u www-data ./venv/bin/python manage.py migrate
sudo -u www-data ./venv/bin/python manage.py collectstatic --noinput
sudo -u www-data ./venv/bin/python manage.py createsuperuser
sudo -u www-data ./venv/bin/python manage.py seed_snippets
```

### 5. Настройка Systemd для автозапуска Gunicorn
Скопируйте подготовленный юнит-файл:
```bash
sudo cp deploy/sprintcoder.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl start sprintcoder
sudo systemctl enable sprintcoder
sudo systemctl status sprintcoder
```

### 6. Настройка Nginx и SSL
Скопируйте конфигурацию Nginx:
```bash
sudo cp deploy/nginx.conf /etc/nginx/sites-available/sprintcoder
sudo nano /etc/nginx/sites-available/sprintcoder  # Замените yourdomain.com на ваш домен
sudo ln -s /etc/nginx/sites-available/sprintcoder /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

Получите бесплатный SSL-сертификат от Let's Encrypt:
```bash
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

После получения SSL не забудьте включить в `.env`:
```ini
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```
И перезагрузить сервис:
```bash
sudo systemctl restart sprintcoder
```

---

## 🔍 Проверка работоспособности

- **Главная страница**: `https://yourdomain.com/`
- **Панель Django Admin**: `https://yourdomain.com/admin/`
- **Панель аналитики посещаемости**: `https://yourdomain.com/admin/analytics/`
