# CV Agent

CV Agent is an AI digital twin that answers recruiters' questions about a
professional's documented career, skills, and experience. It provides a
Gradio web chat and a Telegram bot, powered by the OpenAI API.

The agent uses the project owner's LinkedIn PDF export and profile summary as
its only sources of personal facts. It is instructed to be transparent that
it is an AI representative, avoid unsupported claims, and keep conversations
focused on professional background and role-related questions.

## Requirements

- Python 3.11 or newer
- An OpenAI API key
- A Telegram bot token if you plan to run the Telegram bot
- Your LinkedIn profile export as `linkedin.pdf`
- Your profile summary as `summary.txt`

## Setup

Create and activate a virtual environment, then install the dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Create a local `.env` file from the example and set your OpenAI API key. Add
the Telegram token if you will use Telegram:

```powershell
Copy-Item .env.example .env
```

```env
OPENAI_API_KEY=your_openai_api_key
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
```

Place your profile data in the project root:

- `linkedin.pdf` - your LinkedIn profile export in PDF format.
- `summary.txt` - a concise summary of your professional background.

Both files are required when the app starts. They are excluded from Git so
each project owner can use their own profile; do not commit personal profile
data. Keep `.env` private and never commit API keys or bot tokens.

Create a Telegram bot token with [@BotFather](https://t.me/BotFather) using
`/newbot`.

## Run the web chat

```powershell
python app.py
```

Gradio prints the local URL in the terminal. The web chat retains up to the
most recent 10 history messages for each request.

## Run the Telegram bot

```powershell
python telegram_bot.py
```

Open the bot in Telegram and send `/start` to begin. Send `/reset` to clear
that chat's conversation history. Telegram uses long polling, so keep the
process running while using the bot. Chat history is held in memory and is
cleared when the process restarts.

## Email notifications (optional)

The agent can email contact requests and questions it cannot answer from the
profile. Configure these values in `.env` to enable those notifications:

```env
EMAIL_SMTP_SERVER=smtp.gmail.com
EMAIL_SMTP_PORT=587
EMAIL_ADDRESS=your_email@example.com
EMAIL_APP_PASSWORD=your_email_app_password
EMAIL_TO=recipient@example.com
```

These settings are not required for ordinary chat. The example values are
placeholders; use credentials for your own SMTP account. The `.env.example`
file includes the full list of supported settings.

## Run tests

```powershell
python -m unittest discover -s tests -v
```

## Project files

- `app.py` - Gradio web interface and OpenAI chat handling.
- `telegram_bot.py` - Telegram bot commands and message handling.
- `context.py` - Loads profile data and builds the system prompt.
- `tools.py` - Contact and unanswered-question email notification tools.
- `styles.py` - Web interface styles and example prompts.
- `requirements.txt` - Python dependencies.
- `linkedin.pdf` and `summary.txt` - Required, owner-specific profile data.
