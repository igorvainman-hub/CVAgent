import importlib
import os
import unittest
from unittest.mock import patch


class NotificationToolTests(unittest.TestCase):
    def reload_tools(self):
        import tools
        return importlib.reload(tools)

    def test_push_uses_email_when_configured(self):
        os.environ["EMAIL_SMTP_SERVER"] = "smtp.example.com"
        os.environ["EMAIL_SMTP_PORT"] = "587"
        os.environ["EMAIL_ADDRESS"] = "from@example.com"
        os.environ["EMAIL_APP_PASSWORD"] = "secret"
        os.environ["EMAIL_TO"] = "to@example.com"

        tools = self.reload_tools()

        with patch("tools.smtplib.SMTP") as mock_smtp:
            mock_smtp.return_value.__enter__.return_value = mock_smtp.return_value
            tools.push("hello from email")

        mock_smtp.assert_called_once_with("smtp.example.com", 587)
        mock_smtp.return_value.login.assert_called_once_with("from@example.com", "secret")

    def tearDown(self):
        for key in [
            "EMAIL_SMTP_SERVER",
            "EMAIL_SMTP_PORT",
            "EMAIL_ADDRESS",
            "EMAIL_APP_PASSWORD",
            "EMAIL_TO",
            "EMAIL_RECIPIENT",
            "EMAIL_FROM",
            "EMAIL_PASSWORD",
        ]:
            os.environ.pop(key, None)


if __name__ == "__main__":
    unittest.main()
