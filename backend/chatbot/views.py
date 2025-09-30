import os, json, random, logging
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.shortcuts import render
from django.conf import settings
from openai import OpenAI

from .models import ConversationLog
from products.models import Product

logger = logging.getLogger(__name__)

# ✅ Optional import
try:
    from verification.models import VerifiedProduct
except Exception:
    VerifiedProduct = None

# ✅ OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ✅ Load intents
INTENTS_PATH = os.path.join(settings.BASE_DIR, "chatbot", "intents.json")
try:
    with open(INTENTS_PATH, "r", encoding="utf-8") as f:
        INTENTS = json.load(f)
except Exception as e:
    logger.warning(f"Could not load intents.json: {e}")
    INTENTS = []


# -------------------------------
# Page renderer
# -------------------------------
def chatbot_page(request):
    """Render the chatbot UI"""
    return render(request, "chatbot/chat.html")


# -------------------------------
# Intent helper
# -------------------------------
def find_intent_by_examples(msg):
    low = msg.lower()
    for intent in INTENTS:
        for ex in intent.get("examples", []):
            if ex.lower().strip() in low:
                return intent
    return None


# -------------------------------
# Main chatbot response
# -------------------------------
@csrf_exempt          # ✅ TEMP for testing, avoids CSRF failure
@require_POST
def get_response(request):
    try:
        payload = json.loads(request.body.decode("utf-8"))
    except Exception:
        return HttpResponseBadRequest("Invalid JSON body.")

    message = (payload.get("message") or "").strip()
    if not message:
        return JsonResponse({"response": "Please type something to ask."})

    user = request.user if request.user.is_authenticated else None

    # 1️⃣ Barcode check
    if VerifiedProduct and message.isdigit() and len(message) >= 6:
        try:
            vp = VerifiedProduct.objects.get(barcode=message)
            resp = f"{vp.product.name} — {'Authentic ✅' if vp.is_authentic else 'Fake ❌'}"
            ConversationLog.objects.create(user=user, user_message=message, bot_response=resp)
            return JsonResponse({"response": resp})
        except VerifiedProduct.DoesNotExist:
            pass

    # 2️⃣ Product check
    products = Product.objects.filter(name__icontains=message)
    if products.exists():
        p = products.first()
        resp = f"{p.name}\nPrice: KSh {p.price}\nStock: {p.stock}\nSeller: {p.seller}"
        ConversationLog.objects.create(user=user, user_message=message, bot_response=resp)
        return JsonResponse({"response": resp})

    # 3️⃣ Intent check
    intent = find_intent_by_examples(message)
    if intent:
        resp = random.choice(intent.get("responses", [])) or "I am not sure how to answer that."
        ConversationLog.objects.create(user=user, user_message=message, bot_response=resp)
        return JsonResponse({"response": resp})

    # 4️⃣ OpenAI fallback
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant for farmers in Kenya."},
                {"role": "user", "content": message}
            ],
            max_tokens=200,
            temperature=0.7
        )
        ai_resp = response.choices[0].message.content.strip()
    except Exception as e:
        ai_resp = f"⚠️ Error contacting AI service: {str(e)}"

    ConversationLog.objects.create(user=user, user_message=message, bot_response=ai_resp)
    return JsonResponse({"response": ai_resp})


# -------------------------------
# Health check
# -------------------------------
def health_check(request):
    return JsonResponse({"status": "ok"})
