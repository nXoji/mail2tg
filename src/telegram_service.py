import re
import html
import time
import requests
from config import Config
from logger import get_logger

class TelegramService:
    def __init__(self):
        self.BOT_TOKEN = Config.BOT_TOKEN
        self.CHAT_ID = Config.CHAT_ID
        self.API_URL = f"https://api.telegram.org/bot{self.BOT_TOKEN}"
        self.logger = get_logger(__name__)

    def send_message(self, message: str, parse_mode: str = 'HTML') -> bool:
        url = f"{self.API_URL}/sendMessage"
        payload = {
            'chat_id': self.CHAT_ID,
            'text': message
        }
        if parse_mode:
            payload['parse_mode'] = parse_mode

        if not self._make_request(url, data=payload):
            if parse_mode:
                self.logger.warning("Failed sending message with HTML, falling back to plain text")
                plain_text = html.unescape(re.sub(r'<[^>]+>', '', message))
                return self.send_message(plain_text, parse_mode=None)
            return False

        return True

    def send_document(self, filename: str, file_obj) -> bool:
        url = f"{self.API_URL}/sendDocument"
        data = {'chat_id': self.CHAT_ID}
        files = {'document': (filename, file_obj)}
        return self._make_request(url, data=data, files=files, timeout=45)

    def _make_request(self, url: str, data: dict = None, files: dict = None, timeout: int = 20) -> bool:
        method_name = url.split('/')[-1]

        for attempt in range(3):
            try:
                if files:
                    for key, val in files.items():
                        if len(val) > 1 and hasattr(val[1], 'seek'):
                            val[1].seek(0)

                r = requests.post(url, data=data, files=files, timeout=timeout)
                time.sleep(0.5)

                if r.ok:
                    self.logger.info(f"Telegram API: {method_name} success")
                    return True
                elif r.status_code == 429:
                    retry_after = int(r.json().get('parameters', {}).get('retry_after', 5))
                    self.logger.warning(f"Rate limited by Telegram API ({method_name}). Retrying after {retry_after} seconds.")
                    time.sleep(retry_after + 1)
                    continue
                else:
                    self.logger.error(f"Telegram API error ({method_name}): {r.status_code} {r.text}")
                    return False

            except Exception as e:
                self.logger.error(f"Unexpected error in {method_name} (attempt {attempt+1}/3): {e}")
                time.sleep(2)

        self.logger.error(f"Failed to execute {method_name} after 3 attempts")
        return False
