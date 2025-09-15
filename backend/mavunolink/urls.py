

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core.views import home

urlpatterns = [
    path('', home, name='home'),   # Home page
    path('admin/', admin.site.urls),

    # Products
    path('products/', include('products.urls')),

    # Accounts
    path('accounts/', include('accounts.urls')),

    # Products
    path('products/', include('products.urls')),

    # Marketplace (main entry + dealers inside it)
    path('marketplace/', include('marketplace.urls')),

    # Chatbot
    path('chatbot/', include('chatbot.urls')),

    # Verification
    path('verify/', include('verification.urls')),

    # Reviews
    path('reviews/', include('reviews.urls')),

    # Orders
    path('orders/', include('orders.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
