from os import getenv
from dotenv import load_dotenv

load_dotenv()

class Config:
    # imap configuration
    IMAP_SERVER = 'imap.gmail.com'
    IMAP_PORT = 993
    EMAIL_ADDRESS = getenv("GMAIL_EMAIL")
    APP_PASSWORD = getenv('GMAIL_APP_PASSWORD')

    # telegram bot configuration
    BOT_TOKEN = getenv('TELEGRAM_BOT_TOKEN')
    CHAT_ID = getenv('TELEGRAM_CHAT_ID')

    # email check interval in seconds
    CHECK_INTERVAL = 60
