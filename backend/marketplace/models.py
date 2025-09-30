from django.db import models
from accounts.models import User
from products.models import Product
from django.utils import timezone


class Dealer(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,  # Keep dealer data even if user is deleted
        related_name='dealer_profile',
        null=True,
        blank=True
    )
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    verified = models.BooleanField(default=False)  # Only verified dealers are shown
    created_at = models.DateTimeField(default=timezone.now)  # Migration-friendly
    updated_at = models.DateTimeField(auto_now=True)  # Track updates

    class Meta:
        ordering = ['-verified', '-created_at']
        verbose_name = 'Dealer'
        verbose_name_plural = 'Dealers'

    def __str__(self):
        return f"{self.name} ({'Verified' if self.verified else 'Unverified'})"


class Listing(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="listings"
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="listings"
    )
    price = models.DecimalField(max_digits=12, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    description = models.TextField(blank=True, null=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)  # Migration-friendly
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.name} — {self.owner.username}"


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    listings = models.ManyToManyField(
        Listing,
        related_name="tags",
        blank=True
    )

    def __str__(self):
        return self.name
