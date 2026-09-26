from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Language(models.Model):
    LANGUAGE_CHOICES = [
        ('python', 'Python'),
        ('javascript', 'JavaScript / TypeScript'),
        ('java', 'Java'),
        ('cpp', 'C++'),
        ('go', 'Go'),
        ('sql', 'SQL'),
        ('css', 'CSS'),
    ]
    slug = models.CharField(max_length=20, unique=True, choices=LANGUAGE_CHOICES)
    name = models.CharField(max_length=50)
    icon = models.CharField(max_length=10, default='💻')  # emoji icon (legacy, kept for admin)

    def __str__(self):
        return self.name


class Snippet(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]
    language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name='snippets')
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES)
    title = models.CharField(max_length=200)
    code = models.TextField()
    # Optional: user who imported this snippet (for "my repos" feature)
    imported_by = models.ForeignKey(
        'auth.User', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='imported_snippets'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.language.slug}] {self.title} ({self.difficulty})"

    def line_count(self):
        return len(self.code.strip().splitlines())


class Attempt(models.Model):
    user = models.ForeignKey(
        'auth.User', on_delete=models.CASCADE, related_name='attempts', null=True, blank=True
    )
    snippet = models.ForeignKey(Snippet, on_delete=models.CASCADE, related_name='attempts')
    wpm = models.FloatField()
    cpm = models.FloatField()
    accuracy = models.FloatField()  # 0.0 - 100.0
    time_seconds = models.FloatField()
    errors_json = models.JSONField(default=dict)  # {"a": 3, "s": 1, ...}
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        user_str = self.user.username if self.user else 'anonymous'
        return f"{user_str} — {self.snippet} — {self.wpm:.0f} WPM"


class UserProfile(models.Model):
    """Extended user profile — stores GitHub repos for personal snippet import."""
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, related_name='userprofile')
    # Newline-separated list of "owner/repo" strings
    github_repos = models.TextField(blank=True, default='',
                                    help_text='One repo per line, format: owner/repo')
    last_import_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Profile({self.user.username})"

    def get_repo_list(self) -> list:
        """Return a cleaned list of owner/repo strings."""
        return [
            line.strip()
            for line in self.github_repos.splitlines()
            if line.strip() and '/' in line.strip()
        ]


@receiver(post_save, sender='auth.User')
def create_user_profile(sender, instance, created, **kwargs):
    """Automatically create a UserProfile when a new User is registered."""
    if created:
        UserProfile.objects.get_or_create(user=instance)

