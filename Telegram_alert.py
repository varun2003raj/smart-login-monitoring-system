
import requests
import urllib3
from config import BOT_TOKEN, CHAT_ID


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BOT_TOKEN = "YOUR_BOT_TOKEN"
CHAT_ID = "YOUR_CHAT_ID"

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": msg
    }

    try:
        response = requests.post(url, data=data, timeout=10, verify=False)
        print("Telegram status:", response.status_code)
    except Exception as e:
        print("Telegram error:", e)
