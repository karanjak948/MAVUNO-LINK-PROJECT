from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'seller', 'category', 'price', 'stock', 'rating', 'expiry_date', 'created_at')
    list_filter = ('category', 'expiry_date', 'created_at', 'updated_at')
    search_fields = ('name', 'seller', 'barcode')
