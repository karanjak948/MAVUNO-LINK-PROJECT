# reviews/models.py
from django.db import models
from accounts.models import User
from products.models import Product

class ProductReview(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    rating = models.PositiveSmallIntegerField()  # 1-5
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} - {self.rating}"

class DealerReview(models.Model):
    dealer = models.ForeignKey('marketplace.Dealer', on_delete=models.CASCADE, related_name="dealer_reviews")
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="authored_dealer_reviews")
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.dealer.name} - {self.rating}"
