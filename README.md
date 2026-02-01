<div align="center">
  <img src="https://cdn2.iconfinder.com/data/icons/email-114/100/email-forward-2-email-mail-action-letter-envelope-forward-resend-512.png" width="25%">
  <h1>mail2tg</h1>
  <p>
    <strong>Your email inbox, delivered straight to Telegram.</strong>
  </p>
  <p>

![python](https://img.shields.io/badge/python-3.11+-blue.svg)
![MIT](https://img.shields.io/badge/license-MIT-green)
![docker](https://img.shields.io/badge/docker-enabled-blue)

  </p>
</div>

# About
**mail2tg** is a lightweight bridge designed to bring your IMAP mailbox into Telegram. It focuses on readability and reliability, transforming messy automated emails into clean Telegram messages while ensuring that no critical notification is ever missed due to silent inbox delivery.

# Key Features
* **📎 Attachment Support**: Automatically forwards files and documents alongside email text.
* **🧹 HTML Cleaning**: Transforms cluttered HTML emails into clean, readable text.
* **🔗 Link Preservation**: Keeps all clickable links functional in the forwarded message.
* **✂️ Smart Splitting**: Automatically divides long emails to comply with Telegram's character limits.
* **🛡️ Reliable Delivery**: Emails are marked as "Read" only after successful delivery, ensuring no data loss.
* **🚫 Sender Filtering**: Support for Whitelists and Blacklists to control which emails get forwarded.

# Installation
## Option 1: Docker (Recommended)
1. Clone the repository:
```
git clone https://github.com/nXoji/mail2tg.git
cd mail2tg
```
2. Create .env file from the example:
```
cp .env.example .env
```
3. Edit `.env` with your credentials (see [Configuration](#configuration))
4. Run with Docker Compose:
```
docker compose up -d
```
## Option 2: Manual Installation
1. Clone the repository:
```
git clone https://github.com/nXoji/mail2tg.git
cd mail2tg
```
2. Install dependencies:
```
pip install -r requirements.txt
```
3. Create .env file from the example:
```
cp .env.example .env
```
4. Edit `.env` with your credentials (see [Configuration](#configuration))
5. Run the script:
```
python src/main.py
```

# Configuration
Configure the application by editing the `.env` file. Below are the available environment variables:
| Variable | Description | Example |
| :--- | :--- | :--- |
| `IMAP_SERVER` | IMAP server address of your email provider | `imap.gmail.com` |
| `IMAP_PORT` | IMAP port (usually 993 for SSL) | `993` |
| `EMAIL_ADDRESS` | Your full email address | `user@example.com` |
| `EMAIL_APP_PASSWORD` | App Password (not your login password). Generate one in your email security settings. | `abcd 1234 efgh 5678` |
| `TELEGRAM_BOT_TOKEN` | Token received from @BotFather | `123456:ABC-DEF...` |
| `TELEGRAM_CHAT_ID` | Your numeric Telegram Chat ID (get it from bots like @userinfobot) | `123456789` |
| `CHECK_INTERVAL` | Interval between email checks in seconds (default: 60) | `60` |
| `ALLOWED_SENDERS` | Optional: comma-separated list of allowed emails | `friend@gmail.com, boss@work.com` |
| `BLOCKED_SENDERS` | Optional: comma-separated list of blocked emails | `spam@bad.com, marketing@ads.com` |

# License
mail2tg is open source software under the [MIT License](https://opensource.org/license/mit/).
