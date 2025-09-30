from django.db import models
from django.conf import settings


class ConversationLog(models.Model):
    """
    Simple log of each user → bot exchange.
    Good for quick analytics and intent training.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    user_message = models.TextField()
    bot_response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Log {self.id} – {self.user or 'anon'} @ {self.created_at}"


class ChatSession(models.Model):
    """
    Represents a multi-turn conversation session.
    Groups all ChatMessages into one dialogue history.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="chat_sessions"
    )
    started_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Session {self.id} – {self.user} @ {self.started_at}"


class ChatMessage(models.Model):
    """
    Individual message in a ChatSession (user or bot).
    """
    session = models.ForeignKey(
        ChatSession,
        on_delete=models.CASCADE,
        related_name="messages"
    )
    sender = models.CharField(
        max_length=20,
        choices=[("user", "User"), ("bot", "Bot")],
        default="user"
    )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["session", "created_at"]),
        ]
        ordering = ["created_at"]

    def __str__(self):
        return f"[{self.sender}] {self.text[:40]}..."
