from django.urls import path
from . import views

urlpatterns = [
    path('', views.chatbot_home, name='chatbot_home'),  # Health check
    path('api/', views.chatbot_api, name='chatbot_api'), # Main API endpoint
]