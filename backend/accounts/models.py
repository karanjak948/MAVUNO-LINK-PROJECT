# accounts/models.py
# from django.contrib.auth.models import AbstractUser
# from django.db import models

# class User(AbstractUser):
#     ROLE_FARMER = "farmer"
#     ROLE_DEALER = "dealer"
#     ROLE_ADMIN = "admin"
#     ROLE_CHOICES = [
#         (ROLE_FARMER, "Farmer"),
#         (ROLE_DEALER, "Dealer"),
#         (ROLE_ADMIN, "Admin"),
#     ]

#     role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_FARMER)
#     phone = models.CharField(max_length=30, blank=True, null=True)
    # add more fields if needed

    # def __str__(self):
    #     return self.username

from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class User(AbstractUser):
    # add custom fields here if you have any (e.g. role, phone_number, etc.)

    groups = models.ManyToManyField(
        Group,
        related_name='accounts_user_set',  # renamed to avoid clash
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='accounts_user_permissions_set',  # renamed to avoid clash
        blank=True
    )

    def __str__(self):
        return self.username
