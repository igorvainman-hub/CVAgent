import json
import os
import smtplib
from email.message import EmailMessage
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent / ".env", override=True)

email_smtp_server = os.getenv("EMAIL_SMTP_SERVER")
email_smtp_port = int(os.getenv("EMAIL_SMTP_PORT", "587"))
email_address = os.getenv("EMAIL_ADDRESS") or os.getenv("EMAIL_FROM")
email_app_password = os.getenv("EMAIL_APP_PASSWORD") or os.getenv("EMAIL_PASSWORD")
email_recipient = os.getenv("EMAIL_TO") or os.getenv("EMAIL_RECIPIENT") or email_address


def send_email_notification(text):
    if not all([email_smtp_server, email_address, email_app_password, email_recipient]):
        return

    message = EmailMessage()
    message["Subject"] = "CV Agent notification"
    message["From"] = email_address
    message["To"] = email_recipient
    message.set_content(text)

    with smtplib.SMTP(email_smtp_server, email_smtp_port) as smtp:
        smtp.starttls()
        smtp.login(email_address, email_app_password)
        smtp.send_message(message)


def push(text):
    send_email_notification(text)


def record_user_details(email, name="Name not provided", notes="not provided"):
    push(f"Recording interest from {name} with email {email} and notes {notes}")
    return "OK"


def record_unknown_question(question):
    push(f"Recording {question} asked that I couldn't answer")
    return "OK"


record_user_details_json = {
    "name": "record_user_details",
    "description": "Use this tool to record that a user is interested in being in touch and provided an email address",
    "parameters": {
        "type": "object",
        "properties": {
            "email": {"type": "string", "description": "The email address of this user"},
            "name": {"type": "string", "description": "The user's name, if they provided it"},
            "notes": {
                "type": "string",
                "description": "Any additional info about the conversation that's worth recording to give context",
            },
        },
        "required": ["email"],
        "additionalProperties": False,
    },
}

record_unknown_question_json = {
    "name": "record_unknown_question",
    "description": "Always use this tool to record any question that couldn't be answered as you didn't know the answer",
    "parameters": {
        "type": "object",
        "properties": {
            "question": {"type": "string", "description": "The question that couldn't be answered"},
        },
        "required": ["question"],
        "additionalProperties": False,
    },
}

tools = [
    {"type": "function", "function": record_user_details_json},
    {"type": "function", "function": record_unknown_question_json},
]

tool_map = {
    "record_user_details": record_user_details,
    "record_unknown_question": record_unknown_question,
}


def handle_tool_calls(tool_calls):
    results = []
    for tool_call in tool_calls:
        tool_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)
        print(f"Tool called: {tool_name}", flush=True)
        tool = tool_map.get(tool_name)
        result = tool(**arguments) if tool else "Unknown tool: " + tool_name
        results.append(
            {"role": "tool", "content": json.dumps(result), "tool_call_id": tool_call.id}
        )
    return results
