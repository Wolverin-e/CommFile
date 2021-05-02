import imaplib
import email
import csv
import json
from pathlib import Path
import time

FILE_DIR = Path(__file__).parent.resolve()


def get_text(msg):
    if msg.is_multipart():
        return get_text(msg.get_payload(0))
    else:
        return msg.get_payload(None, True)


try:
    last_read = -1
    while 1:
        with open(FILE_DIR/"config.json") as conf_file:
            config = json.load(conf_file)
        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        mail.login(config["smtp"]["user"], config["smtp"]["pass"])
        mail.select()
        return_code, data = mail.search(None, 'All')

        mail_ids = data[0].decode()
        id_list = mail_ids.split()
        latest_email_id = int(id_list[-1])

        if latest_email_id > last_read:

            with open('persons.csv', 'w', newline="") as csvfile:
                filewriter = csv.writer(
                    csvfile,
                    delimiter=',',
                    quotechar='|',
                    quoting=csv.QUOTE_MINIMAL)
                filewriter.writerow(['From', 'Subject'])
                typ, data = mail.fetch(str(latest_email_id), '(RFC822)')
                for response_part in data:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_string(
                            response_part[1].decode("utf-8"))
                        email_subject = msg['subject']
                        email_from = msg['from']
                        email_body = get_text(msg).decode("utf-8")
                        filewriter.writerow([
                            email_from,
                            email_subject,
                            email_body])

            last_read = latest_email_id
        mail.logout()
        time.sleep(1)

except Exception as e:
    print(e)
