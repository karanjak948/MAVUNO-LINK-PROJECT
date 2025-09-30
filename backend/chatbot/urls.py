from django.urls import path
from . import views

urlpatterns = [
    path("", views.chatbot_page, name="chatbot_home"),          
    path("get-response/", views.get_response, name="chatbot_get_response"),
    path("health/", views.health_check, name="chatbot_health"),
]
