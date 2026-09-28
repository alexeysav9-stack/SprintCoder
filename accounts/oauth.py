import re
import secrets
import requests
from urllib.parse import urlencode
from decouple import config

from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme

from .models import SocialAccount

User = get_user_model()

OAUTH_PROVIDERS = {
    'github': {
        'name': 'GitHub',
        'auth_url': 'https://github.com/login/oauth/authorize',
        'token_url': 'https://github.com/login/oauth/access_token',
        'user_url': 'https://api.github.com/user',
        'emails_url': 'https://api.github.com/user/emails',
        'scope': 'read:user user:email',
        'get_client_id': lambda: config('GITHUB_CLIENT_ID', default=''),
        'get_client_secret': lambda: config('GITHUB_CLIENT_SECRET', default=''),
    },
    'google': {
        'name': 'Google',
        'auth_url': 'https://accounts.google.com/o/oauth2/v2/auth',
        'token_url': 'https://oauth2.googleapis.com/token',
        'user_url': 'https://www.googleapis.com/oauth2/v2/userinfo',
        'emails_url': None,
        'scope': 'openid email profile',
        'get_client_id': lambda: config('GOOGLE_CLIENT_ID', default=''),
        'get_client_secret': lambda: config('GOOGLE_CLIENT_SECRET', default=''),
    },
}


def sanitize_username(raw_name: str, fallback_prefix: str = 'user') -> str:
    """Generate a clean, valid Django username."""
    cleaned = re.sub(r'[^a-zA-Z0-9_]', '', raw_name or '').strip()
    if len(cleaned) < 2:
        cleaned = f"{fallback_prefix}_{secrets.token_hex(3)}"
    return cleaned[:28]


def get_unique_username(base_name: str) -> str:
    """Ensure username does not conflict with existing database users."""
    candidate = sanitize_username(base_name)
    if not User.objects.filter(username__iexact=candidate).exists():
        return candidate

    counter = 1
    while True:
        suffix = f"_{counter}"
        adjusted = f"{candidate[:30 - len(suffix)]}{suffix}"
        if not User.objects.filter(username__iexact=adjusted).exists():
            return adjusted
        counter += 1


def oauth_login_view(request, provider: str):
    """
    Initiates the OAuth2 flow by redirecting the user to the provider consent page.
    """
    provider_config = OAUTH_PROVIDERS.get(provider.lower())
    if not provider_config:
        messages.error(request, f'Неподдерживаемый провайдер авторизации: {provider}')
        return redirect('login')

    client_id = provider_config['get_client_id']()
    client_secret = provider_config['get_client_secret']()

    if not client_id or not client_secret:
        messages.warning(
            request,
            f'Вход через {provider_config["name"]} пока не настроен на сервере (задайте {provider.upper()}_CLIENT_ID и {provider.upper()}_CLIENT_SECRET в .env).'
        )
        return redirect('login')

    state = secrets.token_urlsafe(32)
    request.session['oauth_state'] = state
    request.session['oauth_provider'] = provider.lower()

    # Save next redirect safely
    next_url = request.GET.get('next', '')
    if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
        request.session['oauth_next'] = next_url
    else:
        request.session['oauth_next'] = reverse('index')

    redirect_uri = request.build_absolute_uri(reverse('oauth_callback', args=[provider.lower()]))

    params = {
        'client_id': client_id,
        'redirect_uri': redirect_uri,
        'scope': provider_config['scope'],
        'state': state,
    }

    if provider.lower() == 'google':
        params['response_type'] = 'code'
        params['access_type'] = 'online'
        params['prompt'] = 'select_account'

    target_url = f"{provider_config['auth_url']}?{urlencode(params)}"
    return redirect(target_url)


