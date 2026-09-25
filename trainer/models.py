from django.db import models


class Language(models.Model):
    LANGUAGE_CHOICES = [
        ('python', 'Python'),
        ('javascript', 'JavaScript / TypeScript'),
        ('java', 'Java'),
        ('cpp', 'C++'),
        ('go', 'Go'),
        ('sql', 'SQL'),
    ]
    slug = models.CharField(max_length=20, unique=True, choices=LANGUAGE_CHOICES)
    name = models.CharField(max_length=50)
    icon = models.CharField(max_length=10, default='💻')  # emoji icon

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
    title = models.CharField(max_length=100)
    code = models.TextField()
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
