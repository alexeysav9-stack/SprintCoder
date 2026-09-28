from unittest.mock import patch, MagicMock
from django.test import TestCase, RequestFactory, override_settings
from django.contrib.auth import get_user_model
from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.sessions.backends.db import SessionStore
from django.urls import reverse

from accounts.models import SocialAccount
from accounts.oauth import sanitize_username, get_unique_username, oauth_login_view, oauth_callback_view

User = get_user_model()


class SocialAccountModelTests(TestCase):
    def test_social_account_creation(self):
        user = User.objects.create_user(username='octocat', email='octo@github.com')
        account = SocialAccount.objects.create(
            user=user,
            provider='github',
            uid='123456',
            extra_data={'login': 'octocat'}
        )
        self.assertEqual(str(account), 'octocat (github:123456)')
        self.assertEqual(account.provider, 'github')
        self.assertEqual(account.uid, '123456')


class UsernameSanitizationTests(TestCase):
    def test_sanitize_username(self):
        self.assertEqual(sanitize_username('John Doe'), 'JohnDoe')
        self.assertEqual(sanitize_username('alex.dev@test!'), 'alexdevtest')
        self.assertTrue(len(sanitize_username('')) >= 2)

    def test_unique_username_generation(self):
        User.objects.create_user(username='devuser')
        u1 = get_unique_username('devuser')
        self.assertEqual(u1, 'devuser_1')

        User.objects.create_user(username='devuser_1')
        u2 = get_unique_username('devuser')
        self.assertEqual(u2, 'devuser_2')


