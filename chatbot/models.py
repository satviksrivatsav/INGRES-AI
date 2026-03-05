from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class ChatConversation(models.Model):
    BOT_CHOICES = (
        ('public', 'Public Groundwater Bot'),
        ('official', 'Official Policy Bot'),
    )

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    message = models.TextField()
    response = models.TextField()
    bot_type = models.CharField(max_length=10, choices=BOT_CHOICES, default='public')
    timestamp = models.DateTimeField(auto_now_add=True)
    is_anonymous = models.BooleanField(default=False)

    class Meta:
        ordering = ['-timestamp'] # [cite: 313]

    def __str__(self):
        user_label = self.user.email if self.user else "Anonymous"
        return f"{user_label} | {self.bot_type} | {self.timestamp.strftime('%d/%m %H:%M')}"