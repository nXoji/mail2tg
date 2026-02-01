import re
import io
import email
import imaplib
from config import Config
from formatter import Formatter
from typing import List, Optional
from logger import get_logger

class EmailService:
    def __init__(self):
        self.mail = None
        self.logger = get_logger(__name__)

        self.IMAP_SERVER = Config.IMAP_SERVER
        self.IMAP_PORT = Config.IMAP_PORT
        self.EMAIL_ADDRESS = Config.EMAIL_ADDRESS
        self.APP_PASSWORD = Config.APP_PASSWORD
        self.ALLOWED_SENDERS = Config.ALLOWED_SENDERS
        self.BLOCKED_SENDERS = Config.BLOCKED_SENDERS

    def connect(self) -> bool:
        try:
            self.mail = imaplib.IMAP4_SSL(self.IMAP_SERVER, self.IMAP_PORT)
            self.mail.login(self.EMAIL_ADDRESS, self.APP_PASSWORD)
            self.logger.debug("Successfully connected to email server")
            return True
        except imaplib.IMAP4.error as e:
            self.logger.error(f"IMAP authentication failed: {e}")
            return False
        except Exception as e:
            self.logger.error(f"Failed to connect to IMAP server: {e}")
            return False

    def disconnect(self):
        if self.mail:
            try:
                self.mail.logout()
                self.logger.debug("Disconnected from IMAP server.")
            except Exception as e:
                self.logger.error(f"Error during disconnect: {e}")

    def get_unseen_emails(self) -> List[dict]:
        try:
            self.mail.select('INBOX')
            status, email_ids = self.mail.search(None, '(UNSEEN)')

            if status != 'OK':
                self.logger.error("IMAP search failed")
                return []

            if not email_ids[0]:
                self.logger.info("No unseen emails found")
                return []

            emails = []
            for email_id in email_ids[0].split():
                email_data = self._fetch_email(email_id)
                if not email_data:
                    continue

                if not self._is_allowed_sender(email_data['sender']):
                    self.mark_as_read(email_id)
                    continue

                emails.append(email_data)

            if emails:
                self.logger.info(f"Found {len(emails)} new email(s) after filtering")

            return emails
        except Exception as e:
            self.logger.error(f"Failed to fetch unseen emails: {e}")
            return []

    def _is_allowed_sender(self, sender: str) -> bool:
        match = re.search(r'[\w\.-]+@[\w\.-]+', sender)
        email_address = match.group(0).lower() if match else sender.lower()

        if Config.BLOCKED_SENDERS and email_address in Config.BLOCKED_SENDERS:
            self.logger.info(f"Email from <{email_address}> blocked by BLOCKED_SENDERS list")
            return False

        if Config.ALLOWED_SENDERS and email_address not in Config.ALLOWED_SENDERS:
            self.logger.info(f"Email from <{email_address}> skipped (not in ALLOWED_SENDERS)")
            return False

        return True

    def _fetch_email(self, email_id: bytes) -> Optional[dict]:
        status, msg_data = self.mail.fetch(email_id, '(BODY.PEEK[])')
        if status != 'OK':
            self.logger.warning(f"Failed to fetch email {email_id}: status {status}")
            return None

        msg = email.message_from_bytes(msg_data[0][1])
        attachments = self._process_attachments(msg)

        return {
            'id': email_id,
            'subject': Formatter.decode_mime_header(msg['Subject']),
            'sender': Formatter.decode_mime_header(msg['From']),
            'body': Formatter.get_body(msg),
            'attachments': attachments
        }

    def _process_attachments(self, msg) -> List[dict]:
        attachments = []
        for part in msg.walk():
            if part.get_content_maintype() == 'multipart':
                continue

            if part.get('Content-Disposition') is None:
                continue

            filename = part.get_filename()
            if filename:
                try:
                    filename = Formatter.decode_mime_header(filename)
                    file_data = part.get_payload(decode=True)

                    if file_data:
                        attachment_io = io.BytesIO(file_data)
                        attachment_io.name = filename

                        attachments.append({
                            'filename': filename,
                            'content': attachment_io
                        })
                except Exception as e:
                    self.logger.error(f"Error processing attachment {filename}: {e}")
                    continue

        return attachments

    def mark_as_read(self, email_id: bytes):
        try:
            self.mail.store(email_id, '+FLAGS', '\\Seen')
            self.logger.debug(f"Marked email {email_id} as read.")
        except Exception as e:
            self.logger.error(f"Failed to mark email {email_id} as read: {e}")
