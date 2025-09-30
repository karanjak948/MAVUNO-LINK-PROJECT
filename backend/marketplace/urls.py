# marketplace/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.marketplace_home, name='marketplace_home'),
    path('product/<int:pk>/', views.product_detail, name='product-detail'),

    # Dealers page (HTML)
    path('dealers/', views.dealers_page, name='dealers'),

    # Dealers API (JSON)
    path('dealers/api/', views.dealers_api, name='dealers_api'),
]
