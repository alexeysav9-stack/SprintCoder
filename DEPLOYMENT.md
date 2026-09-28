# 🚀 Инструкция по развёртыванию SprintCoder на сервере

Данное руководство описывает варианты публикации веб-приложения **SprintCoder** в продакшен.

---

## 🌟 Вариант №0 (Самый простой): Neon.tech (База данных) + Render.com (Хостинг)

Это наиболее современная, быстрая и бесплатная связка:
- **Neon.tech** предоставляет серверную бессерверную базу данных PostgreSQL.
- **Render.com** собирает проект напрямую из вашего GitHub, раздаёт статику через WhiteNoise, запускает Gunicorn и автоматически выдаёт бесплатный SSL-сертификат (HTTPS).

### Шаг 1. Скопировать строку подключения из Neon.tech
1. Откройте консоль [console.neon.tech](https://console.neon.tech/) и выберите ваш проект (`nameless-flower-41925418`).
2. В блоке **Connection Details** (на главном экране дашборда):
   - Убедитесь, что выбран переключатель **Pooled connection** (рекомендуется) или Direct.
   - Скопируйте строку подключения (**Connection string**). Она выглядит так:
     ```text
     postgresql://neondb_owner:ПАРОЛЬ@ep-nameless-flower-41925418-pooler.eu-central-1.aws.neon.tech/neondb?sslmode=require
     ```

### Шаг 2. Развёртывание на Render.com
1. Зарегистрируйтесь или войдите на [dashboard.render.com](https://dashboard.render.com/) (удобно войти через GitHub).
2. Нажмите синюю кнопку **New +** в верхнем правом углу → выберите **Web Service**.
3. Подключите ваш репозиторий **SprintCoder** (если репозиторий не отображается, нажмите *Configure account* и предоставьте доступ).
4. Заполните параметры веб-сервиса:
   - **Name**: `sprintcoder` (ваш сайт будет доступен по адресу `https://sprintcoder.onrender.com`)
   - **Region**: `Frankfurt (EU Central)` (наиболее близкий регион с минимальным пингом)
   - **Branch**: `main`
   - **Runtime**: `Python 3`
   - **Build Command**:
     ```bash
     ./render_build.sh
     ```
   - **Start Command**:
     ```bash
     gunicorn sprintcoder.wsgi:application
     ```
   - **Instance Type**: `Free` ($0/mo)

5. В разделе **Environment Variables** (Переменные окружения) добавьте:
   | Ключ (Key) | Значение (Value) | Описание |
   | :--- | :--- | :--- |
   | `DATABASE_URL` | *вставьте строку из Neon* | Строка подключения к PostgreSQL |
   | `PYTHON_VERSION` | `3.12.8` | Версия Python |
   | `SECRET_KEY` | *(нажмите «Generate»)* | Секретный ключ Django |
   | `DEBUG` | `False` | Отключение режима отладки |
   | `TIME_ZONE` | `Europe/Moscow` | Часовой пояс аналитики |

6. Нажмите **Deploy Web Service**!

### Шаг 3. Что произойдет автоматически
Render запустит скрипт `./render_build.sh`:
- Установит все зависимости из `requirements.txt`;
- Соберёт и сожмёт статические файлы через WhiteNoise;
- Автоматически накатит миграции на вашу базу в Neon;
- Обнаружит пустую базу и сам наполнит её 280+ стартовыми сниппетами по всем 11 языкам;
- Запустит Gunicorn и выдаст защищённый HTTPS-домен.

### Шаг 4. Создание аккаунта администратора
Когда деплой завершится:
1. В дашборде вашего сервиса на Render перейдите на вкладку **Shell** (консоль в браузере).
2. Выполните команду:
   ```bash
   python manage.py createsuperuser
   ```
3. Введите логин, email и пароль.
4. Готово! Теперь вы можете войти в панель администратора `https://ваше-имя.onrender.com/admin/` и открыть панель аналитики `https://ваше-имя.onrender.com/admin/analytics/`!

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

6. **Настройка входа через Google и GitHub (OAuth 2.0)**:
   - **GitHub OAuth**:
     1. Откройте GitHub: *Settings → Developer settings → OAuth Apps → New OAuth App*.
     2. В поле *Homepage URL* укажите: `https://yourdomain.com`
     3. В поле *Authorization callback URL* укажите:
        `https://yourdomain.com/accounts/oauth/github/callback/`
        *(для локального тестирования: `http://127.0.0.1:8000/accounts/oauth/github/callback/`)*
     4. Скопируйте **Client ID** и **Client Secret** в `.env`:
        ```ini
        GITHUB_CLIENT_ID=ваш_github_client_id
        GITHUB_CLIENT_SECRET=ваш_github_client_secret
        ```
   - **Google OAuth 2.0**:
     1. Откройте [Google Cloud Console](https://console.cloud.google.com/) → *APIs & Services → Credentials*.
     2. Создайте *OAuth client ID* (Тип приложения: Web application).
     3. В поле *Authorized redirect URIs* укажите:
        `https://yourdomain.com/accounts/oauth/google/callback/`
        *(для локального тестирования: `http://127.0.0.1:8000/accounts/oauth/google/callback/`)*
     4. Скопируйте **Client ID** и **Client Secret** в `.env`:
        ```ini
        GOOGLE_CLIENT_ID=ваш_google_client_id
        GOOGLE_CLIENT_SECRET=ваш_google_client_secret
        ```

7. **(Опционально) GitHub Personal Access Token**:
   Для импорта сниппетов из публичных репозиториев пользователей:
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
