# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_FARMER = "farmer"
    ROLE_DEALER = "dealer"
    ROLE_ADMIN = "admin"
    ROLE_CHOICES = [
        (ROLE_FARMER, "Farmer"),
        (ROLE_DEALER, "Dealer"),
        (ROLE_ADMIN, "Admin"),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_FARMER)
    phone = models.CharField(max_length=30, blank=True, null=True)
    # add more fields if needed

    def __str__(self):
        return self.username
