import requests
from config import Config

class TelegramService:
    def __init__(self):
        self.BOT_TOKEN = Config.BOT_TOKEN
        self.CHAT_ID = Config.CHAT_ID
        self.API_URL = f"https://api.telegram.org/bot{self.BOT_TOKEN}/sendMessage"

    def send_message(self, message: str) -> bool:
        payload = {
            'chat_id': self.CHAT_ID,
            'text': message,
            'parse_mode': 'HTML'
        }

        try:
            r = requests.post(self.API_URL, data=payload, timeout=20)
            if r.ok:
                return True
            else:
                print(f"Telegram API error: {r.status_code} {r.text}")
                return False
        except Exception as e:
            print(f"Failed to send message to Telegram: {e}")
            return False
