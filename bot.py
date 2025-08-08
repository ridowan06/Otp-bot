import requests
import time
import random
from telegram import Bot

# ==== CONFIGURATION ====
TELEGRAM_BOT_TOKEN = "8439217241:AAGOoK8IHSxGnRIMSxNV7CsCla_-aAdoz8o"
TELEGRAM_CHAT_ID = "-1002229919396"
DUMMY_API_URL = "http://51.89.99.105/NumberPanel/login"  # Simulated SMS API
# ========================

# Simulate country and service for demo
COUNTRIES = ["🇦🇫 Afghanistan", "🇮🇳 India", "🇺🇸 USA", "🇬🇧 UK", "🇫🇷 France"]
SERVICES = ["TWILIO", "WHATSAPP", "TELEGRAM", "FACEBOOK", "INSTAGRAM"]

def generate_random_captcha():
    a = random.randint(1, 20)
    b = random.randint(1, 20)
    op = random.choice(["+", "-", "*", "/"])
    if op == "/":
        a = a * b  # to make division clean
    return f"{a} {op} {b}"

def solve_captcha(expression: str) -> float:
    try:
        return round(eval(expression), 2)
    except:
        return None

def fetch_mock_sms():
    print("[*] Fetching mock SMS...")
    try:
        res = requests.get(DUMMY_API_URL)
        res.raise_for_status()
        return res.json().get("posts", [])[:2]
    except Exception as e:
        print(f"[!] Error fetching SMS: {e}")
        return []

def generate_formatted_message(msg, index):
    now = time.strftime('%Y-%m-%d %I:%M:%S %p')
    number = f"93779{random.randint(1000,9999)}"
    country = random.choice(COUNTRIES)
    service = random.choice(SERVICES)
    otp = "No OTP found" if random.random() > 0.5 else str(random.randint(100000, 999999))

    return f"""
**🔔 {country} {service} Otp Code Received Successfully...**

⏰**Time:** {now}  
📲**Number:** {number}  
🌐**Country:** {country}  
💬**Service:** {service}  
🔐**Otp Code:** {otp}  
📩
"""

def send_to_telegram(messages, captcha_expression, captcha_result):
    bot = Bot(token=TELEGRAM_BOT_TOKEN)

    header = f"""✅ *OTP Bot Executed*
🧠 *Captcha Solved:* `{captcha_expression} = {captcha_result}`
🧾 *Fetched {len(messages)} Messages*
"""
    try:
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=header, parse_mode="Markdown")

        for i, msg in enumerate(messages):
            formatted = generate_formatted_message(msg, i)
            bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=formatted, parse_mode="Markdown")

    except Exception as e:
        print(f"[!] Failed to send message: {e}")

def main():
    print("==== Educational OTP Bot with Styled Message ====")
    try:
        while True:
            captcha = generate_random_captcha()
            result = solve_captcha(captcha)
            if result is None:
                print("[!] Captcha solve failed.")
                continue

            messages = fetch_mock_sms()
            if not messages:
                print("[!] No messages fetched.")
                time.sleep(10)
                continue

            send_to_telegram(messages, captcha, result)
            print("[*] Messages sent. Waiting before next run...\n")
            time.sleep(60)  # Wait for 60 seconds before next run
    except KeyboardInterrupt:
        print("\n[!] Bot stopped by user.")

if __name__ == "__main__":
    main()
