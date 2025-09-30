
from django.contrib import admin
from .models import Dealer

@admin.register(Dealer)
class DealerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'address', 'created_at')
    search_fields = ('name', 'email', 'phone')

