from django.urls import path
from . import views

urlpatterns = [
    # Orders
    path('', views.order_list, name='order-list'),

    # Cart
    path('cart/', views.cart_detail, name='cart-detail'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add-to-cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove-from-cart'),

    # Checkout
    path('checkout/', views.checkout, name='checkout'),
    path('checkout/<int:cart_id>/', views.checkout, name='checkout-with-id'),

    # Mpesa
    path('mpesa/callback/', views.mpesa_callback, name='mpesa_callback'),
]
