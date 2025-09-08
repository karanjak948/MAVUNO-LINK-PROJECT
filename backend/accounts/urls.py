# accounts/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Auth URLs
    path('register/', views.register_user, name='register_user'),
    path('login/', views.login_user, name='login_user'),
    path('logout/', views.logout_user, name='logout_user'),

    # Profile Dashboard
    path('profile/', views.profile, name='profile'),

    # Standalone Barcode Verification Page
    path('verify/', views.verify_product_page, name='verify_product'),
]
