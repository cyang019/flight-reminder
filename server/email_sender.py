from __future__ import print_function
from email.mime.text import MIMEText
import oauth2client
from oauth2client import client, tools, file
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import base64
import pickle
import os
import httplib2


SCOPES = ['https://mail.google.com/', 'https://www.googleapis.com/auth/gmail.send']
APPLICATION_NAME = 'Gmail API Python Send Email'


def get_credentials():
    # If needed create folder for credential
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
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return creds


def create_message(sender, to, subject, message_text):
  """Create a message for an email.

  Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.

  Returns:
    An object containing a base64url encoded email object.
  """
  message = MIMEText(message_text)
  message['to'] = to
  message['from'] = sender
  message['subject'] = subject
  raw = base64.urlsafe_b64encode(message.as_bytes())
  raw = raw.decode()
  return {'raw': raw}

def send_message(service, message):
  try:
    message = (service.users().messages().send(userId='me', body=message)
               .execute())
    print('Message Id: %s' % message['id'])
    return message
  except Exception as e:
    print('An error occurred: %s' % e)


def create_n_send_message(sender, to, subject, message_text):
  credentials = get_credentials()
  # http = httplib2.Http()
  # http = credentials.authorize(http)

  service = build('gmail', 'v1', credentials=credentials)
  print('service created...')
  msg = create_message(sender, to, subject, message_text)
  send_message(service, msg)



def main():
  create_n_send_message('chen.yang.bytes@gmail.com', 'yangcnju@gmail.com', 'test api', 'hello')


if __name__ == '__main__':
    main()
