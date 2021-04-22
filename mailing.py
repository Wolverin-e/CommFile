import smtplib, ssl
from email.message import EmailMessage
import json

def send_msg(msg_body):

    with open("./config.json") as conf_file:
        config = json.load(conf_file)

    msg = EmailMessage()
    msg.set_content(msg_body)

    msg['Subject'] = 'Sent using MailFS'
    msg['From'] = config["from"]
    msg['To'] = config["send_to"]

    context = ssl.create_default_context()

    smtp_config = config["smtp"]

    with smtplib.SMTP_SSL(smtp_config["server"], int(smtp_config["port"]), context=context) as server:
        server.login(smtp_config["user"], smtp_config["pass"])
        server.send_message(msg)
