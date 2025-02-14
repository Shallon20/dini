import requests
from decouple import config
from requests.auth import HTTPBasicAuth
import datetime
import base64
import json

# M-Pesa API Credentials (Get these from Safaricom Developer Portal)
CONSUMER_KEY = config('CONSUMER_KEY')
CONSUMER_SECRET = config('CONSUMER_SECRET')
SHORTCODE = config('SHORTCODE')
PASSKEY = config('PASSKEY')
CALLBACK_URL = "https://de77-102-212-236-130.ngrok-free.app"
RECEIVING_PHONE_NUMBER = config('RECEIVING_PHONE_NUMBER')


def generate_access_token():
    """Generate M-Pesa access token"""
    auth_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    response = requests.get(auth_url, auth=HTTPBasicAuth(CONSUMER_KEY, CONSUMER_SECRET))
    return response.json()["access_token"]


def stk_push_request(amount, donor_phone):
    """Send STK Push request to donor's phone"""
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    password = base64.b64encode((SHORTCODE + PASSKEY + timestamp).encode()).decode()

    access_token = generate_access_token()
    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}

    amount = int(amount)

    stk_payload = {
        "BusinessShortCode": SHORTCODE,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": donor_phone,
        "PartyB": SHORTCODE,
        "PhoneNumber": donor_phone,  # The donor’s phone number
        "CallBackURL": CALLBACK_URL,
        "AccountReference": "DINIDONATION",
        "TransactionDesc": "Donation for Deaf Community"
    }

    stk_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    response = requests.post(stk_url, json=stk_payload, headers=headers)

    return response.json()


