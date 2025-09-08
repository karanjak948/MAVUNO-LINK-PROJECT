from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from decimal import Decimal

User = get_user_model()


# -----------------------------
# Profile Dashboard + Barcode Verification + Buy Now
# -----------------------------
@login_required
def profile(request):
    from orders.models import Order, CartItem
    from products.models import Product
    from verification.models import VerifiedProduct

    verification_result = None
    verified_item = None

    # Handle barcode verification
    if request.method == 'POST' and 'barcode' in request.POST:
        code = request.POST.get('barcode', '').strip()
        if code:
            vp = VerifiedProduct.objects.filter(barcode=code).select_related('product').first()
            if vp:
                verified_item = vp
                if vp.is_authentic:
                    verification_result = {
                        'status': 'success',
                        'product': vp.product,
                        'message': f"✅ Verified: {vp.product.name} is authentic."
                    }
                else:
                    verification_result = {
                        'status': 'danger',
                        'message': f"⚠️ Alert: {vp.product.name} failed verification (Fake product)."
                    }
            else:
                verification_result = {
                    'status': 'warning',
                    'message': '❌ No matching product found for that barcode.'
                }

    # Handle "Buy Now" for verified products
    if request.method == 'POST' and 'buy_now' in request.POST:
        product_id = request.POST.get('product_id')
        vp = VerifiedProduct.objects.filter(product_id=product_id).first()

        if not vp:
            messages.error(request, "❌ This product is not registered for verification.")
            return redirect('profile')

        if not vp.is_authentic:
            messages.error(request, f"⚠️ {vp.product.name} is FAKE and cannot be purchased.")
            return redirect('profile')

        # Product is authentic → create order
        with transaction.atomic():
            Order.objects.create(
                customer=request.user,
                product=vp.product,
                quantity=1,
                total_price=vp.product.price,
                status='pending'
            )
        messages.success(request, f"✅ {vp.product.name} added to your orders.")
        return redirect('profile')

    # Load cart items
    cart_items = []
    cart_total = Decimal('0.00')
    try:
        qs = CartItem.objects.filter(user=request.user).select_related('product')
        for ci in qs:
            product = ci.product
            qty = ci.quantity or 1
            line_total = (product.price or Decimal('0.00')) * qty
            cart_items.append({'product': product, 'quantity': qty, 'total_price': line_total})
            cart_total += line_total
    except Exception:
        pass

    context = {
        'cart_items': cart_items,
        'cart_total': cart_total,
        'verification_result': verification_result,
        'verified_item': verified_item
    }
    return render(request, 'accounts/profile.html', context)


# -----------------------------
# Auth Pages
# -----------------------------
def register_user(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')

        if not username:
            messages.error(request, 'Username is required.')
            return redirect('register_user')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('register_user')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
            return redirect('register_user')

        User.objects.create_user(username=username, password=password)
        messages.success(request, 'Account created successfully! Please log in.')
        return redirect('login_user')

    return render(request, 'accounts/register.html')


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, 'Logged in successfully.')
            return redirect('profile')
        messages.error(request, 'Invalid username or password.')
        return redirect('login_user')
    return render(request, 'accounts/login.html')


def logout_user(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login_user')


# -----------------------------
# Optional: Standalone Verification Page
# -----------------------------
@login_required
def verify_product_page(request):
    from verification.models import VerifiedProduct
    verified_item = None
    verification_result = None

    if request.method == 'POST' and 'barcode' in request.POST:
        code = request.POST.get('barcode', '').strip()
        if code:
            vp = VerifiedProduct.objects.filter(barcode=code).select_related('product').first()
            if vp:
                verified_item = vp
                if vp.is_authentic:
                    verification_result = {
                        'status': 'success',
                        'product': vp.product,
                        'message': f"✅ {vp.product.name} is authentic."
                    }
                else:
                    verification_result = {
                        'status': 'danger',
                        'message': f"⚠️ {vp.product.name} is FAKE and cannot be purchased."
                    }
            else:
                verification_result = {
                    'status': 'warning',
                    'message': '❌ No matching product found.'
                }

    return render(request, 'accounts/verify.html', {
        'verification_result': verification_result,
        'verified_item': verified_item
    })
