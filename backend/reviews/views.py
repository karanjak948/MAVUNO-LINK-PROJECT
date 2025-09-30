from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Review, Dealer
from products.models import Product
from .forms import ReviewForm


def review_list(request):
    """List all reviews (optimized)."""
    reviews = Review.objects.select_related("reviewer", "product", "dealer").order_by("-created_at")
    return render(request, "reviews/review_list.html", {"reviews": reviews})


@login_required
def add_review(request):
    """
    General add review page.
    - If using ReviewForm -> normal form submission.
    - If using custom POST -> handle product/dealer selection manually.
    """
    products = Product.objects.all()
    dealers = Dealer.objects.all()

    if request.method == "POST":
        # Try form first
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.reviewer = request.user
            review.save()
            return redirect("review_list")

        # If not form, fallback to manual
        review_type = request.POST.get("type")  # 'product' or 'dealer'
        rating = int(request.POST.get("rating", 1))
        comment = request.POST.get("comment", "")

        if review_type == "product":
            product_id = int(request.POST.get("product_id"))
            product = get_object_or_404(Product, id=product_id)
            Review.objects.create(
                reviewer=request.user,
                product=product,
                rating=rating,
                comment=comment
            )
            return redirect("review_list")

        elif review_type == "dealer":
            dealer_id = int(request.POST.get("dealer_id"))
            dealer = get_object_or_404(Dealer, id=dealer_id)
            Review.objects.create(
                reviewer=request.user,
                dealer=dealer,
                rating=rating,
                comment=comment
            )
            return redirect("review_list")

    else:
        form = ReviewForm()

    return render(
        request,
        "reviews/add_review.html",
        {"form": form, "products": products, "dealers": dealers}
    )


@login_required
def add_product_review(request, product_id):
    """Directly add a review for a specific product."""
    product = get_object_or_404(Product, id=product_id)
    if request.method == "POST":
        rating = int(request.POST.get("rating", 1))
        comment = request.POST.get("comment", "")
        Review.objects.create(
            reviewer=request.user,
            product=product,
            rating=rating,
            comment=comment
        )
        return redirect("review_list")
    return render(request, "reviews/add_review.html", {"product": product})


@login_required
def add_dealer_review(request, dealer_id):
    """Directly add a review for a specific dealer."""
    dealer = get_object_or_404(Dealer, id=dealer_id)
    if request.method == "POST":
        rating = int(request.POST.get("rating", 1))
        comment = request.POST.get("comment", "")
        Review.objects.create(
            reviewer=request.user,
            dealer=dealer,
            rating=rating,
            comment=comment
        )
        return redirect("review_list")
    return render(request, "reviews/add_review.html", {"dealer": dealer})