def oauth_callback_view(request, provider: str):
    """
    Handles the OAuth2 callback, exchanges code for access token,
    retrieves user profile, and logs in or creates the user.
    """
    provider_key = provider.lower()
    provider_config = OAUTH_PROVIDERS.get(provider_key)
    if not provider_config:
        messages.error(request, 'Неизвестный провайдер авторизации.')
        return redirect('login')

    # 1. State validation (CSRF protection)
    saved_state = request.session.pop('oauth_state', None)
    received_state = request.GET.get('state')
    next_url = request.session.pop('oauth_next', reverse('index'))

    if not saved_state or saved_state != received_state:
        messages.error(request, 'Ошибка безопасности OAuth: несовпадение проверочного ключа (state). Попробуйте снова.')
        return redirect('login')

    # Check for error from provider
    error = request.GET.get('error')
    if error:
        error_desc = request.GET.get('error_description', error)
        messages.error(request, f'Вход отклонён провайдером {provider_config["name"]}: {error_desc}')
        return redirect('login')

    code = request.GET.get('code')
    if not code:
        messages.error(request, 'Код авторизации не получен от провайдера.')
        return redirect('login')

    client_id = provider_config['get_client_id']()
    client_secret = provider_config['get_client_secret']()
    redirect_uri = request.build_absolute_uri(reverse('oauth_callback', args=[provider_key]))

    # 2. Token exchange
    try:
        if provider_key == 'github':
            token_resp = requests.post(
                provider_config['token_url'],
                headers={'Accept': 'application/json'},
                data={
                    'client_id': client_id,
                    'client_secret': client_secret,
                    'code': code,
                    'redirect_uri': redirect_uri,
                },
                timeout=10,
            )
            token_data = token_resp.json()
            access_token = token_data.get('access_token')

        elif provider_key == 'google':
            token_resp = requests.post(
                provider_config['token_url'],
                data={
                    'client_id': client_id,
                    'client_secret': client_secret,
                    'code': code,
                    'redirect_uri': redirect_uri,
                    'grant_type': 'authorization_code',
                },
                timeout=10,
            )
            token_data = token_resp.json()
            access_token = token_data.get('access_token')
        else:
            access_token = None

        if not access_token:
            messages.error(request, f'Не удалось получить токен доступа от {provider_config["name"]}.')
            return redirect('login')

    except Exception as exc:
        messages.error(request, f'Сетевая ошибка при обмене токена с {provider_config["name"]}: {exc}')
        return redirect('login')

    # 3. Retrieve user profile
    try:
        headers = {'Authorization': f'Bearer {access_token}'}
        user_resp = requests.get(provider_config['user_url'], headers=headers, timeout=10)
        profile_data = user_resp.json()

        if provider_key == 'github':
            uid = str(profile_data.get('id', ''))
            preferred_name = profile_data.get('login', '')
            email = profile_data.get('email')

            # If GitHub email is private, fetch from emails endpoint
            if not email and provider_config['emails_url']:
                try:
                    emails_resp = requests.get(provider_config['emails_url'], headers=headers, timeout=10)
                    emails_list = emails_resp.json()
                    if isinstance(emails_list, list):
                        primary = next((e['email'] for e in emails_list if e.get('primary') and e.get('verified')), None)
                        if not primary:
                            primary = next((e['email'] for e in emails_list if e.get('verified')), None)
                        if primary:
                            email = primary
                except Exception:
                    pass

        elif provider_key == 'google':
            uid = str(profile_data.get('id') or profile_data.get('sub', ''))
            email = profile_data.get('email')
            preferred_name = profile_data.get('name') or (email.split('@')[0] if email else '')

        else:
            uid = ''
            email = None
            preferred_name = ''

        if not uid:
            messages.error(request, f'Не удалось извлечь идентификатор пользователя из ответа {provider_config["name"]}.')
            return redirect('login')

    except Exception as exc:
        messages.error(request, f'Ошибка при получении профиля {provider_config["name"]}: {exc}')
        return redirect('login')

    # 4. Find or create user
    user = None
    social_account = SocialAccount.objects.filter(provider=provider_key, uid=uid).first()

    if social_account:
        # Existing social connection
        user = social_account.user
        social_account.extra_data = profile_data
        social_account.save(update_fields=['extra_data', 'updated_at'])
    elif email:
        # Match by verified email
        existing_user = User.objects.filter(email__iexact=email).first()
        if existing_user:
            user = existing_user
            SocialAccount.objects.create(
                user=user,
                provider=provider_key,
                uid=uid,
                extra_data=profile_data
            )
            messages.info(
                request,
                f'Ваш аккаунт {provider_config["name"]} успешно связан с существующим профилем {user.username}!'
            )

    if not user:
        # Create brand new user
        unique_username = get_unique_username(preferred_name or f"{provider_key}_user")
        user = User.objects.create_user(
            username=unique_username,
            email=email or '',
        )
        user.set_unusable_password()
        user.save()

        SocialAccount.objects.create(
            user=user,
            provider=provider_key,
            uid=uid,
            extra_data=profile_data
        )
        messages.success(request, f'Добро пожаловать в SprintCoder, {user.username}!')
    else:
        messages.success(request, f'С возвращением, {user.username}!')

    # 5. Log in user
    login(request, user)
    return redirect(next_url or 'index')
