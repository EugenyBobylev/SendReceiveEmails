from time import sleep
from typing import List, Dict
from GMailApi import get_service, get_all_unread_emails, modify_message, get_all_income_emails
from GMailApi import create_mail, send_gmail


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


def parse_email(message) -> Dict:
    result={'id':message['id'], 'snippet':message['snippet'],'from':'','to':'','subject':'', 'date':''}
    result['snippet'] = message['snippet']
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


def create_output_message(input_data) -> str:
    msg = "Ваше сообщение получено и принято в работу! \r\n\r\n"
    msg += f"from={input_data['from']}\r\b"
    msg += f" date={input_data['date']}\r\b"
    msg += f"subject={input_data['subject']}\r\n"
    msg += f"text={input_data['snippet']}"
    return msg


def create_response(input_data: Dict) -> Dict:
    to:str = input_data['from']
    to = to[to.index('<'):]
    result = {
        'from':'bobylev.e.a@gmail.com',
        'to':to,
        'subject':f'Подтверждение входящего письма id={input_data["id"]}',
        'snippet': create_output_message(input_data)
    }
    return result


if __name__ == '__main__':
    while True:
        srv = get_service()
        all_email_data:List[Dict] = read_all_new_emails(srv)
        for email_data in all_email_data:
            response = create_response(email_data)
            mail_msg = create_mail(sender=response['from'],to=response['to'],
                                    subject=response['subject'],text=response['snippet'])
            send_gmail(srv,'me', mail_msg)
            print(f"to={response['to']}; subject={response['subject']}")
        sleep(12)