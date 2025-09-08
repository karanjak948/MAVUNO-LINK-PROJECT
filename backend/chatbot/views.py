from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Optional: If you want Django's built-in CSRF protection with AJAX, remove @csrf_exempt
@csrf_exempt
def chatbot_api(request):
    """
    Handles chatbot POST requests.
    """
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_message = data.get("message", "").strip()

            if not user_message:
                return JsonResponse({"response": "Please type something."}, status=400)

            # --- Chatbot logic here ---
            # For now, just echo the message
            bot_reply = f"You said: {user_message}"
            # --------------------------

            return JsonResponse({"response": bot_reply})
        except json.JSONDecodeError:
            return JsonResponse({"response": "Invalid request format."}, status=400)

    return JsonResponse({"response": "Invalid request method."}, status=405)


def chatbot_home(request):
    """
    Simple health check for chatbot API.
    """
    return JsonResponse({"message": "Chatbot API is working"})
