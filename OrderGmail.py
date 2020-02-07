import base64
from time import sleep
from typing import List, Dict
from GMailApi import get_service, get_all_unread_emails, modify_message, get_all_income_emails
from GMailApi import create_mail, send_gmail
from mailparser import create_persons_from_mail_data
from models import Person
from repo import Repo


def mark_as_readed(service, msg_id) -> None:
    labels = {'removeLabelIds': ['UNREAD'], 'addLabelIds': []}
    modified_msg = modify_message(service, user_id='me', msg_id=msg_id, msg_labels=labels)
    if modified_msg is not None:
        print(f"{modified_msg['labelIds']}")


def read_all_new_emails(service) -> List:
    result = list()
    emails = get_all_unread_emails(service)
    for email in emails:
        mark_as_readed(service, email['id'])
        msg = parse_email(email)
        result.append(msg)
    return result


def read_all_emails(service) -> List:
    result = list()
    emails = get_all_income_emails(service)
    for email in emails:
        msg = parse_email(email)
        result.append(msg)
    return result


def decode_mail_str(encoded_str: str) -> str:
    decoded_bytes = base64.urlsafe_b64decode(encoded_str)
    decoded_str = decoded_bytes.decode('utf-8')
    return decoded_str


def parse_mail_part(part)-> str:
    type = part["mimeType"]
    if part["mimeType"] == 'multipart/alternative':
        return parse_mail_part(part['parts'][0])
    if type == 'text/html' or type == 'text/plain':
        body = part['body']
        encoded_data = body['data']
        decoded_data = decode_mail_str(encoded_data)
    return decoded_data


def parse_email(message) -> Dict[str, str]:
    result={'id': message['id'], 'snippet': message['snippet'], 'from': '', 'to': '', 'subject': '', 'date': ''}
    result['snippet'] = parse_mail_part(message['payload'])
    headers: List[Dict] = message['payload']['headers']
    for header in headers:
        if header['name'] == 'From':
            result['from'] = header['value']
        elif header['name'] == 'To':
            result['to'] = header['value']
        elif header['name'] == 'Subject':
            result['subject'] = header['value']
        elif header['name'] == 'Date':
            result['date'] = header['value']
    return result


def print_email_data(data: Dict) -> None:
    print(f"From={data['from']}; To={data['to']}; "
          f"Subject=\"{data['subject']}\" message =\"{data['snippet']}\"")


def create_standart_message(input_data) -> str:
    msg = "Ваше сообщение получено и принято в работу! \r\n\r\n"
    msg += f"from={input_data['from']}\r\b"
    msg += f" date={input_data['date']}\r\b"
    msg += f"subject={input_data['subject']}\r\n"
    msg += f"text={input_data['snippet']}"
    return msg


def insert_persons(data_str) -> List[Dict[bool, Person]]:
    persons = create_persons_from_mail_data(data_str)
    results = repo.add_persons(persons)
    return results


def create_sql_insert_message(results) -> str:
    msg = "Ошибка добавления в Базу данных"
    if (results is not None) and len(results) > 0:
        msg = ""
        for result in results:
            if result['ok']:
                msg += f'Успешное добавление в Базу данных \r\n'
            else:
                msg += 'Ошибка добавления в Базу данных \r\n'
            msg += f'{result["person"]} \r\n'
    return msg


def update_persons(data_str) -> List[Dict[bool, Person]]:
    persons = create_persons_from_mail_data(data_str)
    results = repo.update_persons(persons)
    return results


def create_sql_update_message(results):
    msg = "Ошибка обновления Базы данных"
    if (results is not None) and len(results) > 0:
        msg = ""
        for result in results:
            if result['ok']:
                msg += f'Успешное обновление Базы данных \r\n'
            else:
                msg += 'Ошибка обновления Базы данных \r\n'
            msg += f'{result["person"]} \r\n'
    return msg


def create_output_message(input_data) -> str:
    msg = ""
    subject: str = input_data['subject']
    snippet: str = input_data['snippet']
    if subject.lower() == "nsert":
        results = insert_persons(snippet)
        msg = create_sql_insert_message(results)
    elif subject.lower() == "update":
        results = update_persons(snippet)
        msg = create_sql_update_message(results)
    else:
        msg = create_standart_message(input_data)
    return msg


def create_response(input_data: Dict) -> Dict:
    to: str = input_data['from']
    to = to[to.index('<'):]
    snippet = create_output_message(input_data)
    result = {
        'from': 'bobylev.e.a@gmail.com',
        'to': to,
        'subject': f'Подтверждение входящего письма id={input_data["id"]}',
        'snippet': snippet
    }
    return result


if __name__ == '__main__':
    repo = Repo()
    while True:
        srv = get_service()
        all_email_data: List[Dict] = read_all_new_emails(srv)
        for email_data in all_email_data:
            response = create_response(email_data)
            print(f"to={response['to']}; subject={response['subject']}\n"
                  f"snippet={response['snippet']}")
            mail_msg = create_mail(sender=response['from'],
                                   to=response['to'],
                                   subject=response['subject'],
                                   text=response['snippet'])
            send_gmail(srv, 'me', mail_msg)
        sleep(12)
