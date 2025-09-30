
from django.contrib import admin
from .models import ConversationLog

@admin.register(ConversationLog)
class ConversationLogAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "created_at", "short_user_message")
    readonly_fields = ("created_at",)

    def short_user_message(self, obj):
        return (obj.user_message[:60] + "...") if len(obj.user_message) > 60 else obj.user_message
    short_user_message.short_description = "User message"

# Register your models here.
