import email
import imaplib
from config import Config
from formatter import Formatter
from typing import List, Optional

class EmailService:
    def __init__(self):
        self.mail = None

        self.IMAP_SERVER = Config.IMAP_SERVER
        self.IMAP_PORT = Config.IMAP_PORT
        self.EMAIL_ADDRESS = Config.EMAIL_ADDRESS
        self.APP_PASSWORD = Config.APP_PASSWORD

    def connect(self):
        self.mail = imaplib.IMAP4_SSL(self.IMAP_SERVER, self.IMAP_PORT)
        self.mail.login(self.EMAIL_ADDRESS, self.APP_PASSWORD)
        
        return True

    def disconnect(self):
        if self.mail:
            self.mail.logout()

    def get_unseen_emails(self) -> List[dict]:
        self.mail.select('INBOX')
        status, email_ids = self.mail.search(None, '(UNSEEN)')

        if status != 'OK' or not email_ids[0]:
            return []

        emails = []
        for email_id in email_ids[0].split():
            email_data = self._fetch_email(email_id)
            if email_data:
                emails.append(email_data)
                self._mark_as_read(email_id)

        return emails

    def _fetch_email(self, email_id: bytes) -> Optional[dict]:
        status, msg_data = self.mail.fetch(email_id, '(RFC822)')
        if status != 'OK':
            return None

        msg = email.message_from_bytes(msg_data[0][1])

        return {
            'id': email_id,
            'subject': Formatter.decode_mime_header(msg['Subject']),
            'sender': Formatter.decode_mime_header(msg['From']),
            'body': Formatter.get_body(msg)
        }

    def _mark_as_read(self, email_id: bytes):
        self.mail.store(email_id, '+FLAGS', '\\Seen')
