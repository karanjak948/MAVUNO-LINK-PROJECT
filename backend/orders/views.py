from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from .models import CartItem, Order
from products.models import Product
from verification.models import VerifiedProduct


@login_required
def order_list(request):
    """
    Show all orders for the logged-in user.
    """
    orders = Order.objects.filter(customer=request.user).select_related("product")
    return render(request, "orders/order_list.html", {"orders": orders})


@login_required
@transaction.atomic
def add_to_cart(request, product_id):
    """
    Adds a product to the cart only if:
      - The product exists
      - The product is registered in VerifiedProduct
      - The product is marked is_authentic=True
    """
    if request.method != "POST":
        messages.error(request, "Invalid request.")
        return redirect("profile")

    product = get_object_or_404(Product, id=product_id)

    # Check verification
    vp = VerifiedProduct.objects.filter(product=product).first()
    if not vp:
        messages.error(request, f"❌ {product.name} is not verified and cannot be added to cart.")
        return redirect("profile")

    if not vp.is_authentic:
        messages.error(request, f"⚠️ {product.name} is FAKE and cannot be purchased.")
        return redirect("profile")

    # Get quantity (default=1)
    try:
        qty = int(request.POST.get("quantity", 1))
        if qty < 1:
            qty = 1
    except Exception:
        qty = 1

    # Add or update cart item
    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    if created:
        cart_item.quantity = qty
    else:
        cart_item.quantity += qty
    cart_item.save()

    messages.success(request, f"✅ {product.name} added to your cart (x{cart_item.quantity}).")
    return redirect("profile")


@login_required
@transaction.atomic
def checkout(request):
    """
    Moves cart items into Orders (only authentic products).
    """
    cart_items = CartItem.objects.filter(user=request.user).select_related("product")

    if not cart_items.exists():
        messages.warning(request, "Your cart is empty.")
        return redirect("profile")

    for ci in cart_items:
        # Double-check authenticity before confirming order
        vp = VerifiedProduct.objects.filter(product=ci.product, is_authentic=True).first()
        if not vp:
            messages.error(request, f"❌ {ci.product.name} failed authenticity check. Removed from cart.")
            ci.delete()
            continue

        total_price = ci.product.price * ci.quantity
        Order.objects.create(
            customer=request.user,
            product=ci.product,
            quantity=ci.quantity,
            total_price=total_price,
            status="pending",
        )
        ci.delete()

    messages.success(request, "✅ Checkout complete. Your order has been placed!")
    return redirect("order-list")
