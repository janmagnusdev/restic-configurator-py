import email
import smtplib
import ssl
from email.message import EmailMessage

import keyring


def send(msg):
    smtp_server = "smtp.mailbox.org"
    port = 465  # 25 for plain, 465 for automatic SSL, 587 for STARTTLS

    password = keyring.get_password("smtp.mailbox.org", "jan-magnus@monenschein.eu")
    if password is None:
        raise RuntimeError("No password found in keyring, can't send mail")

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login("jan-magnus@monenschein.eu", password)
        server.send_message(msg)


def create_message(content: str, to: str, subject: str) -> EmailMessage:
    msg = email.message.EmailMessage()

    msg["to"] = to
    msg["from"] = "mail@janmagnus.dev"
    msg["subject"] = f"[restic-configurator-py (automated)] {subject}"
    msg.set_content(content)
    return msg
