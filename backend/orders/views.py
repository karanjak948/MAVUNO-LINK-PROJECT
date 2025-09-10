from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from .models import Cart, CartItem, Order, OrderItem
from products.models import Product
from verification.models import VerifiedProduct


@login_required
def order_list(request):
    """
    Show all orders for the logged-in user.
    """
    orders = Order.objects.filter(customer=request.user).prefetch_related("items__product")
    return render(request, "orders/order_list.html", {"orders": orders})


@login_required
@transaction.atomic
def add_to_cart(request, product_id):
    """
    Adds a product to the cart only if verified & authentic.
    Triggered from marketplace 'Add to Cart' button (POST form).
    """
    if request.method != "POST":
        messages.error(request, "Invalid request.")
        return redirect("marketplace")

    product = get_object_or_404(Product, id=product_id)

    # ✅ Ensure product is authentic
    vp = VerifiedProduct.objects.filter(product=product, is_authentic=True).first()
    if not vp:
        messages.error(request, f"❌ {product.name} is not authentic and cannot be added to cart.")
        return redirect("marketplace")

    # ✅ Quantity (default = 1)
    try:
        qty = int(request.POST.get("quantity", 1))
        if qty < 1:
            qty = 1
    except Exception:
        qty = 1

    # ✅ Get or create user cart
    cart, _ = Cart.objects.get_or_create(user=request.user)

    # ✅ Add or update cart item
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if created:
        cart_item.quantity = qty
    else:
        cart_item.quantity += qty
    cart_item.save()

    messages.success(request, f"✅ {product.name} added to your cart (x{cart_item.quantity}).")
    return redirect("cart-detail")


@login_required
def cart_detail(request):
    """
    Display cart details with items, quantities, and totals.
    """
    cart, _ = Cart.objects.get_or_create(user=request.user)
    return render(request, "orders/cart_detail.html", {"cart": cart})


@login_required
def remove_from_cart(request, item_id):
    """
    Remove an item from the cart.
    """
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    item.delete()
    messages.success(request, "🗑️ Item removed from cart.")
    return redirect("cart-detail")


@login_required
@transaction.atomic
def checkout(request):
    """
    Convert cart items into an order with order items.
    """
    cart = Cart.objects.filter(user=request.user).first()
    if not cart or not cart.items.exists():
        messages.warning(request, "Your cart is empty.")
        return redirect("cart-detail")

    # ✅ Create new order
    order = Order.objects.create(customer=request.user, status="pending")

    for ci in cart.items.all():
        # Double-check authenticity
        vp = VerifiedProduct.objects.filter(product=ci.product, is_authentic=True).first()
        if not vp:
            messages.error(request, f"❌ {ci.product.name} failed authenticity check. Skipped.")
            continue

        OrderItem.objects.create(
            order=order,
            product=ci.product,
            quantity=ci.quantity,
            price=ci.product.price,
        )

    # ✅ Clear cart after checkout
    cart.items.all().delete()

    messages.success(request, f"✅ Checkout complete. Order #{order.id} placed!")
    return redirect("order-list")
