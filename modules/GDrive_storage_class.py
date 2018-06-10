import io
import os
from mimetypes import MimeTypes

from apiclient import discovery
from apiclient.http import MediaFileUpload, MediaIoBaseDownload
from httplib2 import Http
from oauth2client import file, client, tools


class GDrive_Storage:
    def __init__(self):
        self.__drive = None
        pass

    @property
    def drive_handle(self):
        return self.__drive

    def link_account(self):
        SCOPES = 'https://www.googleapis.com/auth/drive'
        store = file.Storage('storage.json')
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
            credentials = tools.run_flow(flow, store)
        self.__drive = discovery.build('drive', 'v3', http=credentials.authorize(Http()))

    def unlink_account(self):
        try:
            os.remove("/storage.json")
            return True
        except:
            return False

    def create_folder(self, name):
        file_metadata = {
            'name': name,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        file = self.__drive.files().create(body=file_metadata,
                                           fields='id').execute()
        return True if file else False

    def upload_file(self, local_file, parent=None):
        mime = MimeTypes()
        name = self._get_filename_from_path(local_file)
        parent = [self.search(i) for i in parent] if parent else 'root'
        file_metadata = {'name': name, 'parents': parent}
        media = MediaFileUpload(name, mimetype=mime.guess_type(name), resumable=True)
        try:
            file = self.__drive.files().create(body=file_metadata,
                                               media_body=media,
                                               fields='id').execute()
        except Exception as e:
            print("An error occurred while uploading file to Google Drive")
        return True

    def _get_filename_from_path(self, path):
        name = []
        for i in path[::-1]:
            if i == '/':
                break
            name.append(i)
        return "".join(name[::-1])

    def delete_file(self, filename):
        try:
            self.__drive.files().delete(fileId=self.search(filename)).execute()
        except:
            print("File wasn't found in Google Drive.")

    def sync(self, local_file):
        try:
            self.delete_file(self._get_filename_from_path(local_file))
            self.upload_file(local_file)
            print("Synchronized with Google Drive.")
        except:
            print("Failed to synchronize with Google Drive")

    def search(self, query_name):
        for i in self.__drive.files().list().execute().get('files', []):
            if i['name'] == query_name:
                return i['id']
        print("File wasn't found in Google Drive")

    def download_file(self, filename):
        try:
            request = self.__drive.files().get_media(fileId=self.search(filename))
        except:
            print("The file wasn't found in Google Drive.")
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        download_succeeded = False
        while not download_succeeded:
            download_succeeded = downloader.next_chunk()
        with open(filename, 'wb') as file:
            file.write(fh.getvalue())

    def list_files(self):
        for j in set(i['name'] for i in self.__drive.files().list().execute().get('files', [])):
            print(j)

