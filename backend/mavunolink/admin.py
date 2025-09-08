from django.contrib import admin
from .models import Profile

# Register Profile model in Django Admin
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')
