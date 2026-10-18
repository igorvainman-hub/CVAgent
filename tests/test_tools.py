import unittest
from unittest.mock import patch

import tools


class NotificationToolTests(unittest.TestCase):
    def setUp(self):
        self.settings = patch.multiple(
            tools,
            email_smtp_server="smtp.example.com",
            email_smtp_port=587,
            email_address="from@example.com",
            email_app_password="secret",
            email_recipient="to@example.com",
        )
        self.settings.start()
        self.addCleanup(self.settings.stop)

    def assert_notification_sent(self, send_notification, expected_subject, expected_body):
        with patch("tools.smtplib.SMTP") as mock_smtp:
            mock_smtp.return_value.__enter__.return_value = mock_smtp.return_value
            result = send_notification()

        mock_smtp.assert_called_once_with("smtp.example.com", 587)
        mock_smtp.return_value.login.assert_called_once_with("from@example.com", "secret")
        message = mock_smtp.return_value.send_message.call_args.args[0]
        self.assertEqual(message["Subject"], expected_subject)
        self.assertEqual(message["From"], "from@example.com")
        self.assertEqual(message["To"], "to@example.com")
        self.assertEqual(message.get_content().strip(), expected_body)
        self.assertEqual(result, "OK")

    def test_record_user_details_sends_contact_email(self):
        self.assert_notification_sent(
            lambda: tools.record_user_details(
                "person@example.com", "Alex", "Interested in the project"
            ),
            "New contact request",
            "New contact request\nName: Alex\nEmail: person@example.com\n"
            "Notes: Interested in the project",
        )

    def test_record_unknown_question_sends_question_email(self):
        self.assert_notification_sent(
            lambda: tools.record_unknown_question("How does the agent work?"),
            "Unanswered question",
            "An unanswered question was recorded:\nHow does the agent work?",
        )

    def test_email_notification_fails_when_not_configured(self):
        with patch.object(tools, "email_smtp_server", None):
            with self.assertRaisesRegex(RuntimeError, "EMAIL_SMTP_SERVER"):
                tools.record_unknown_question("A question")


if __name__ == "__main__":
    unittest.main()
