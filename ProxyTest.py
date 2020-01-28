from __future__ import print_function
import base64
import email
import pickle
import os.path
from apiclient import errors
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def get_message(service, user_id, msg_id):
    try:
        message = service.users().messages().get(userId=user_id, id=msg_id).execute()
        return message
    except errors.HttpError as ex:
        print(f'An error occurred: \"{ex}\"')


def get_mime_message(service, user_id, msg_id):
    try:
        message = service.users().messages().get(userId=user_id, id=msg_id, format='raw').execute()
        print(f'{message["snippet"]}')
        msg_str = base64.urlsafe_b64decode(message['raw'].encode('utf-8')).decode("utf-8")
        mime_msg = email.message_from_string(msg_str)
        return mime_msg
    except errors.HttpError as exc:
        print(f'An error occurred: {exc}')


def get_attachments(service, user_id, msg_id, store_dir):
    try:
        message = service.users().messages().get(userId=user_id, id=msg_id).execute()
        for part in message['payload']['parts']:
            if part['filename']:
                body = part['body']
                file_data = base64.urlsafe_b64decode(body['attachmentId'])
                path = ''.join([store_dir, part['filename']])
                f = open(path, 'wb')
                f.write(file_data)
                f.close()
    except Exception as ex:
        print(f'An error occured: {ex}')


def get_service():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            #flow = InstalledAppFlow.from_client_secrets_file('SendReceiveEmail-352a90d376f2.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)
    return service


def get_all_income_emails(service):
    # Call the Gmail API
    results = service.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])

    # Query the service object to get User Profile
    userInfo = service.users().getProfile(userId='me').execute()
    print("UserInfo is \n %s" % (userInfo))

    # Call the Gmail API to fetch INBOX
    results = service.users().messages().list(userId='me', labelIds=['INBOX']).execute()
    messages = results.get('messages', [])

    if not messages:
        print('No messages found.')
    else:
        print('Messages:')
        for message in messages:
            msg = get_message(service, user_id='me', msg_id=message['id'])
            print(f"id= {msg['id']}; snippet= {msg['snippet']}")


if __name__ == '__main__':
    srv = get_service()
    #get_all_income_emails(srv)

    email_id = '16fe94817cda70f1'
    #msg = get_message(srv, 'me', email_id)
    #print(msg['snippet'])
    get_attachments(srv, 'me', email_id, '')

    #mime_msg = get_mime_message(srv, 'me', email_id)

