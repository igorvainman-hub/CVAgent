# CV Agent

AI digital twin that answers questions about a person's career, skills and experience. The project provides both a Gradio web interface and a Telegram bot.

## Requirements

- Python 3.11 or newer
- An OpenAI API key
- A Telegram bot token for Telegram mode
- Your own LinkedIn export as `linkedin.pdf`
- Your own profile summary as `summary.txt`

## Setup

Create and activate a virtual environment, then install the dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Copy `.env.example` to `.env` and set the required values:

```powershell
Copy-Item .env.example .env
```

```env
OPENAI_API_KEY=your_openai_api_key
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
```

Add your personal profile data to the project root:

- `linkedin.pdf` - export your LinkedIn profile as a PDF and rename it to `linkedin.pdf`.
- `summary.txt` - write a short description of yourself and save it as `summary.txt`.

These files are intentionally ignored by Git because every project owner must use their own data. Do not upload another person's profile information to GitHub.

Create the Telegram token with [@BotFather](https://t.me/BotFather) using `/newbot`. Keep `.env` private and never commit it.

## Run the Telegram bot

```powershell
python telegram_bot.py
```

Open the bot in Telegram and send `/start`. Use `/reset` to clear the conversation history. The bot uses long polling, so the process must remain running.

## Run the web interface

```powershell
python app.py
```

Gradio prints a local URL in the terminal.

## Run tests

```powershell
python -m unittest discover -s tests -v
```

## Optional notifications

Set `EMAIL_SMTP_SERVER`, `EMAIL_SMTP_PORT`, `EMAIL_ADDRESS`, `EMAIL_APP_PASSWORD`, and `EMAIL_TO` if you want the agent to email contact requests and unanswered questions. These values are not required for ordinary chat.

## Project files

- `telegram_bot.py` - Telegram polling bot
- `app.py` - Gradio interface and OpenAI chat logic
- `context.py` - prompt and profile data loading
- `tools.py` - optional email notification tools
- `summary.txt` and `linkedin.pdf` - profile data used by the agent