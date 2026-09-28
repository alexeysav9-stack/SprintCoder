from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


class Language(models.Model):
    LANGUAGE_CHOICES = [
        ('python', 'Python'),
        ('javascript', 'JavaScript / TypeScript'),
        ('java', 'Java'),
        ('cpp', 'C++'),
        ('go', 'Go'),
        ('sql', 'SQL'),
        ('css', 'CSS'),
        ('bash', 'Bash'),
        ('html', 'HTML'),
        ('php', 'PHP'),
        ('csharp', 'C#'),
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
    extra_exercise_seconds = models.FloatField(
        default=0.0,
        help_text='Additional exercise time from practice sessions in seconds'
    )

    def __str__(self):
        return f"Profile({self.user.username})"

    def get_repo_list(self) -> list:
        """Return a cleaned list of owner/repo strings."""
        return [
            line.strip()
            for line in self.github_repos.splitlines()
            if line.strip() and '/' in line.strip()
        ]

    def get_total_exercise_seconds(self) -> float:
        """Return total seconds spent in exercises (completed attempts + extra practice)."""
        attempt_time = self.user.attempts.aggregate(models.Sum('time_seconds'))['time_seconds__sum'] or 0.0
        return float(attempt_time) + float(self.extra_exercise_seconds)

    def get_streak_info(self) -> dict:
        """Return the user's daily exercise streak information."""
        from .utils import get_user_streak
        return get_user_streak(self.user)



class SiteVisit(models.Model):
    """Stores page visit records for admin analytics and traffic monitoring."""
    DEVICE_CHOICES = [
        ('desktop', 'Desktop'),
        ('mobile', 'Mobile'),
        ('tablet', 'Tablet'),
        ('bot', 'Bot'),
    ]

    timestamp = models.DateTimeField(default=timezone.now, db_index=True)
    path = models.CharField(max_length=255, db_index=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user = models.ForeignKey(
        'auth.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='site_visits'
    )
    session_key = models.CharField(max_length=64, blank=True, db_index=True)
    user_agent = models.CharField(max_length=500, blank=True)
    device_type = models.CharField(max_length=20, choices=DEVICE_CHOICES, default='desktop', db_index=True)
    browser = models.CharField(max_length=50, blank=True)
    referer = models.CharField(max_length=500, blank=True)
    status_code = models.PositiveSmallIntegerField(default=200)

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['timestamp', 'session_key']),
            models.Index(fields=['timestamp', 'user']),
            models.Index(fields=['timestamp', 'device_type']),
        ]

    def __str__(self):
        user_str = self.user.username if self.user else (f"session:{self.session_key[:8]}" if self.session_key else 'guest')
        return f"[{self.timestamp:%Y-%m-%d %H:%M}] {self.path} ({user_str})"


@receiver(post_save, sender='auth.User')
def create_user_profile(sender, instance, created, **kwargs):
    """Automatically create a UserProfile when a new User is registered."""
    if created:
        UserProfile.objects.get_or_create(user=instance)


