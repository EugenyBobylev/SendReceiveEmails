from SendEmail import send_mail_ru, get_attach_image, get_plain_mimie, get_attach_mime

if __name__ == '__main__':
    send_from = "masternz@mail.ru"
    send_to = ["ebobylev@gmail.com", "beabooks@mail.ru", ]
    subject = "SMTP e-mail тест"
    message = """
Это электронное письмо было послано самому себе в исключительно отладочных целях.
Оно может содержать различные типы вложений как-то: двоичные файлы, изображения и т.д.
"""

    msg_root = get_plain_mimie(send_from, send_to, subject, message)
    msg_attaches = get_attach_mime(["d:\\Книги\\Python\\Шпаргалка по Python.pdf",
                                    "d:\\Книги\\Python\\info.docx"])
    msg_images = get_attach_image(["2.jpg"])

    for msg_attach in msg_attaches:
        msg_root.attach(msg_attach)

    for img in msg_images:
        msg_root.attach(img)

    send_mail_ru(send_from, send_to, msg_root)
    # send_gmail_com(send_from, send_to, msg_root)
    # print(msg_root)
