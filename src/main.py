import signal
import threading
from config import Config
from email_service import EmailService
from telegram_service import TelegramService
from formatter import Formatter
from logger import setup_logging, get_logger

setup_logging()
logger = get_logger(__name__)

shutdown_event = threading.Event()

def signal_handler(signum, frame):
    logger.info("Shutdown signal received, stopping...")
    shutdown_event.set()

def main():
    logger.info("Starting mail2tg...")

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    email_service = EmailService()
    telegram_service = TelegramService()

    while not shutdown_event.is_set():
        if email_service.connect():
            unseen_emails = email_service.get_unseen_emails()

            if unseen_emails:
                for email_data in unseen_emails:
                    if shutdown_event.is_set():
                        break

                    messages = Formatter.format_telegram_message(email_data)
                    all_sent = True

                    for i, msg_parts in enumerate(messages):
                        if not telegram_service.send_message(msg_parts):
                            logger.error(f"Failed to send part {i+1}/{len(messages)} of email {email_data['id']}")
                            all_sent = False
                            break

                    if all_sent and email_data.get('attachments'):
                        for attachment in email_data['attachments']:
                            fname = attachment['filename']
                            fcontent = attachment['content']

                            logger.info(f"Sending attachment: {fname}")

                            if not telegram_service.send_document(fname, fcontent):
                                logger.error(f"Failed to send attachment: {fname}")
                                all_sent = False

                            fcontent.close()

                    if not all_sent:
                        logger.warning(f"Email {email_data['id']} had errors during sending. Marking as read to prevent loop.")
                    email_service.mark_as_read(email_data['id'])

            email_service.disconnect()

        shutdown_event.wait(Config.CHECK_INTERVAL)

    logger.info("mail2tg stopped.")

if __name__ == "__main__":
    main()
