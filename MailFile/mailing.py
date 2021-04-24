import smtplib
import ssl
from email.message import EmailMessage
import json
from pathlib import Path
from logging import getLogger

FILE_DIR = Path(__file__).parent.resolve()

logger = getLogger(__name__)


def send_msg(msg_body='', to=None, subject=None, attach=None, filename=''):

    logger.debug("-> send_msg %s %s %s %s", msg_body, to, subject, attach)

    with open(FILE_DIR/"config.json") as conf_file:
        config = json.load(conf_file)

    mail = EmailMessage()
    mail.set_content(msg_body)

    mail['From'] = config["from"]
    mail['To'] = to or config["send_to"]
    mail['Subject'] = subject or 'Sent using MailFS'

    if attach:
        mail.add_attachment(attach, filename=filename)

    smtp_config = config["smtp"]
    with(
        smtplib.SMTP_SSL(
            host=smtp_config["server"],
            port=int(smtp_config["port"]),
            context=ssl.create_default_context()
        ) as server
    ):

        server.login(smtp_config["user"], smtp_config["pass"])
        logger.debug(mail)
        server.send_message(mail)
        logger.debug("Sent Mail!")
