<div align="center">
  <img src="https://cdn2.iconfinder.com/data/icons/email-114/100/email-forward-2-email-mail-action-letter-envelope-forward-resend-512.png" width="25%">
  <h1>mail2tg</h1>
  <p>
    <strong>mail2tg is a lightweight and reliable bot that forwards incoming emails from your IMAP mailbox directly to Telegram.</strong>
  </p>
  <p>

![python](https://img.shields.io/badge/python-3.11+-blue.svg)
![MIT](https://img.shields.io/badge/license-MIT-green)
![docker](https://img.shields.io/badge/docker-enabled-blue)

  </p>
</div>

# About
**mail2tg** acts as a reliable bridge between your email and Telegram. It regularly checks your IMAP inbox for new unread messages and forwards them to your chat. Unlike simple forwarders, mail2tg cleans up messy HTML emails into readable text, preserves clickable links, and intelligently splits long messages that exceed Telegram's character limits. It ensures no data is lost by only marking emails as "Read" on the server after they have been successfully delivered.

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

# License
mail2tg is open source software under the [MIT License](https://opensource.org/license/mit/).
