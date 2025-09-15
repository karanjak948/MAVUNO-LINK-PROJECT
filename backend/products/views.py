from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Product
from .forms import ProductForm

def product_list(request):
    products = Product.objects.all()
    return render(request, "products/list.html", {"products": products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, "products/detail.html", {"product": product})

def upload_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("product_list")
    else:
        form = ProductForm()
    return render(request, "products/upload.html", {"form": form})

def verify_product(request, barcode):
    try:
        product = Product.objects.get(barcode=barcode)
        return JsonResponse({"valid": True, "message": f"✅ {product.name} is verified."})
    except Product.DoesNotExist:
        return JsonResponse({"valid": False, "message": "❌ Product not found."})
    
def marketplace(request):
    products = Product.objects.all()
    return render(request, "products/marketplace.html", {"products": products})
