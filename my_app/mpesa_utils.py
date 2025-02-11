import requests
from requests.auth import HTTPBasicAuth
import datetime
import base64
import json

# M-Pesa API Credentials (Get these from Safaricom Developer Portal)
CONSUMER_KEY = "your_consumer_key"
CONSUMER_SECRET = "your_consumer_secret"
SHORTCODE = "174379"  # Use M-Pesa Test Shortcode or your Business Shortcode
PASSKEY = "your_passkey"
CALLBACK_URL = "https://de77-102-212-236-130.ngrok-free.app"

# Your Personal M-Pesa Phone Number (Donations will be sent here)
RECEIVING_PHONE_NUMBER = "2547XXXXXXXX"  # Replace with your Safaricom number


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

    stk_payload = {
        "BusinessShortCode": SHORTCODE,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": donor_phone,  # Donor's phone number
        "PartyB": SHORTCODE,  # Your M-Pesa business number or test shortcode
        "PhoneNumber": donor_phone,  # The donor’s phone number
        "CallBackURL": CALLBACK_URL,
        "AccountReference": "DeafCommunityDonation",
        "TransactionDesc": "Donation for Deaf Community"
    }

    stk_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    response = requests.post(stk_url, json=stk_payload, headers=headers)

    return response.json()


