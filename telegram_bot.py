import asyncio
import logging
import os
from pathlib import Path

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

from app import chat

load_dotenv(Path(__file__).resolve().parent / ".env", override=True)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

histories: dict[int, list[dict[str, str]]] = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_chat is None or update.message is None:
        return

    histories[update.effective_chat.id] = []
    await update.message.reply_text(
        "Hello! I am a CV agent. Ask me about my career, skills, and experience."
    )


async def respond(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_chat is None or update.message is None:
        return

    user_message = update.message.text
    if not user_message:
        return

    history = histories.setdefault(update.effective_chat.id, [])
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")

    try:
        answer = await asyncio.to_thread(chat, user_message, history)
    except Exception:
        logging.exception("Error while processing a Telegram message")
        await update.message.reply_text("Sorry, I could not process that message.")
        return

    history.extend(
        [
            {"role": "user", "content": user_message},
            {"role": "assistant", "content": answer},
        ]
    )

    for start_index in range(0, len(answer), 4096):
        await update.message.reply_text(answer[start_index : start_index + 4096])


async def main() -> None:
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        raise RuntimeError("Set TELEGRAM_BOT_TOKEN in the .env file")

    application = Application.builder().token(token).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("reset", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, respond))

    await application.initialize()
    await application.start()
    await application.updater.start_polling()
    try:
        await asyncio.Event().wait()
    finally:
        await application.updater.stop()
        await application.stop()
        await application.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
