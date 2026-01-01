import time
import requests
from config import Config
from logger import get_logger

class TelegramService:
    def __init__(self):
        self.BOT_TOKEN = Config.BOT_TOKEN
        self.CHAT_ID = Config.CHAT_ID
        self.API_URL = f"https://api.telegram.org/bot{self.BOT_TOKEN}/sendMessage"
        self.logger = get_logger(__name__)

    def send_message(self, message: str) -> bool:
        payload = {
            'chat_id': self.CHAT_ID,
            'text': message,
            'parse_mode': 'HTML'
        }

        for attempt in range(3):
            try:
                r = requests.post(self.API_URL, data=payload, timeout=20)

                if r.ok:
                    self.logger.info("Message sent successfully")
                    return True
                elif r.status_code == 429:
                    retry_after = int(r.json().get('parameters', {}).get('retry_after', 5))
                    self.logger.warning(f"Rate limited by Telegram API. Retrying after {retry_after} seconds.")
                    time.sleep(retry_after + 1)
                    continue
                else:
                    self.logger.error(f"Telegram API error: {r.status_code} {r.text}")
                    return False

            except Exception as e:
                self.logger.error(f"Failed to send message to Telegram (attempt {attempt+1}/3): {e}")
                time.sleep(2)

        self.logger.error("Failed to send message after 3 attempts")
        return False
