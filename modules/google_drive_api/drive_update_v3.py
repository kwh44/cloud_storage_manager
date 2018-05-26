from __future__ import print_function
import os

from apiclient.http import MediaFileUpload
from apiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools

SCOPES = 'https://www.googleapis.com/auth/drive'
store = file.Storage('storage.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store)
DRIVE = discovery.build('drive', 'v3', http=creds.authorize(Http()))

id = tuple(i['id'] for i in DRIVE.files().list().execute().get('files', []) if i['name'] == 'hello.txt')[0]


file = DRIVE.files().get(fileId=id).execute()

media_body = MediaFileUpload('delusion_come_back.txt', mimetype=None, resumable=True)

DRIVE.files().update(fileId=id, body={'name':'delusion_come_back.txt'}, media_body=media_body).execute()
