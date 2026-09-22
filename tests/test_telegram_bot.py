import asyncio
import os
import unittest
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

os.environ.setdefault("OPENAI_API_KEY", "test-key")

import telegram_bot


class TelegramBotTests(unittest.TestCase):
    def setUp(self):
        telegram_bot.histories.clear()

    def test_start_resets_chat_history(self):
        chat_id = 42
        telegram_bot.histories[chat_id] = [{"role": "user", "content": "old"}]
        message = SimpleNamespace(reply_text=AsyncMock())
        update = SimpleNamespace(
            effective_chat=SimpleNamespace(id=chat_id), message=message
        )

        asyncio.run(telegram_bot.start(update, SimpleNamespace()))

        self.assertEqual(telegram_bot.histories[chat_id], [])
        message.reply_text.assert_awaited_once()

    def test_respond_saves_history_and_replies(self):
        chat_id = 7
        message = SimpleNamespace(text="What are your skills?", reply_text=AsyncMock())
        update = SimpleNamespace(
            effective_chat=SimpleNamespace(id=chat_id), message=message
        )
        context = SimpleNamespace(bot=SimpleNamespace(send_chat_action=AsyncMock()))

        with patch.object(telegram_bot, "chat", return_value="I build software."):
            asyncio.run(telegram_bot.respond(update, context))

        self.assertEqual(
            telegram_bot.histories[chat_id],
            [
                {"role": "user", "content": "What are your skills?"},
                {"role": "assistant", "content": "I build software."},
            ],
        )
        context.bot.send_chat_action.assert_awaited_once_with(
            chat_id=chat_id, action="typing"
        )
        message.reply_text.assert_awaited_once_with("I build software.")

    def test_respond_splits_long_messages(self):
        long_answer = "a" * 5000
        message = SimpleNamespace(text="Tell me more", reply_text=AsyncMock())
        update = SimpleNamespace(
            effective_chat=SimpleNamespace(id=8), message=message
        )
        context = SimpleNamespace(bot=SimpleNamespace(send_chat_action=AsyncMock()))

        with patch.object(telegram_bot, "chat", return_value=long_answer):
            asyncio.run(telegram_bot.respond(update, context))

        self.assertEqual(message.reply_text.await_count, 2)
        self.assertEqual(message.reply_text.await_args_list[0].args[0], "a" * 4096)
        self.assertEqual(message.reply_text.await_args_list[1].args[0], "a" * 904)


if __name__ == "__main__":
    unittest.main()