from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from products.models import Product
from orders.models import Order, OrderItem
from .models import VerifiedProduct


def verify_home(request):
    """Landing page for verification section"""
    return render(request, "verification/verify_home.html")


@login_required
def verify_and_add_to_cart(request):
    """
    Verify product using barcode and add to cart if authentic
    """
    if request.method == "POST":
        barcode = request.POST.get("barcode")

        try:
            verified_product = VerifiedProduct.objects.get(barcode=barcode)
        except VerifiedProduct.DoesNotExist:
            messages.error(request, "❌ Product not found in verification database.")
            return redirect("verify_product_page")  # fix redirect target

        if not verified_product.is_authentic:
            messages.error(request, "⚠️ This product is FAKE and cannot be purchased.")
            return redirect("verify_product_page")  # fix redirect target

        # Product is authentic → add to cart
        product = verified_product.product
        order, _ = Order.objects.get_or_create(user=request.user, is_paid=False)

        order_item, created = OrderItem.objects.get_or_create(
            order=order,
            product=product,
            defaults={"quantity": 1, "price": product.price},
        )
        if not created:
            order_item.quantity += 1
            order_item.save()

        messages.success(
            request,
            f"✅ {product.name} verified and added to your cart successfully."
        )
        return redirect("order-list")

    return render(request, "verification/verify_form.html")  # use verify_form.html for input page
