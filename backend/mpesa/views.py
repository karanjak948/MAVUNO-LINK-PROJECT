import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from orders.models import Order

@csrf_exempt
def mpesa_callback(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        print("📩 CALLBACK:", json.dumps(data, indent=4))

        stk_callback = data.get("Body", {}).get("stkCallback", {})
        result_code = stk_callback.get("ResultCode")
        checkout_request_id = stk_callback.get("CheckoutRequestID")

        if not checkout_request_id:
            return JsonResponse({"ResultCode": 1, "ResultDesc": "Missing CheckoutRequestID"})

        if result_code == 0:  # ✅ SUCCESS
            metadata = stk_callback.get("CallbackMetadata", {}).get("Item", [])
            mpesa_receipt = None
            amount = None

            for item in metadata:
                if item["Name"] == "MpesaReceiptNumber":
                    mpesa_receipt = item["Value"]
                elif item["Name"] == "Amount":
                    amount = item["Value"]

            # ✅ Update order in DB
            Order.objects.filter(checkout_request_id=checkout_request_id).update(
                status="paid",
                transaction_id=mpesa_receipt,
                is_paid=True,
                amount=amount
            )

            print("✅ Order updated to PAID")
            return JsonResponse({"ResultCode": 0, "ResultDesc": "Processed successfully"})

        else:
            # ❌ Failed transaction
            Order.objects.filter(checkout_request_id=checkout_request_id).update(
                status="failed"
            )
            return JsonResponse({"ResultCode": 0, "ResultDesc": "Transaction failed"})

    except Exception as e:
        print("⚠️ Callback Error:", e)
        return JsonResponse({"ResultCode": 1, "ResultDesc": "Callback error"})
