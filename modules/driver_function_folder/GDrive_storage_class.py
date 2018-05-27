from __future__ import print_function

import io
import os
from mimetypes import MimeTypes
from apiclient import discovery
from apiclient.http import MediaFileUpload, MediaIoBaseDownload
from googleDocFormats import GoogleDocFormats as GDF
from httplib2 import Http
from oauth2client import file, client, tools


class GDrive_Storage:
    _format_list = [(i, GDF[i][0]) for i in GDF]

    def __init__(self):
        """Initialize attributes for only internal use"""
        self.__drive = None
        pass

    @property
    def drive_handle(self):
        return self.__drive

    def link_account(self):
        """Return True if the the user's Google Drive account was successfully
         connected, otherwise False"""
        SCOPES = 'https://www.googleapis.com/auth/drive'
        store = file.Storage('storage.json')
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
            credentials = tools.run_flow(flow, store)
        self.__drive = discovery.build('drive', 'v3', http=credentials.authorize(Http()))

    def unlink_account(self):
        """Return True if the user's Google Drive account was successfully disconnected, otherwise False"""
        try:
            os.remove("/storage.json")
            return True
        except:
            return False

    def create_folder(self, name):
        """Return True if the creation of empty folder in user's Google
        Drive storage was successful, otherwise False."""
        file_metadata = {
            'name': name,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        file = self.__drive.files().create(body=file_metadata,
                                           fields='id').execute()
        return True if file else False

    def __display_doc_formats(self):
        print(self._format_list[:6])
        print(self._format_list[6:11])
        print(self._format_list[11:18])

    def upload_file(self, local_file, parent=None):
        """Return True if the upload of the file was successful, otherwise False"""
        mime = MimeTypes()
        name = self._get_filename_from_path(local_file)
        file_metadata = {'name': name,
                         'parents': [self.search(parent) if parent else 'root']}
        media = MediaFileUpload(name, mimetype=mime.guess_type(name), resumable=True)
        try:
            file = self.__drive.files().create(body=file_metadata,
                                               media_body=media,
                                               fields='id').execute()
        except Exception as e:
            print(e.args)
            print("An error occurred, while uploading file, please try again.")
            return False
        return True

    def _get_filename_from_path(self, path):
        name = []
        for i in path[::-1]:
            if i == '/':
                break
            name.append(i)
        return "".join(name[::-1])

    # to be added
    def delete_file(self, id):
        """Return True if the deletion was successfully executed, otherwise False"""
        try:
            self.__drive.files().delete(fileId=id).execute()
            return True
        except:
            print("Invalid ID was entered.")
            return False

    def sync(self, id, local_file, mimetype=None, resume=True):
        """Return True if the local synchronization of files was successfully executed, otherwise False."""
        try:
            media = MediaFileUpload(local_file, mimetype=mimetype, resumable=resume)
            self.__drive.files().update(fileId=id, body={'name': self._get_filename_from_path(local_file)},
                                        media_body=media)
            return True
        except:
            print("An error occurred, please try again.")
            return False

    def search(self, query_name):
        """Returns id and download link of the file if it was uploaded
         to the Google Drive storage, otherwise False."""
        for i in self.__drive.files().list().execute().get('files', []):
            if i['name'] == query_name:
                return i['id']

    def download_file(self, name_extension, id):
        """Return link to download contents of the path, otherwise False"""
        try:
            request = self.__drive.files().get_media(fileId=id)
        except:
            print("Invalid id, please try again.")
            return False
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        download_succeeded = False
        while not download_succeeded:
            download_succeeded = downloader.next_chunk()
        with open(name_extension, 'wb') as file:
            file.write(fh.getvalue())
