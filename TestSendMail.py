from SendEmail import send_gmail_com, get_attach_image, get_plain_mimie, get_attach_mime
from GMailApi import get_service, send_gmail

if __name__ == '__main__':
    send_from = "ebobylev.e.e@gmail.com"
    send_to = ["beabooks@mail.ru"]
    subject = "Проверка отсылки (docx)"
    message = """
Это электронное письмо было послано самому себе в исключительно отладочных целях.
Оно может содержать различные типы вложений как-то: двоичные файлы, изображения и т.д.
PS. Отправка письма возможно была сделана через gmail api
"""

    msg_root = get_plain_mimie(send_from, send_to, subject, message)
    #print(msg_root)
    msg_attaches = get_attach_mime(['C:\\Users\\Bobylev\\Downloads\\ТЗ_на_xls.docx'])
    for msg_attach in msg_attaches:
        msg_root.attach(msg_attach)

    service = get_service()
    send_gmail(service,'me',msg_root)

    #msg_attaches = get_attach_mime(["d:\\Книги\\Python\\Шпаргалка по Python.pdf",
    #                                "d:\\Книги\\Python\\info.docx"])
    #msg_images = get_attach_image(["2.jpg"])


    #for img in msg_images:
    #    msg_root.attach(img)

    #send_mail_ru(send_from, send_to, msg_root)
    #send_gmail_com(send_from, send_to, msg_root)
