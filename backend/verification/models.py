from django.db import models
from products.models import Product
from accounts.models import User


class VerifiedProduct(models.Model):
    product = models.OneToOneField(
        Product,
        on_delete=models.CASCADE,
        related_name="verification"
    )
    barcode = models.CharField(max_length=100, unique=True)
    is_authentic = models.BooleanField(default=True)

    class Meta:
        ordering = ["product__name"]
        verbose_name = "Verified Product"
        verbose_name_plural = "Verified Products"

    def __str__(self):
        status = "Authentic ✅" if self.is_authentic else "Fake ❌"
        return f"{self.product.name} [{self.barcode}] - {status}"


class VerificationRequest(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="verifications"
    )
    requested_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    proof = models.CharField(max_length=500, blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ("pending", "Pending"),
            ("accepted", "Accepted"),
            ("rejected", "Rejected"),
        ],
        default="pending"
    )
    reviewed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reviewed_verifications"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Verification Request"
        verbose_name_plural = "Verification Requests"

    def __str__(self):
        return f"Verification {self.id} - {self.product.name} ({self.status})"
