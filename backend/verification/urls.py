from django.urls import path
from . import views

urlpatterns = [
    path('', views.verify_home, name='verify_home'),  # Home page for verification
    path('scan/', views.verify_and_add_to_cart, name='verify_product_page'),  # Barcode scan + add to cart
    path("check/", views.verify_and_add_to_cart, name="verify_form"),  # restore verify_form
    path("result/", views.verify_home, name="verify_result"),
]
