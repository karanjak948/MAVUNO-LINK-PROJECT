from django.urls import path
from . import views

urlpatterns = [
    path('', views.review_list, name="review_list"),  # shows all reviews
    path('add/', views.add_review, name="add_review"),  # general add review
    path('product/<int:product_id>/add/', views.add_product_review, name="add_product_review"),
    path('dealer/<int:dealer_id>/add/', views.add_dealer_review, name="add_dealer_review"),
]


