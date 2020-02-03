from GMailApi import get_service, get_all_unread_emails, modify_message

if __name__ == '__main__':
    labels = {'removeLabelIds': ['UNREAD'], 'addLabelIds': []}
    srv = get_service()
    emails = get_all_unread_emails(srv)
    for msg in emails:
        print(f"id= {msg['id']}; snippet= {msg['snippet']}")
        modified_msg = modify_message(srv, user_id='me', msg_id=msg['id'], msg_labels=labels)
        if modified_msg is not None:
            print(f"{modified_msg['labelIds']}")
