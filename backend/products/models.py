# products/models.py
from django.db import models

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('Seeds', 'Seeds'),
        ('Fertilizers', 'Fertilizers'),
        ('Equipment', 'Equipment'),
        ('Chemicals', 'Chemicals'),
        ('Feeds', 'Feeds'),
        ('Tools', 'Tools'),
        ('Other', 'Other'),
    ]

    name = models.CharField(max_length=255)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Seeds')
    description = models.TextField(blank=True, default='No description available.')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    stock = models.PositiveIntegerField(default=0)
    seller = models.CharField(max_length=255, default='Unknown Dealer')
    rating = models.FloatField(default=0.0)
    reviews_count = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    
    # 🔹 Barcode for product verification
    barcode = models.CharField(max_length=100, unique=True, default='000000000000')

    # 🔹 Expiry date for perishable/agro-chem products
    expiry_date = models.DateField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.barcode})"
