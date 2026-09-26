from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from trainer.models import Language, Snippet, Attempt, UserProfile
from trainer.views import _extract_css_chunks, _extract_code_chunks


class CSSChunkingTests(TestCase):
    def test_extract_css_chunks(self):
        css_sample = """
        /* Main header */
        .header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 1rem 2rem;
            background: #fff;
        }

        /* Navigation menu */
        .nav-item {
            margin: 0 10px;
            color: #333;
            text-decoration: none;
            font-size: 14px;
        }

        .nav-item:hover {
            color: #007bff;
        }

        /* Hero banner */
        .hero {
            position: relative;
            min-height: 400px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            color: white;
            padding: 40px 20px;
            text-align: center;
        }
        """
        chunks = _extract_css_chunks(css_sample)
        self.assertTrue(len(chunks['easy']) > 0)
        for chunk in chunks['easy']:
            lines = chunk.splitlines()
            self.assertTrue(4 <= len(lines) <= 10)
            self.assertTrue('{' in chunk and '}' in chunk)

    def test_extract_code_chunks(self):
        py_sample = "\n".join([f"x_{i} = {i} * 2" for i in range(50)])
        chunks = _extract_code_chunks(py_sample, "python")
        self.assertTrue(len(chunks['easy']) > 0)
        self.assertTrue(len(chunks['medium']) > 0)
        self.assertTrue(len(chunks['hard']) > 0)


class RandomSnippetViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.force_login(self.user)

        self.css_lang, _ = Language.objects.get_or_create(slug='css', defaults={'name': 'CSS'})
        self.py_lang, _ = Language.objects.get_or_create(slug='python', defaults={'name': 'Python'})

        # Standard snippets
        Snippet.objects.create(language=self.css_lang, difficulty='easy', title='Global CSS Easy', code='body { margin: 0; }')

        # User imported CSS snippets
        self.user_css_easy = Snippet.objects.create(
            language=self.css_lang, difficulty='easy', title='[MY] repo - style.css',
            code='.btn { padding: 10px; color: red; }', imported_by=self.user
        )
        self.user_css_med = Snippet.objects.create(
            language=self.css_lang, difficulty='medium', title='[MY] repo - style.css',
            code='.btn {\n padding: 10px;\n color: red;\n border: none;\n border-radius: 4px;\n margin: 5px;\n font-size: 14px;\n font-weight: bold;\n display: inline-block;\n text-align: center;\n cursor: pointer;\n}',
            imported_by=self.user
        )

    def test_my_repos_css_easy(self):
        response = self.client.get('/exercise/random/?language=css&difficulty=easy&my_repos=1')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f'/exercise/{self.user_css_easy.pk}/')

    def test_my_repos_css_difficulty_fallback(self):
        # User has no hard CSS snippet, but has easy and medium
        response = self.client.get('/exercise/random/?language=css&difficulty=hard&my_repos=1')
        self.assertEqual(response.status_code, 302)
        self.assertIn(response.url, [f'/exercise/{self.user_css_easy.pk}/', f'/exercise/{self.user_css_med.pk}/'])

    def test_my_repos_no_language_snippets(self):
        # User has no Python snippets imported
        response = self.client.get('/exercise/random/?language=python&difficulty=easy&my_repos=1')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')
        msgs = [m.message for m in get_messages(response.wsgi_request)]
        self.assertTrue(any('Python' in m for m in msgs))

    def test_my_repos_not_imported_yet(self):
        other_user = User.objects.create_user(username='newbie', password='password123')
        self.client.force_login(other_user)
        response = self.client.get('/exercise/random/?language=css&difficulty=easy&my_repos=1')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')
        msgs = [m.message for m in get_messages(response.wsgi_request)]
        self.assertTrue(any('imported any snippets' in m for m in msgs))

    def test_random_language_standard(self):
        response = self.client.get('/exercise/random/?language=random&difficulty=easy')
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/exercise/'))

    def test_random_language_my_repos(self):
        response = self.client.get('/exercise/random/?language=random&difficulty=easy&my_repos=1')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f'/exercise/{self.user_css_easy.pk}/')

    def test_settings_page_renders(self):
        from django.test import RequestFactory
        from trainer.views import settings_view
        rf = RequestFactory()
        request = rf.get('/settings/')
        request.user = self.user
        response = settings_view(request)
        self.assertEqual(response.status_code, 200)
        content = response.content.decode('utf-8')
        self.assertIn('Color Theme', content)
        self.assertIn('Catppuccin Mocha', content)
