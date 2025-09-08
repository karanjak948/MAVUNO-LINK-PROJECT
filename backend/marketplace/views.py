from django.shortcuts import render
from django.http import JsonResponse
from .models import Dealer

def dealer_list(request):
    """Return a JSON list of all dealers"""
    qs = Dealer.objects.all()
    data = [
        {
            "name": d.name,
            "email": d.email,
            "phone": d.phone,
            "address": d.address,
        }
        for d in qs
    ]
    return JsonResponse(data, safe=False)

def marketplace_home(request):
    """Render marketplace main page with products"""
    # You might later want to fetch products from DB
    return render(request, "marketplace/marketplace.html", {"products": []})
