import base64
from datetime import datetime, timedelta
import logging
import requests
from requests.auth import HTTPBasicAuth
from django.conf import settings

logger = logging.getLogger(__name__)

_token_cache = {"token": None, "expires_at": None}

def _base_url():
    return "https://sandbox.safaricom.co.ke" if settings.MPESA_ENV == "sandbox" else "https://api.safaricom.co.ke"

def get_mpesa_token():
    now = datetime.utcnow()
    if _token_cache["token"] and _token_cache["expires_at"] and now < _token_cache["expires_at"]:
        return _token_cache["token"]

    url = f"{_base_url()}/oauth/v1/generate?grant_type=client_credentials"
    resp = requests.get(url, auth=HTTPBasicAuth(settings.MPESA_CONSUMER_KEY, settings.MPESA_CONSUMER_SECRET), timeout=10)
    resp.raise_for_status()
    data = resp.json()
    token = data.get("access_token")
    _token_cache["token"] = token
    _token_cache["expires_at"] = now + timedelta(seconds=3500)
    return token

def initiate_stk_push(phone_number: str, amount: int, account_reference: str, transaction_desc="MavunoLink Purchase"):
    """
    Initiate STK Push. amount must be an integer (Ksh).
    Returns: dict with keys 'ok' (bool), 'response' (raw response), 'MerchantRequestID', 'CheckoutRequestID'
    """
    token = get_mpesa_token()
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    passwd_raw = settings.MPESA_SHORTCODE + settings.MPESA_PASSKEY + timestamp
    password = base64.b64encode(passwd_raw.encode()).decode()

    # ✅ Updated callback to your ngrok tunnel
    callback_url = "https://e50ea3b90fe9.ngrok-free.app/api/mpesa/callback/"

    payload = {
        "BusinessShortCode": settings.MPESA_SHORTCODE,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": int(amount),
        "PartyA": phone_number,
        "PartyB": settings.MPESA_SHORTCODE,
        "PhoneNumber": phone_number,
        "CallBackURL": callback_url,  # 🔗 your live ngrok callback
        "AccountReference": account_reference,
        "TransactionDesc": transaction_desc,
    }

    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    url = f"{_base_url()}/mpesa/stkpush/v1/processrequest"
    resp = requests.post(url, json=payload, headers=headers, timeout=15)
    resp.raise_for_status()
    data = resp.json()
    return {
        "ok": True,
        "response": data,
        "MerchantRequestID": data.get("MerchantRequestID"),
        "CheckoutRequestID": data.get("CheckoutRequestID"),
    }
