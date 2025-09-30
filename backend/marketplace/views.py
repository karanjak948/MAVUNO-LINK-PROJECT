# marketplace/views.py

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.db.models import Q
from .models import Dealer, Product

def marketplace_home(request):
    """Render marketplace main page with products, search, category filter, and sorting"""
    query = request.GET.get("q", "")
    selected_category = request.GET.get("category", "All")
    sort = request.GET.get("sort", "")

    categories = Product.CATEGORY_CHOICES if hasattr(Product, 'CATEGORY_CHOICES') else []

    products = Product.objects.all()

    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))
    if selected_category != "All":
        products = products.filter(category=selected_category)

    if sort == "price_asc":
        products = products.order_by("price")
    elif sort == "price_desc":
        products = products.order_by("-price")
    elif sort == "latest":
        products = products.order_by("-created_at")
    elif sort == "popular":
        products = products.order_by("-reviews_count")

    return render(request, "marketplace/marketplace.html", {
        "products": products,
        "query": query,
        "selected_category": selected_category,
        "categories": categories,
        "sort": sort,
    })

# marketplace/views.py
def dealers_page(request):
    """Render HTML page listing all dealers"""
    dealers = Dealer.objects.all()
    return render(request, "marketplace/dealers.html", {"dealers": dealers})


def dealers_api(request):
    """Return JSON list of all dealers (API)"""
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

def product_detail(request, pk):
    """Show details for a single product"""
    product = get_object_or_404(Product, pk=pk)
    return render(request, "marketplace/product_detail.html", {"product": product})
