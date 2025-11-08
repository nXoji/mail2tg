import time
import email
import imaplib
from os import getenv
from dotenv import load_dotenv
import requests
import html

load_dotenv()

IMAP_SERVER = 'imap.gmail.com'
EMAIL_ADDRESS = getenv("GMAIL_EMAIL")
APP_PASSWORD = getenv('GMAIL_APP_PASSWORD')
BOT_TOKEN = getenv('TELEGRAM_BOT_TOKEN')
CHAT_ID = getenv('TELEGRAM_CHAT_ID')

def get_body(msg):
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                payload = part.get_payload(decode=True)
                charset = part.get_content_charset() or 'utf-8'
                return payload.decode(charset, errors='ignore')
    else:
        payload = msg.get_payload(decode=True)
        charset = msg.get_content_charset() or 'utf-8'
        return payload.decode(charset, errors='ignore')

    return "(No text content)"

def send_to_telegram(text: str) -> bool:
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "HTML",
    }
    try:
        r = requests.post(url, data=payload, timeout=20)
        if r.ok:
            return True
        else:
            print(f"Telegram API error: {r.status_code} {r.text}")
            return False
    except Exception as e:
        print(f"Failed to send message to Telegram: {e}")
        return False


def check_and_forward_emails():
        print(f"Connecting to IMAP server: {IMAP_SERVER}...")
        mail = imaplib.IMAP4_SSL(IMAP_SERVER, 993)

        mail.login(EMAIL_ADDRESS, APP_PASSWORD)
        print("Logged in successfully.")

        mail.select('INBOX')

        status, email_ids = mail.search(None, '(UNSEEN)')

        if status != 'OK':
            print(f"IMAP search failed with status: {status}")
            mail.logout()
            return

        id_list = email_ids[0].split()

        if not id_list:
            print("No new emails found.")
            mail.logout()
            return

        print(f"Found {len(id_list)} new email(s). Processing...")

        for email_id in id_list:
            status, msg_data = mail.fetch(email_id, '(RFC822)')

            if status != 'OK':
                print(f"Failed to fetch email ID {email_id}. Skipping.")
                continue

            msg = email.message_from_bytes(msg_data[0][1])

            subject = str(msg.get('Subject', '(No Subject)'))
            sender = str(msg['From'] if msg['From'] else '(Unknown Sender)')

            body = str(get_body(msg))
            body = body if len(body) < 2000 else body[:2000] + '...'

            telegram_message = f"""
<b>📧 New Email Received</b>
<b>From:</b> {html.escape(sender)}
<b>Subject:</b> {html.escape(subject)}

{html.escape(body)}"""
            send_to_telegram(telegram_message.strip())

            mail.store(email_id, '+FLAGS', '\\Seen')

        mail.logout()
        print("IMAP connection closed.")

def main():
    print("Starting mail2tg...")

    while True:
        check_and_forward_emails()
        time.sleep(10)

if __name__ == "__main__":
    main()
