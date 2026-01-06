import time
from config import Config
from email_service import EmailService
from telegram_service import TelegramService
from formatter import Formatter
from logger import setup_logging, get_logger

setup_logging()
logger = get_logger(__name__)

def main():
    logger.info("Starting mail2tg...")

    email_service = EmailService()
    telegram_service = TelegramService()

    while True:
        if email_service.connect():
            unseen_emails = email_service.get_unseen_emails()

            if unseen_emails:
                for email_data in unseen_emails:
                    messages = Formatter.format_telegram_message(email_data)
                    all_sent = True

                    for i, msg_parts in enumerate(messages):
                        if not telegram_service.send_message(msg_parts):
                            logger.error(f"Failed to send part {i+1}/{len(messages)} of email {email_data['id']}")
                            all_sent = False
                            break

                    if all_sent:
                        email_service.mark_as_read(email_data['id'])
                    else:
                        logger.warning(f"Email {email_data['id']} was not marked as read due to sending errors.")

        email_service.disconnect()

        time.sleep(Config.CHECK_INTERVAL)

if __name__ == "__main__":
    main()
