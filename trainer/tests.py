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
        self.assertIn('Code Editor &amp; Typing Field', content)
        self.assertIn('Font Family', content)
        self.assertIn('Cursor Style', content)
        self.assertIn('Cursor Animation', content)
        self.assertIn('Character State Colors', content)
        self.assertIn('Typing Field Width', content)


class SteamTimeTrackingTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='steamcoder', password='password123')
        self.lang, _ = Language.objects.get_or_create(slug='python', defaults={'name': 'Python', 'icon': '🐍'})
        self.snippet = Snippet.objects.create(
            language=self.lang, difficulty='easy', title='Hello World', code='print("hello world")'
        )

    def test_format_exercise_time(self):
        from trainer.utils import format_exercise_time
        res_zero = format_exercise_time(0)
        self.assertEqual(res_zero['hours'], 0)
        self.assertEqual(res_zero['minutes'], 0)
        self.assertEqual(res_zero['formatted'], '0 mins')

        res_secs = format_exercise_time(42)
        self.assertEqual(res_secs['formatted'], '42 secs')

        res_mins = format_exercise_time(3469)  # 57 min 49 sec
        self.assertEqual(res_mins['hours'], 0)
        self.assertEqual(res_mins['minutes'], 57)
        self.assertEqual(res_mins['formatted'], '57 mins')
        self.assertEqual(res_mins['steam_hours'], 1.0)

        res_hours = format_exercise_time(7325)  # 2 hours 2 min 5 sec
        self.assertEqual(res_hours['hours'], 2)
        self.assertEqual(res_hours['minutes'], 2)
        self.assertEqual(res_hours['formatted'], '2 hrs 2 mins')
        self.assertEqual(res_hours['formatted_ru'], '2 ч. 2 мин.')
        self.assertEqual(res_hours['steam_hours'], 2.0)

    def test_user_profile_total_exercise_seconds(self):
        profile, _ = UserProfile.objects.get_or_create(user=self.user)
        self.assertEqual(profile.get_total_exercise_seconds(), 0.0)

        Attempt.objects.create(
            user=self.user, snippet=self.snippet, wpm=60, cpm=300, accuracy=98, time_seconds=45.5
        )
        Attempt.objects.create(
            user=self.user, snippet=self.snippet, wpm=70, cpm=350, accuracy=99, time_seconds=65.5
        )
        self.assertAlmostEqual(profile.get_total_exercise_seconds(), 111.0)

        profile.extra_exercise_seconds = 20.0
        profile.save()
        self.assertAlmostEqual(profile.get_total_exercise_seconds(), 131.0)

    def test_index_page_steam_widget_authenticated(self):
        from django.test import RequestFactory
        from trainer.views import index
        Attempt.objects.create(
            user=self.user, snippet=self.snippet, wpm=80, cpm=400, accuracy=100, time_seconds=120
        )
        rf = RequestFactory()
        request = rf.get('/')
        request.user = self.user
        response = index(request)
        self.assertEqual(response.status_code, 200)
        content = response.content.decode('utf-8')
        self.assertIn('steam-corner-widget', content)
        self.assertIn('TIME PRACTICED', content)
        self.assertIn('2', content)  # 2 mins
        self.assertIn('min', content)

    def test_index_page_steam_widget_anonymous(self):
        from django.test import RequestFactory
        from django.contrib.auth.models import AnonymousUser
        from trainer.views import index
        rf = RequestFactory()
        request = rf.get('/')
        request.user = AnonymousUser()
        response = index(request)
        self.assertEqual(response.status_code, 200)
        content = response.content.decode('utf-8')
        self.assertIn('steam-corner-widget', content)
        self.assertIn('data-authenticated="false"', content)

    def test_profile_page_steam_badge_and_language_time(self):
        from django.test import RequestFactory
        from trainer.views import profile
        Attempt.objects.create(
            user=self.user, snippet=self.snippet, wpm=80, cpm=400, accuracy=100, time_seconds=180
        )
        rf = RequestFactory()
        request = rf.get('/profile/')
        request.user = self.user
        response = profile(request)
        self.assertEqual(response.status_code, 200)
        content = response.content.decode('utf-8')
        self.assertIn('steam-profile-badge', content)
        self.assertIn('TIME PRACTICED', content)
        self.assertIn('Time Practiced', content)
        self.assertIn('3 mins', content)


    def test_record_time_api(self):
        self.client.force_login(self.user)
        # Valid time record
        res = self.client.post('/api/record-time/', '{"seconds": 45}', content_type='application/json')
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data['status'], 'ok')
        self.assertIn('total_time', data)

        profile = UserProfile.objects.get(user=self.user)
        self.assertAlmostEqual(profile.extra_exercise_seconds, 45.0)

        # Out of bounds ignored
        res_ignored = self.client.post('/api/record-time/', '{"seconds": 1}', content_type='application/json')
        self.assertEqual(res_ignored.status_code, 200)
        self.assertEqual(res_ignored.json()['status'], 'ignored')

    def test_save_attempt_returns_total_time(self):
        self.client.force_login(self.user)
        payload = {
            'snippet_id': self.snippet.pk,
            'wpm': 85.0,
            'cpm': 425.0,
            'accuracy': 98.5,
            'time_seconds': 25.0,
            'errors_json': {},
        }
        import json
        res = self.client.post('/api/save-attempt/', json.dumps(payload), content_type='application/json')
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data['status'], 'ok')
        self.assertIsNotNone(data['total_time'])


class BashSupportTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='bashuser', password='password123')
        self.client.force_login(self.user)
        self.bash_lang, _ = Language.objects.get_or_create(slug='bash', defaults={'name': 'Bash', 'icon': '🐚'})
        self.bash_easy = Snippet.objects.create(
            language=self.bash_lang, difficulty='easy', title='Check dir', code='if [ ! -d "$DIR" ]; then\n  mkdir -p "$DIR"\nfi\n'
        )

    def test_bash_devicon(self):
        from trainer.templatetags.trainer_extras import devicon_class, devicon
        self.assertEqual(devicon_class('bash'), 'devicon-bash-plain colored')
        html = str(devicon('bash'))
        self.assertIn('devicon-bash-plain colored', html)

    def test_bash_random_redirect(self):
        res = self.client.get('/exercise/random/?language=bash&difficulty=easy')
        self.assertEqual(res.status_code, 302)
        self.assertEqual(res.url, f'/exercise/{self.bash_easy.pk}/')

    def test_bash_code_chunking(self):
        sample_bash = (
            '# Check directory\n'
            'if [ ! -d "$DIR" ]; then\n'
            '    mkdir -p "$DIR"\n'
            '    echo "Created: $DIR"\n'
            'else\n'
            '    echo "Exists: $DIR"\n'
            'fi\n'
            'exit 0\n'
        )
        chunks = _extract_code_chunks(sample_bash, 'bash')
        self.assertTrue(len(chunks['easy']) > 0)
        self.assertIn('mkdir -p "$DIR"', chunks['easy'][0])


class NewLanguagesSupportTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='polylanguser', password='password123')
        self.client.force_login(self.user)

        self.html_lang, _ = Language.objects.get_or_create(slug='html', defaults={'name': 'HTML', 'icon': '🌐'})
        self.php_lang, _ = Language.objects.get_or_create(slug='php', defaults={'name': 'PHP', 'icon': '🐘'})
        self.csharp_lang, _ = Language.objects.get_or_create(slug='csharp', defaults={'name': 'C#', 'icon': '🔷'})

        self.html_snippet = Snippet.objects.create(
            language=self.html_lang, difficulty='easy', title='HTML Form',
            code='<form action="/login" method="post">\n  <input type="text" name="username" />\n</form>'
        )
        self.php_snippet = Snippet.objects.create(
            language=self.php_lang, difficulty='easy', title='PHP Echo',
            code='<?php\necho "Hello, World!";\n?>'
        )
        self.csharp_snippet = Snippet.objects.create(
            language=self.csharp_lang, difficulty='easy', title='C# Main',
            code='class Program {\n  static void Main() {\n    System.Console.WriteLine("Hi");\n  }\n}'
        )

    def test_devicons(self):
        from trainer.templatetags.trainer_extras import devicon_class, devicon
        self.assertEqual(devicon_class('html'), 'devicon-html5-plain colored')
        self.assertIn('devicon-html5-plain colored', str(devicon('html')))

        self.assertEqual(devicon_class('php'), 'devicon-php-plain colored')
        self.assertIn('devicon-php-plain colored', str(devicon('php')))

        self.assertEqual(devicon_class('csharp'), 'devicon-csharp-plain colored')
        self.assertIn('devicon-csharp-plain colored', str(devicon('csharp')))

    def test_random_redirects(self):
        res_html = self.client.get('/exercise/random/?language=html&difficulty=easy')
        self.assertEqual(res_html.status_code, 302)
        self.assertEqual(res_html.url, f'/exercise/{self.html_snippet.pk}/')

        res_php = self.client.get('/exercise/random/?language=php&difficulty=easy')
        self.assertEqual(res_php.status_code, 302)
        self.assertEqual(res_php.url, f'/exercise/{self.php_snippet.pk}/')

        res_csharp = self.client.get('/exercise/random/?language=csharp&difficulty=easy')
        self.assertEqual(res_csharp.status_code, 302)
        self.assertEqual(res_csharp.url, f'/exercise/{self.csharp_snippet.pk}/')

    def test_html_code_chunking(self):
        sample_html = (
            '<!-- Navigation bar -->\n'
            '<nav class="navbar">\n'
            '    <div class="logo">Brand</div>\n'
            '    <ul class="nav-links">\n'
            '        <li><a href="#home">Home</a></li>\n'
            '        <li><a href="#about">About</a></li>\n'
            '    </ul>\n'
            '</nav>\n'
        )
        chunks = _extract_code_chunks(sample_html, 'html')
        self.assertTrue(len(chunks['easy']) > 0)
        self.assertIn('<nav class="navbar">', chunks['easy'][0])

    def test_php_code_chunking(self):
        sample_php = (
            '<?php\n'
            '// User service class\n'
            'class UserService {\n'
            '    private $db;\n'
            '    public function __construct($db) {\n'
            '        $this->db = $db;\n'
            '    }\n'
            '    public function findUser($id) {\n'
            '        return $this->db->query("SELECT * FROM users WHERE id = ?", [$id]);\n'
            '    }\n'
            '}\n'
        )
        chunks = _extract_code_chunks(sample_php, 'php')
        self.assertTrue(len(chunks['easy']) > 0)
        self.assertIn('class UserService', chunks['easy'][0])

    def test_csharp_code_chunking(self):
        sample_csharp = (
            '// Calculator implementation\n'
            'namespace Demo.Services\n'
            '{\n'
            '    public class Calculator\n'
            '    {\n'
            '        public int Add(int a, int b)\n'
            '        {\n'
            '            return a + b;\n'
            '        }\n'
            '    }\n'
            '}\n'
        )
        chunks = _extract_code_chunks(sample_csharp, 'csharp')
        self.assertTrue(len(chunks['easy']) > 0)
        self.assertIn('public class Calculator', chunks['easy'][0])


