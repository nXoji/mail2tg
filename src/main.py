import time
from config import Config
from email_service import EmailService
from telegram_service import TelegramService
from formatter import Formatter

def main():
    print("Starting mail2tg...")

    email_service = EmailService()
    telegram_service = TelegramService()

    while True:
        if email_service.connect():
            unseen_emails = email_service.get_unseen_emails()
            email_service.disconnect()

            if unseen_emails:
                print(f"Found {len(unseen_emails)} new email(s). Processing...")

                for email_data in unseen_emails:
                    email = Formatter.format_telegram_message(email_data)
                    telegram_service.send_message(email)

        time.sleep(Config.CHECK_INTERVAL)

if __name__ == "__main__":
    main()
