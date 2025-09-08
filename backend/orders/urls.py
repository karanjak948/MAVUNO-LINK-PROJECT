from django.urls import path
from . import views

urlpatterns = [
    # View all orders for the logged-in user
    path('', views.order_list, name='order-list'),

    # Add product to cart (authentic-only)
    path('add/<int:product_id>/', views.add_to_cart, name='add-to-cart'),

    # Checkout page
    path('checkout/', views.checkout, name='checkout'),
]
