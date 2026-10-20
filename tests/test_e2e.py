import asyncio
import os
import unittest
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

os.environ.setdefault("OPENAI_API_KEY", "test-key")

import telegram_bot


class CriticalPathE2ETests(unittest.TestCase):
    def setUp(self):
        telegram_bot.histories.clear()

    def test_chat_limits_model_context_to_five_history_exchanges(self):
        history = [
            message
            for exchange in range(7)
            for message in (
                {"role": "user", "content": f"user {exchange}"},
                {"role": "assistant", "content": f"assistant {exchange}"},
            )
        ]
        openai_response = SimpleNamespace(
            choices=[
                SimpleNamespace(
                    finish_reason="stop",
                    message=SimpleNamespace(content="Answer"),
                )
            ]
        )

        with patch(
            "app.openai.chat.completions.create", return_value=openai_response
        ) as request:
            telegram_bot.chat("current question", history)

        request_messages = request.call_args.kwargs["messages"]
        self.assertEqual(len(request_messages), 12)
        self.assertEqual(request_messages[0]["role"], "system")
        self.assertEqual(request_messages[1:-1], history[-10:])
        self.assertEqual(
            request_messages[-1],
            {"role": "user", "content": "current question"},
        )

    def test_telegram_message_reaches_ai_and_returns_answer(self):
        chat_id = 100
        start_message = SimpleNamespace(reply_text=AsyncMock())
        start_update = SimpleNamespace(
            effective_chat=SimpleNamespace(id=chat_id), message=start_message
        )
        asyncio.run(telegram_bot.start(start_update, SimpleNamespace()))

        user_message = SimpleNamespace(
            text="Tell me about your experience.", reply_text=AsyncMock()
        )
        update = SimpleNamespace(
            effective_chat=SimpleNamespace(id=chat_id), message=user_message
        )
        bot_context = SimpleNamespace(
            bot=SimpleNamespace(send_chat_action=AsyncMock())
        )
        openai_response = SimpleNamespace(
            choices=[
                SimpleNamespace(
                    finish_reason="stop",
                    message=SimpleNamespace(content="I have experience in software engineering."),
                )
            ]
        )

        with patch("app.openai.chat.completions.create", return_value=openai_response) as request:
            asyncio.run(telegram_bot.respond(update, bot_context))

        request.assert_called_once()
        request_messages = request.call_args.kwargs["messages"]
        self.assertEqual(request_messages[-1], {"role": "user", "content": user_message.text})
        user_message.reply_text.assert_awaited_once_with(
            "I have experience in software engineering."
        )
        self.assertEqual(
            telegram_bot.histories[chat_id][-2:],
            [
                {"role": "user", "content": user_message.text},
                {
                    "role": "assistant",
                    "content": "I have experience in software engineering.",
                },
            ],
        )


if __name__ == "__main__":
    unittest.main()