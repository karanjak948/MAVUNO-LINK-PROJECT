from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import VerifiedProduct, VerificationRequest


@admin.register(VerifiedProduct)
class VerifiedProductAdmin(admin.ModelAdmin):
    list_display = ("product_link", "barcode", "is_authentic", "is_authentic_status")
    search_fields = ("product__name", "barcode")
    list_filter = ("is_authentic",)
    list_editable = ("is_authentic",)
    ordering = ("product__name",)

    def is_authentic_status(self, obj):
        """Display authenticity with ✅/❌ icons"""
        color = "green" if obj.is_authentic else "red"
        label = "Authentic" if obj.is_authentic else "Fake"
        return format_html(
            '<span style="color:{}; font-weight:bold;">{}</span>', color, label
        )
    is_authentic_status.short_description = "Authenticity"

    def product_link(self, obj):
        """Clickable product name linking to edit page"""
        url = reverse("admin:products_product_change", args=[obj.product.id])
        return format_html('<a href="{}">{}</a>', url, obj.product.name)
    product_link.short_description = "Product"


@admin.register(VerificationRequest)
class VerificationRequestAdmin(admin.ModelAdmin):
    list_display = ("product_link", "requested_by", "status", "created_at", "reviewed_by")
    search_fields = ("product__name", "requested_by__username", "reviewed_by__username")
    list_filter = ("status", "created_at")
    list_editable = ("status",)
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")
    date_hierarchy = "created_at"

    def product_link(self, obj):
        """Clickable product name linking to VerifiedProduct"""
        url = reverse("admin:verification_verifiedproduct_change", args=[obj.product.id])
        return format_html('<a href="{}">{}</a>', url, obj.product.name)
    product_link.short_description = "Product"
