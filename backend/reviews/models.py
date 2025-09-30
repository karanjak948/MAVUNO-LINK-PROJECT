from django.db import models
from accounts.models import User   # ✅ your custom User
from products.models import Product
from marketplace.models import Dealer   # ✅ reuse Dealer from marketplace


class Review(models.Model):
    reviewer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviews"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="product_reviews",
        null=True,
        blank=True
    )
    dealer = models.ForeignKey(
        Dealer,
        on_delete=models.CASCADE,
        related_name="dealer_reviews",
        null=True,
        blank=True
    )
    rating = models.PositiveIntegerField(default=5)
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        if self.product:
            target = self.product.name
        elif self.dealer:
            target = self.dealer.business_name  # ✅ matches marketplace.Dealer
        else:
            target = "Unknown"
        return f"Review by {self.reviewer.username} on {target}"
