from os import getenv
from dotenv import load_dotenv

load_dotenv()

class Config:
    # imap configuration
    IMAP_SERVER = getenv('IMAP_SERVER')
    IMAP_PORT = int(getenv('IMAP_PORT', 993))
    EMAIL_ADDRESS = getenv('EMAIL_ADDRESS')
    APP_PASSWORD = getenv('EMAIL_APP_PASSWORD')

    # telegram bot configuration
    BOT_TOKEN = getenv('TELEGRAM_BOT_TOKEN')
    CHAT_ID = getenv('TELEGRAM_CHAT_ID')

    # email check interval in seconds
    CHECK_INTERVAL = int(getenv('CHECK_INTERVAL', 60))
