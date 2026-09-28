from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class SocialAccount(models.Model):
    """
    Stores linked OAuth2 social accounts (Google, GitHub) for users.
    Allows seamless login, registration, and account linking.
    """
    PROVIDER_CHOICES = [
        ('google', 'Google'),
        ('github', 'GitHub'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='social_accounts')
    provider = models.CharField(max_length=20, choices=PROVIDER_CHOICES)
    uid = models.CharField(max_length=255)
    extra_data = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('provider', 'uid')
        indexes = [
            models.Index(fields=['provider', 'uid']),
        ]

    def __str__(self):
        return f"{self.user.username} ({self.provider}:{self.uid})"