class SnippetModerationAndValidationTests(TestCase):
    def test_reject_unbalanced_braces_and_orphan_closing_brace(self):
        """Test that snippets like the user-reported Java constructor with orphan closing brace are rejected."""
        from trainer.snippet_validator import is_valid_snippet
        bad_java = (
            "    public UncheckedInterruptedException(final Throwable cause) {\n"
            "        super(cause);\n"
            "    }\n\n"
            "}"
        )
        ok, reason = is_valid_snippet(bad_java, "java")
        self.assertFalse(ok)
        self.assertTrue("unbalanced_braces" in reason or "orphan_closing_brace" in reason)

    def test_reject_pure_docstring(self):
        """Test that snippets like the user-reported sqlalchemy __init__.py docstring are rejected."""
        from trainer.snippet_validator import is_valid_snippet
        bad_python = (
            '"""Working examples of single-table, joined-table, and concrete-table\n'
            'inheritance as described in :ref:`inheritance_toplevel`.\n\n'
            '.. autosource::\n\n'
            '"""'
        )
        ok, reason = is_valid_snippet(bad_python, "python")
        self.assertFalse(ok)
        self.assertIn("pure_docstring", reason)

    def test_reject_sql_jinja_templates(self):
        """Test that dbt-style Jinja macros in SQL files are rejected."""
        from trainer.snippet_validator import is_valid_snippet
        bad_sql = (
            "{% macro safe_relation_replace(existing_rel) %}\n"
            "SELECT id, name\n"
            "FROM existing_rel\n"
            "WHERE active = 1;\n"
            "{% endmacro %}"
        )
        ok, reason = is_valid_snippet(bad_sql, "sql")
        self.assertFalse(ok)
        self.assertEqual(reason, "sql_jinja_template")

    def test_reject_cut_off_fields(self):
        """Test that fragmented model / form fields cut off from classes are rejected."""
        from trainer.snippet_validator import is_valid_snippet
        bad_cut_off = "FileField,\nSubmitField('Submit'),\nTextAreaField('Notes')"
        ok, reason = is_valid_snippet(bad_cut_off, "python")
        self.assertFalse(ok)

    def test_accept_valid_snippets(self):
        """Test that well-formed functions and classes in multiple languages are accepted."""
        from trainer.snippet_validator import is_valid_snippet

        valid_py = (
            "def calculate_discount(price: float, rate: float = 0.1) -> float:\n"
            "    if rate < 0 or rate > 1:\n"
            "        raise ValueError('Invalid rate')\n"
            "    return price * (1.0 - rate)"
        )
        ok, _ = is_valid_snippet(valid_py, "python")
        self.assertTrue(ok)

        valid_java = (
            "public String formatUser(String name, int age) {\n"
            "    if (age < 0) throw new IllegalArgumentException();\n"
            "    return String.format(\"%s (%d)\", name, age);\n"
            "}"
        )
        ok, _ = is_valid_snippet(valid_java, "java")
        self.assertTrue(ok)

    def test_excluded_file_paths(self):
        """Test that test files, locales, __init__.py, and vendor files are excluded."""
        from trainer.snippet_validator import is_excluded_file_path
        self.assertTrue(is_excluded_file_path("sqlalchemy/__init__.py"))
        self.assertTrue(is_excluded_file_path("setup.py"))
        self.assertTrue(is_excluded_file_path("tests/test_parser.py"))
        self.assertTrue(is_excluded_file_path("src/locale/ar-ma.js"))
        self.assertTrue(is_excluded_file_path("vendor/bundle.min.js"))

        self.assertFalse(is_excluded_file_path("app/services/calculator.py"))
        self.assertFalse(is_excluded_file_path("src/utils/formatters.js"))

    def test_purge_garbage_snippets_command(self):
        """Test that purge_garbage_snippets removes invalid snippets and preserves valid ones."""
        from django.core.management import call_command
        from trainer.models import Language, Snippet

        py_lang, _ = Language.objects.get_or_create(slug="python", defaults={"name": "Python"})
        # Create a garbage snippet with [GH] tag
        bad_snip = Snippet.objects.create(
            language=py_lang,
            difficulty="easy",
            title="[GH] test_repo — __init__.py",
            code='"""Only a docstring\nwith no actual code\nand sphinx directive\n"""',
        )
        # Create a valid snippet
        good_snip = Snippet.objects.create(
            language=py_lang,
            difficulty="easy",
            title="[GH] test_repo — utils.py",
            code=(
                "def add(a, b):\n"
                "    total = a + b\n"
                "    result = total * 2\n"
                "    return result"
            ),
        )

        call_command("purge_garbage_snippets")

        self.assertFalse(Snippet.objects.filter(pk=bad_snip.pk).exists())
        self.assertTrue(Snippet.objects.filter(pk=good_snip.pk).exists())




