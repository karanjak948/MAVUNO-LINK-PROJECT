from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_reviews, name='reviews_home'),
]
