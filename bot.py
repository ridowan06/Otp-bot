requests==2.31.0
python-dotenv==1.0.1


import os
import requests
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")  # Store in .env file
CHAT_ID = os.getenv("CHAT_ID")      # Store in .env file
OTP_API = os.getenv("OTP_API")      # Store in .env file

def fetch_otp():
    try:
        response = requests.post(OTP_API)
        response.raise_for_status()
        data = response.json()
        return {
            "time": data.get("timestamp", 'N/A'),
            "number": data.get("number", 'N/A'),
            "service": data.get("service", 'N/A'),
            "code": data.get("otp", 'N/A')
        }
    except Exception as e:
        print(f"Error fetching OTP: {e}")
        return None

def send_to_telegram(otp_data):
    if not otp_data:
        return

    message = f""" # We Are All One #
    Time: {otp_data['time']}
    Number: {otp_data['number']}
    Service: {otp_data['service']}
    OTP Code: {otp_data['code']}
    Bot by: Bmr_lmoment06"""

    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": CHAT_ID,
            "text": message
        }
        response = requests.post(url, data=payload)
        response.raise_for_status()
    except Exception as e:
        print(f"Error sending to Telegram: {e}")

# Run every 5 seconds
while True:
    otp = fetch_otp()
    if otp:
        send_to_telegram(otp)
    time.sleep(5)
