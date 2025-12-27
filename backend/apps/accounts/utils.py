import requests
from django.conf import settings
import os

def send_otp_sms(phone_number, otp):
    """
    Send OTP via SMS Provider.
    Toggle providers by setting SMS_PROVIDER in .env
    """
    provider = os.environ.get('SMS_PROVIDER', 'console') # Default to console (mock)
    print(f"\n[SMS DEBUG] Configured Provider: {provider}")

    success = False
    if provider == 'twilio':
        success = send_via_twilio(phone_number, otp)
    elif provider == 'fast2sms':
        success = send_via_fast2sms(phone_number, otp)
    else:
        # Mock for Local Development
        print(f"\n[MOCK SMS] To: {phone_number} | Code: {otp}\n")
        return True
        
    # If API failed but we are in DEBUG, print it so dev can still login
    if not success and settings.DEBUG:
        print(f"\n[DEBUG FALLBACK] SMS Failed (Check Creds). Mock OTP: {otp}\n")
        return True # Pretend success for dev flow
        
    return success

def send_via_twilio(phone_number, otp):
    """
    Send via Twilio
    Requires: TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER
    """
    account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
    auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
    from_number = os.environ.get('TWILIO_PHONE_NUMBER')

    if not all([account_sid, auth_token, from_number]):
        print("Error: Missing Twilio Credentials")
        return False

    url = f"https://api.twilio.com/2010-04-01/Accounts/{account_sid}/Messages.json"
    data = {
        "From": from_number,
        "To": phone_number,
        "Body": f"Your Prime Optical Login OTP is {otp}. Valid for 5 minutes."
    }
    
    try:
        response = requests.post(url, data=data, auth=(account_sid, auth_token))
        return response.status_code in [200, 201]
    except Exception as e:
        print(f"Twilio Error: {e}")
        return False

def send_via_fast2sms(phone_number, otp):
    """
    Send via Fast2SMS (India)
    Requires: FAST2SMS_API_KEY
    """
    api_key = os.environ.get('FAST2SMS_API_KEY')
    print(f"[SMS DEBUG] Fast2SMS Key Loaded? {'Yes' if api_key and 'replace' not in api_key else 'NO (Placeholder detected!)'}")
    
    if not api_key:
        print("Error: Missing Fast2SMS API Key")
        return False
        
    url = "https://www.fast2sms.com/dev/bulkV2"
    payload = {
        "route": "otp",
        "variables_values": otp,
        "numbers": phone_number,
    }
    headers = {
        "authorization": api_key,
        "Content-Type": "application/json"
    }
    
    try:
        print(f"[SMS DEBUG] Sending request to Fast2SMS for {phone_number}...")
        response = requests.post(url, json=payload, headers=headers)
        print(f"[SMS DEBUG] Fast2SMS Response: {response.status_code} - {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"Fast2SMS Error: {e}")
        return False
