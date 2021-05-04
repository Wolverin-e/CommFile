import imaplib
import email
import json
from pathlib import Path

FILE_DIR = Path(__file__).parent.resolve()


def get_text(msg):
    if msg.is_multipart():
        return get_text(msg.get_payload(0))
    else:
        return msg.get_payload(None, True)


def receive():
    unread_msg = ""
    delimiter = '**********************\n\n'
    with open(FILE_DIR/"config.json") as conf_file:
        config = json.load(conf_file)
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(config["smtp"]["user"], config["smtp"]["pass"])
    mail.select()
    _, data = mail.search(None, 'UnSeen')

    mail_ids = data[0].decode()
    id_list = mail_ids.split()
    first_email_id = int(id_list[0])
    latest_email_id = int(id_list[-1])

    count = 0
    for i in range(latest_email_id, first_email_id, -1):
        _, data = mail.fetch(str(i), '(RFC822)')
        for response_part in data:
            if isinstance(response_part, tuple):
                msg = email.message_from_string(
                    response_part[1].decode("utf-8")
                )
                email_subject = str(msg['subject'])
                email_from = str(msg['from'])
                email_body = str(get_text(msg).decode("utf-8"))
                unread_msg = '\n'.join([
                    unread_msg,
                    email_from,
                    email_subject,
                    email_body,
                    delimiter
                ])
        count += 1
        if count >= 1:
            break

    mail.logout()
    return unread_msg
