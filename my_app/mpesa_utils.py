import base64
import json
from decimal import Decimal

import requests
from django.conf import settings
from django.http import JsonResponse


def get_mpesa_access_token():
    api_url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

    # Encode your credentials
    api_credentials = f"{settings.CONSUMER_KEY}:{settings.CONSUMER_SECRET}"
    api_key_secret = base64.b64encode(api_credentials.encode()).decode('utf-8')

    headers = {
        'Authorization': f'Basic {api_key_secret}'
    }

    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        access_token = response.json()['access_token']
        return access_token
    else:
        return None


def initiate_mpesa_payment(phone_number, amount):
    # Convert Decimal to float if amount is a Decimal object
    if isinstance(amount, Decimal):
        amount = float(amount)

    access_token = get_mpesa_access_token()

    if access_token is None:
        return JsonResponse({"message": "Failed to get access token"}, status=500)

    # Prepare the payload for STK Push request
    api_url = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    payload = {
        "BusinessShortCode": settings.SHORTCODE,
        "Password": settings.PASSKEY,
        "Shortcode": settings.SHORTCODE,
        "LipaNaMpesaOnlineShortcode": settings.SHORTCODE,
        "PhoneNumber": phone_number,
        "Amount": amount,
        "AccountReference": "Donation",
        "TransactionDesc": "Charity Donation",
        "Remarks": "Donation Payment",
        "TransactionType": "PayBill",
        "Initiator": "Test",  # Replace this with your actual initiator name
        "SecurityCredential": "your_security_credential",  # Replace with your security credential
        "RequestCode": "Donation Payment",
        "CallbackURL": settings.CALLBACK_URL
    }

    response = requests.post(api_url, data=json.dumps(payload), headers=headers)

    if response.status_code == 200:
        return JsonResponse({"message": "STK Push request sent successfully!"}, status=200)
    else:
        return JsonResponse({"message": "Failed to initiate payment"}, status=500)
