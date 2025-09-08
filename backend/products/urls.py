from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='list'),          # /products/
    path('upload/', views.upload_product, name='upload'),
    path('verify/<str:barcode>/', views.verify_product, name='verify'),
    path('<int:pk>/', views.product_detail, name='detail'),
]
