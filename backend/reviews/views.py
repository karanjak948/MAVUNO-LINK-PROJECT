from django.http import JsonResponse
from .models import ProductReview

def list_reviews(request):
    qs = ProductReview.objects.all()
    data = [{"product": r.product.name, "rating": r.rating, "comment": r.comment} for r in qs]
    return JsonResponse(data, safe=False)
