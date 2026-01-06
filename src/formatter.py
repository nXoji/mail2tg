import re
import html
from email.header import decode_header
from bs4 import BeautifulSoup
from logger import get_logger

logger = get_logger(__name__)

class Formatter:
    @staticmethod
    def get_body(msg) -> str:
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/html":
                    html_content = Formatter._decode_payload(part)
                    return Formatter._clean_html(html_content)

            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    return html.escape(Formatter._decode_payload(part))
        else:
            content = Formatter._decode_payload(msg)
            if msg.get_content_type() == "text/html":
                return Formatter._clean_html(content)

            return html.escape(content)

        return "(No text content)"

    @staticmethod
    def _decode_payload(part) -> str:
        payload = part.get_payload(decode=True)
        charset = part.get_content_charset() or 'utf-8'
        return payload.decode(charset, errors='ignore')

    @staticmethod
    def _clean_html(html_content: str) -> str:
        try:
            soup = BeautifulSoup(html_content, "html.parser")

            for tag in soup(["script", "style", "meta", "head", "title", "link"]):
                tag.decompose()

            for a in soup.find_all("a", href=True):
                text = a.get_text(strip=True)
                href = a["href"]

                if not href or href.startswith(("#", "javascript:")) or not text:
                    continue

                safe_text = html.escape(text)
                safe_href = html.escape(href)

                a.replace_with(f"##LINK_START##{safe_href}##TEXT_START##{safe_text}##LINK_END##")

            for br in soup.find_all("br"):
                br.replace_with("\n")

            block_tags = [
                'p', 'div', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
                'li', 'tr', 'blockquote', 'article', 'section', 'header', 'footer'
            ]
            for tag in soup.find_all(block_tags):
                tag.insert_after("\n")

            text = soup.get_text(separator=" ", strip=False)

            escaped_text = html.escape(text)

            final_text = re.sub(
                r'##LINK_START##(.*?)##TEXT_START##(.*?)##LINK_END##',
                r'<a href="\1">\2</a>',
                escaped_text
            )
            lines = []
            for line in final_text.split('\n'):
                clean_line = re.sub(r'\s+', ' ', line).strip()
                if clean_line:
                    lines.append(clean_line)

            return '\n'.join(lines)
        except Exception as e:
            logger.warning(f"HTML parsing failed: {e}")
            return html.escape(html_content)

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
        body_text = email_data['body']

        formatted_message = (
            f"<b>📧 New Email Received</b>\n"
            f"<b>From:</b> {safe_sender}\n"
            f"<b>Subject:</b> {safe_subject}\n\n"
            f"{body_text}"
        )

        return Formatter._split_message(formatted_message)

    @staticmethod
    def _split_message(text: str, max_length: int = 4096) -> list:
        if len(text) <= max_length:
            return [text]

        parts = []
        while text:
            if len(text) <= max_length:
                parts.append(text)
                break

            split_at = text.rfind('\n', 0, max_length)
            if split_at == -1:
                split_at = text.rfind(' ', 0, max_length)
            if split_at == -1:
                split_at = max_length

            chunk = text[:split_at]
            parts.append(chunk)

            text = text[split_at:].lstrip()

        return parts
