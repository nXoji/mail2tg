import html
from email.header import decode_header

class Formatter:
    @staticmethod
    def get_body(msg) -> str:
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

    @staticmethod
    def decode_mime_header(header_value: str) -> str:
        if not header_value:
            return "(No Value)"

        decoded_parts = decode_header(header_value)
        decoded_string = ''
        for part, encoding in decoded_parts:
            if isinstance(part, bytes):
                encoding = encoding or 'utf-8'
                decoded_string += part.decode(encoding, errors='ignore')
            else:
                decoded_string += part
        return decoded_string

    @staticmethod
    def format_telegram_message(email_data: dict) -> str:
        safe_sender = html.escape(email_data['sender'])
        safe_subject = html.escape(email_data['subject'])
        safe_body = html.escape(email_data['body'])

        if len(safe_body) > 2000:
            safe_body = safe_body[:2000] + "..."

        formatted_message = (
            f"<b>📧 New Email Received</b>\n"
            f"<b>From:</b> {safe_sender}\n"
            f"<b>Subject:</b> {safe_subject}\n\n"
            f"{safe_body}"
        )

        return formatted_message
