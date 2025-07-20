
import os
import requests
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

BOT_TOKEN = os.getenv("7563160151:AAF72BsGSr8npVv98xKbDc8ePqPQ3eT2O8M")  # Store in .env file
CHAT_ID = os.getenv("-4242370427")      # Store in .env file
OTP_API = os.getenv("http://51.89.99.105/NumberPanel/agent/res/data_smscdr.php?fdate1=2025-07-20%2000:00:00&fdate2=2025-07-20%2023:59:59&frange=&fclient=&fnum=&fcli=&fgdate=&fgmonth=&fgrange=&fgclient=&fgnumber=&fgcli=&fg=0&sEcho=1&iColumns=9&sColumns=%2C%2C%2C%2C%2C%2C%2C%2C&iDisplayStart=0&iDisplayLength=25&mDataProp_0=0&sSearch_0=&bRegex_0=false&bSearchable_0=true&bSortable_0=true&mDataProp_1=1&sSearch_1=&bRegex_1=false&bSearchable_1=true&bSortable_1=true&mDataProp_2=2&sSearch_2=&bRegex_2=false&bSearchable_2=true&bSortable_2=true&mDataProp_3=3&sSearch_3=&bRegex_3=false&bSearchable_3=true&bSortable_3=true&mDataProp_4=4&sSearch_4=&bRegex_4=false&bSearchable_4=true&bSortable_4=true&mDataProp_5=5&sSearch_5=&bRegex_5=false&bSearchable_5=true&bSortable_5=true&mDataProp_6=6&sSearch_6=&bRegex_6=false&bSearchable_6=true&bSortable_6=true&mDataProp_7=7&sSearch_7=&bRegex_7=false&bSearchable_7=true&bSortable_7=true&mDataProp_8=8&sSearch_8=&bRegex_8=false&bSearchable_8=true&bSortable_8=false&sSearch=&bRegex=false&iSortCol_0=0&sSortDir_0=desc&iSortingCols=1&_=1753047892231")      # Store in .env file

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

    message = f""" # OTP HUB #
    Time: {otp_data['time']}
    Number: {otp_data['number']}
    Service: {otp_data['service']}
    OTP Code: {otp_data['code']}
    Bot by: @mr_lmoment06"""

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

# Run every 1 seconds
while True:
    otp = fetch_otp()
    if otp:
        send_to_telegram(otp)
    time.sleep(1)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)  # Correct for Render
