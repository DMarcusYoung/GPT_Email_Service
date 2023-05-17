from __future__ import print_function

import os.path
import base64

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from bs4 import BeautifulSoup

from gpt import emailSummary

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def getLastEmail(n=5):
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        # Call the Gmail API
        service = build('gmail', 'v1', credentials=creds)
        results = service.users().messages().list(userId='me').execute()
        messages = results.get('messages', [])

        emails = []
        if not messages:
            print('No messages found.')
            return
        for i in range(n):
            message = service.users().messages().get(userId='me', id=messages[i]['id']).execute()
            payload = message['payload']
            headers = payload['headers']

            subject = ''
            sender = ''
            for d in headers:
                if d['name'] == 'Subject':
                    subject = d['value']
                if d['name'] == 'From':
                    sender = d['value']
    
            # The Body of the message is in Encrypted format. So, we have to decode it.
            # Get the data and decode it with base 64 decoder.
            
            parts = payload.get('parts')
            if not parts:
                print('No Message found.')
                emails.append([None, None, None])
                continue
            parts = parts[0]
            data = parts['body']['data']
            data = data.replace("-","+").replace("_","/")
            decoded_data = base64.b64decode(data)

            # Now, the data obtained is in lxml. So, we will parse 
            # it with BeautifulSoup library
            # print(decoded_data)
            # soup = BeautifulSoup(decoded_data, features="html.parser")
            soup = BeautifulSoup(decoded_data , "lxml")
            body = soup.body()

            emails.append([subject, sender, body])

        return emails
    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f'An error occurred: {error}')

def main():
    emails = getLastEmail(2)

    summaries = emailSummary(emails)
    print(summaries)

if __name__ == '__main__':
    main()