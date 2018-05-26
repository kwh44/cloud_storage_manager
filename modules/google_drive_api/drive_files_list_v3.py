from __future__ import print_function
import os

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

files_list = []

Files = DRIVE.files().list().execute().get('files', [])
for i in Files:
	if i['mimeType'] == 'application/vnd.google-apps.folder':
		files_list.append((i['name'], i['id'], i['mimeType']))

files_list.sort(key=lambda x: x[0])

print(help(DRIVE.files().update))