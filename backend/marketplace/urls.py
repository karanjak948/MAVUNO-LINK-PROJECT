from django.urls import path
from . import views

urlpatterns = [
    path('', views.marketplace_home, name='marketplace_home'),
    path('dealers/', views.dealer_list, name='dealers'),           
]
