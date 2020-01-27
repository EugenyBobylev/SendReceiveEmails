import imaplib
import email
import base64
import re
from typing import List

ORG_EMAIL = "@gmail.com"
FROM_EMAIL = "ebobylev" + ORG_EMAIL
FROM_PWD = "Ujvbhrf1557"
SMTP_SERVER = "imap.gmail.com"
SMTP_PORT = 993


def from_base64(encoded: str) -> str:
    decoded: str = base64.b64decode(encoded)
    return decoded


def parse_list_response(line: bytes):
    str_line = line.decode('utf-8')
    pattern = r'\((?P<flags>.*?)\) "(?P<delimiter>.*)" (?P<name>.*)'
    regex = re.compile(pattern)
    flags, delimiter, mailbox_name = regex.match(str_line).groups()
    mailbox_name = mailbox_name.strip('"')
    return flags, delimiter, mailbox_name


def listing_mailbox():
    mail: imaplib.IMAP4_SSL= None
    try:
        mail = imaplib.IMAP4_SSL(SMTP_SERVER)
        mail.login(FROM_EMAIL, FROM_PWD)
        typ, data = mail.list()
    except Exception as ex:
        print(ex)
    finally:
        if mail is None:
            return
        mail.logout()
    print(f"Response code: {typ}")
    for line in data:
        flags, delimiter, mailbox_name = parse_list_response(line)
        print(f"{flags} {delimiter} {mailbox_name}")


def read_email_from_gmail():
    try:
        mail = imaplib.IMAP4_SSL(SMTP_SERVER)
        mail.login(FROM_EMAIL, FROM_PWD)

        typ, data = mail.list()

        mail.select('inbox')
        data = mail.search(None, 'ALL')
        mail_ids = data[0]

        id_list = mail_ids.split()
        first_email_id = int(id_list[0])
        latest_email_id = int(id_list[-1])

        for i in range(latest_email_id, first_email_id, -1):
            data = mail.fetch(i, '(RFC822)')

            for response_part in data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_string(response_part[1])
                    email_subject = msg['subject']
                    email_from = msg['from']
                    print('From : ' + email_from + '\n')
                    print('Subject : ' + email_subject + '\n')

    except Exception as e:
        print("Возникло прерывание")
        print(e)


if __name__ == '__main__':
    listing_mailbox()
    #read_email_from_gmail()