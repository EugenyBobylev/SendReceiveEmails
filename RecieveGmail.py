from typing import List, Dict

from GMailApi import get_service, get_all_unread_emails, modify_message, get_all_income_emails


def read_all_new_emails(service) -> None:
    labels = {'removeLabelIds': ['UNREAD'], 'addLabelIds': []}
    emails = get_all_unread_emails(service)
    for msg in emails:
        print(f"id= {msg['id']}; snippet= {msg['snippet']}")
        modified_msg = modify_message(service, user_id='me', msg_id=msg['id'], msg_labels=labels)
        if modified_msg is not None:
            print(f"{modified_msg['labelIds']}")



def read_all_emails(service) -> None:
    emails = get_all_income_emails(service)
    for msg in emails:
        msg_from: str = ""
        msg_to: str = ""
        msg_subject = ""
        msg_date = ""
        headers: List[Dict] = msg['payload']['headers']
        for header in headers:
            if header['name'] == 'From':
                msg_from = header['value']
            elif header['name'] == 'To':
                msg_to = header['value']
            elif header['name'] == 'Subject':
                msg_subject = header['value']
            elif header['name'] == 'Date':
                msg_date = header['value']
        print(f"Id={msg['id']}; From={msg_from}; To={msg_to}; Date={msg_date}; Subject=\"{msg_subject}\" message =\"{msg['snippet']}\"")

if __name__ == '__main__':
    srv = get_service()
    read_all_emails(srv)
