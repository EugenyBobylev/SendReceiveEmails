import os, smtplib, ssl
from typing import List
from email import encoders
from email.header import Header
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate

COMMASPACE = ', '


def get_plain_mimie(send_from, send_to: List[str], subject, message: str) -> MIMEMultipart:
    assert type(send_to) == list, 'send_to должен быть списком строк'
    msg = MIMEMultipart('alternative')
    msg.set_charset('utf-8')
    msg['From'] = f"Eugeny Bobylev <{send_from}>"
    msg['To'] = COMMASPACE.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = Header(subject, 'utf-8')
    msg.attach(MIMEText(message, "plain"))
    return msg


def get_attach_mime(attachments: List[str]) -> List[MIMEBase]:
    messages = list()
    assert type(attachments) == list, 'attachments должен быть списком'
    for attachment in attachments:
        fname = os.path.basename(attachment)
        with(open(attachment, 'rb')) as f:
            msg = MIMEBase("application", "octet-stream")
            msg.set_payload(f.read())
        encoders.encode_base64(msg)
        msg.add_header("Content-Disposition", "attachment",
                       filename=(Header(fname, "utf-8").encode()))
        messages.append(msg)
    return messages


def get_attach_image(attachments: List[str]) -> List[MIMEImage]:
    messages = list()
    assert type(attachments) == list, 'attachments должен быть списком'
    for attachment in attachments:
        fname = os.path.basename(attachment)
        with(open(attachment, 'rb')) as fb:
            img = MIMEImage(fb.read(), name=fname)
        messages.append(img)
    return messages


def send_mail_ru(send_from, send_to, mime: MIMEMultipart):
    with smtplib.SMTP_SSL("smtp.mail.ru", port=465) as server:
        server.login(send_from, "Ujvbhrf1557")
        server.sendmail(send_from, send_to, mime.as_string())


def send_gmail_com(send_from, send_to, mime: MIMEMultipart):
    context = ssl.create_default_context()
    with smtplib.SMTP("smtp.gmail.com", port=587) as server:
        server.ehlo()
        server.starttls(context=context)
        server.ehlo()
        server.login("ebobylev@gmail.com", "Ujvbhrf1557")
        server.sendmail(send_from, send_to, mime.as_string())