class OAuthFlowTests(TestCase):
    def setUp(self):
        self.rf = RequestFactory()

    def _setup_request(self, req):
        req.session = SessionStore()
        req.session.create()
        messages = FallbackStorage(req)
        setattr(req, '_messages', messages)
        return req

    def test_oauth_login_disabled_by_default(self):
        req = self._setup_request(self.rf.get('/accounts/oauth/github/'))
        res = oauth_login_view(req, 'github')
        self.assertEqual(res.status_code, 302)
        self.assertEqual(res.url, reverse('login'))

    @override_settings(ENABLE_SOCIAL_AUTH=True)
    def test_oauth_login_unconfigured_shows_warning(self):
        req = self._setup_request(self.rf.get('/accounts/oauth/github/'))
        with patch('accounts.oauth.config', return_value=''):
            res = oauth_login_view(req, 'github')
            self.assertEqual(res.status_code, 302)
            self.assertEqual(res.url, reverse('login'))

    @override_settings(ENABLE_SOCIAL_AUTH=True)
    def test_oauth_login_configured_redirects_to_provider(self):
        req = self._setup_request(self.rf.get('/accounts/oauth/github/?next=/profile/'))
        with patch('accounts.oauth.config', side_effect=lambda k, default='': 'dummy_val' if 'GITHUB' in k else default):
            res = oauth_login_view(req, 'github')
            self.assertEqual(res.status_code, 302)
            self.assertIn('https://github.com/login/oauth/authorize', res.url)
            self.assertIn('client_id=dummy_val', res.url)
            self.assertIn('state=', res.url)
            self.assertTrue(bool(req.session.get('oauth_state')))
            self.assertEqual(req.session.get('oauth_next'), '/profile/')

    def test_oauth_callback_state_mismatch_rejected(self):
        req = self._setup_request(self.rf.get('/accounts/oauth/github/callback/?state=bad_state&code=123'))
        req.session['oauth_state'] = 'good_state'
        res = oauth_callback_view(req, 'github')
        self.assertEqual(res.status_code, 302)
        self.assertEqual(res.url, reverse('login'))

    @patch('accounts.oauth.requests.get')
    @patch('accounts.oauth.requests.post')
    def test_oauth_callback_github_creates_user(self, mock_post, mock_get):
        req = self._setup_request(self.rf.get('/accounts/oauth/github/callback/?state=test_state&code=test_code'))
        req.session['oauth_state'] = 'test_state'
        req.session['oauth_next'] = reverse('index')

        # Mock token exchange
        mock_token_resp = MagicMock()
        mock_token_resp.json.return_value = {'access_token': 'gh_token_123'}
        mock_post.return_value = mock_token_resp

        # Mock user profile
        mock_user_resp = MagicMock()
        mock_user_resp.json.return_value = {
            'id': 987654,
            'login': 'coder_github',
            'name': 'GitHub Coder',
            'email': 'gh_coder@example.com'
        }
        mock_get.return_value = mock_user_resp

        with patch('accounts.oauth.config', return_value='dummy_secret'):
            res = oauth_callback_view(req, 'github')

        self.assertEqual(res.status_code, 302)
        self.assertEqual(res.url, reverse('index'))

        user = User.objects.get(username='coder_github')
        self.assertEqual(user.email, 'gh_coder@example.com')

        social = SocialAccount.objects.get(user=user, provider='github')
        self.assertEqual(social.uid, '987654')

    @patch('accounts.oauth.requests.get')
    @patch('accounts.oauth.requests.post')
    def test_oauth_callback_google_links_existing_email(self, mock_post, mock_get):
        # Create existing user with email
        existing_user = User.objects.create_user(username='alex_existing', email='alex@gmail.com')

        req = self._setup_request(self.rf.get('/accounts/oauth/google/callback/?state=google_state&code=google_code'))
        req.session['oauth_state'] = 'google_state'

        # Mock token exchange
        mock_token_resp = MagicMock()
        mock_token_resp.json.return_value = {'access_token': 'google_token_123'}
        mock_post.return_value = mock_token_resp

        # Mock user profile
        mock_user_resp = MagicMock()
        mock_user_resp.json.return_value = {
            'id': 'google_sub_999',
            'name': 'Alex Google',
            'email': 'alex@gmail.com',
            'verified_email': True
        }
        mock_get.return_value = mock_user_resp

        with patch('accounts.oauth.config', return_value='dummy_secret'):
            res = oauth_callback_view(req, 'google')

        self.assertEqual(res.status_code, 302)

        # Should NOT create duplicate user, but link social account to existing_user
        self.assertEqual(User.objects.filter(email='alex@gmail.com').count(), 1)
        social = SocialAccount.objects.get(user=existing_user, provider='google')
        self.assertEqual(social.uid, 'google_sub_999')

    def test_templates_hide_social_buttons_by_default(self):
        from accounts.views import login_view, register_view

        req_login = self._setup_request(self.rf.get('/accounts/login/'))
        req_login.user = MagicMock(is_authenticated=False)
        res_login = login_view(req_login)
        self.assertEqual(res_login.status_code, 200)
        self.assertNotIn(b'btn-oauth-google', res_login.content)
        self.assertNotIn(b'btn-oauth-github', res_login.content)

        req_reg = self._setup_request(self.rf.get('/accounts/register/'))
        req_reg.user = MagicMock(is_authenticated=False)
        res_reg = register_view(req_reg)
        self.assertEqual(res_reg.status_code, 200)
        self.assertNotIn(b'btn-oauth-google', res_reg.content)
        self.assertNotIn(b'btn-oauth-github', res_reg.content)

    @override_settings(ENABLE_SOCIAL_AUTH=True)
    def test_templates_render_social_buttons_when_enabled(self):
        from accounts.views import login_view, register_view

        req_login = self._setup_request(self.rf.get('/accounts/login/'))
        req_login.user = MagicMock(is_authenticated=False)
        res_login = login_view(req_login)
        self.assertEqual(res_login.status_code, 200)
        self.assertIn(b'btn-oauth-google', res_login.content)
        self.assertIn(b'btn-oauth-github', res_login.content)

        req_reg = self._setup_request(self.rf.get('/accounts/register/'))
        req_reg.user = MagicMock(is_authenticated=False)
        res_reg = register_view(req_reg)
        self.assertEqual(res_reg.status_code, 200)
        self.assertIn(b'btn-oauth-google', res_reg.content)
        self.assertIn(b'btn-oauth-github', res_reg.content)

