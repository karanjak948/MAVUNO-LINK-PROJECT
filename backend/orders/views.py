# orders/views.py
import json
import logging
from decimal import Decimal

from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db import transaction

from .models import Cart, CartItem, Order, OrderItem
from products.models import Product
from verification.models import VerifiedProduct
from utils.mpesa import initiate_stk_push

logger = logging.getLogger(__name__)


def _normalize_phone(phone: str):
    """Normalize phone to 2547XXXXXXXX format."""
    if not phone:
        return None
    phone = phone.strip()
    if phone.startswith("+"):
        phone = phone[1:]
    if phone.startswith("0"):
        phone = "254" + phone[1:]
    return phone


# =========================
# CART VIEWS
# =========================

@login_required
def cart_detail(request):
    """Display cart details with items and totals."""
    cart, _ = Cart.objects.get_or_create(user=request.user)
    return render(request, "orders/cart_detail.html", {"cart": cart})


@login_required
@transaction.atomic
def add_to_cart(request, product_id):
    """Add product to cart (only verified & authentic)."""
    if request.method != "POST":
        messages.error(request, "Invalid request.")
        return redirect("marketplace_home")

    product = get_object_or_404(Product, id=product_id)
    vp = VerifiedProduct.objects.filter(product=product, is_authentic=True).first()
    if not vp:
        messages.error(request, f"❌ {product.name} is not authentic and cannot be added.")
        return redirect("marketplace_home")

    qty = int(request.POST.get("quantity", 1) or 1)
    if qty < 1:
        qty = 1

    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if created:
        cart_item.quantity = qty
    else:
        cart_item.quantity += qty
    cart_item.save()

    messages.success(request, f"✅ {product.name} added to your cart (x{cart_item.quantity}).")
    return redirect("cart-detail")


@login_required
def remove_from_cart(request, item_id):
    """Remove an item from the cart."""
    try:
        item = CartItem.objects.get(id=item_id, cart__user=request.user)
        item.delete()
        messages.success(request, "🗑️ Item removed from cart.")
    except CartItem.DoesNotExist:
        messages.warning(request, "⚠️ That item is no longer in your cart.")
    return redirect("cart-detail")


# =========================
# ORDER VIEWS
# =========================

@login_required
def order_list(request):
    """Show all orders for logged-in user (latest first)."""
    orders = Order.objects.filter(customer=request.user).order_by("-created_at")
    return render(request, "orders/order_list.html", {"orders": orders})


@login_required
@transaction.atomic
def checkout(request, cart_id=None):
    """
    Convert cart items into an order & initiate M-Pesa STK Push.
    If cart_id is given, fetch that cart. Otherwise, use the user's active cart.
    """
    if cart_id:
        cart = get_object_or_404(Cart, id=cart_id, user=request.user)
    else:
        cart = Cart.objects.filter(user=request.user).first()

    if not cart or not cart.items.exists():
        messages.warning(request, "Your cart is empty.")
        return redirect("cart-detail")

    items = list(cart.items.select_related("product").all())

    # ✅ Verify authenticity for all items
    for ci in items:
        vp = VerifiedProduct.objects.filter(product=ci.product, is_authentic=True).first()
        if not vp:
            messages.error(request, f"❌ {ci.product.name} is not authentic. Remove it before checkout.")
            return redirect("cart-detail")

    # ✅ Calculate total
    total = sum((ci.product.price or Decimal("0.00")) * ci.quantity for ci in items)
    total = Decimal(total).quantize(Decimal("1.00"))

    # ✅ Create order & items
    order = Order.objects.create(customer=request.user, status="pending", amount=total)
    for ci in items:
        OrderItem.objects.create(
            order=order,
            product=ci.product,
            quantity=ci.quantity,
            price=ci.product.price,
        )

    # ✅ Clear cart after checkout
    cart.items.all().delete()

    # ✅ Get phone number for M-Pesa
    user = request.user
    phone = getattr(user, "phone_number", None) or getattr(user, "phone", None) or request.POST.get("phone")
    phone = _normalize_phone(phone)
    if not phone:
        messages.error(request, "Please add your phone number to profile (format 2547XXXXXXXX).")
        order.delete()
        return redirect("profile")

    # ✅ Initiate STK push
    try:
        mpesa_resp = initiate_stk_push(phone, int(total), account_reference=f"Order{order.id}")
    except Exception as e:
        logger.exception("M-Pesa STK push failed")
        messages.error(request, f"Failed to initiate M-Pesa: {e}")
        order.status = "failed"
        order.save()
        return redirect("order-list")

    order.merchant_request_id = mpesa_resp.get("MerchantRequestID") or mpesa_resp.get("response", {}).get("MerchantRequestID")
    order.checkout_request_id = mpesa_resp.get("CheckoutRequestID") or mpesa_resp.get("response", {}).get("CheckoutRequestID")
    order.save()

    messages.info(request, "STK Push sent. Approve the prompt on your phone to complete payment.")
    return redirect("order-list")


# =========================
# M-PESA CALLBACK
# =========================

@csrf_exempt
def mpesa_callback(request):
    """
    Daraja will POST here. Parse JSON and update order accordingly.
    """
    try:
        data = json.loads(request.body.decode("utf-8"))
    except Exception:
        return JsonResponse({"ResultCode": 1, "ResultDesc": "Invalid JSON"}, status=400)

    body = data.get("Body", {})
    stk = body.get("stkCallback") or {}
    merchant_req = stk.get("MerchantRequestID")
    checkout_req = stk.get("CheckoutRequestID")
    result_code = stk.get("ResultCode")
    result_desc = stk.get("ResultDesc")

    # ✅ Find order
    order = None
    if merchant_req:
        order = Order.objects.filter(merchant_request_id=merchant_req).first()
    if not order and checkout_req:
        order = Order.objects.filter(checkout_request_id=checkout_req).first()

    # ✅ Extract metadata
    mpesa_receipt = None
    phone = None
    amount = None
    meta_items = stk.get("CallbackMetadata", {}).get("Item", [])
    for item in meta_items:
        name = item.get("Name", "").lower()
        if name == "mpesareceiptnumber":
            mpesa_receipt = item.get("Value")
        if name == "amount":
            amount = item.get("Value")
        if name == "phonenumber":
            phone = item.get("Value")

    if not order:
        logger.warning("Received unmatched M-Pesa callback", extra={"merchant": merchant_req, "checkout": checkout_req})
        return JsonResponse({"ResultCode": 0, "ResultDesc": "No matching order"})

    # ✅ Update order
    if result_code == 0:
        order.is_paid = True
        order.status = "paid"
        order.transaction_id = mpesa_receipt or checkout_req
        order.save()
    else:
        order.is_paid = False
        order.status = "failed"
        order.save()

    return JsonResponse({"ResultCode": 0, "ResultDesc": "Accepted"})
