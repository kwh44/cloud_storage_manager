import time
import webbrowser

from dropbox import Dropbox
from dropbox import DropboxOAuth2FlowNoRedirect
from dropbox.exceptions import ApiError
from dropbox.files import WriteMode


class DropBoxStorage:
    def __init__(self):
        self._APP_KEY = 'orl3775x8jdgcg0'
        self._APP_SECRET = 'cgz8tvz8k4uiubx'
        self._dbx_user_account = None
        self._access_token = None

    @property
    def access_token(self):
        return self._access_token

    @property
    def dbx_user_account(self):
        return self._dbx_user_account.users_get_current_account()

    def link_account(self):
        auth_flow = DropboxOAuth2FlowNoRedirect(self._APP_KEY,
                                                self._APP_SECRET)
        authorize_url = auth_flow.start()
        print("In 5 seconds you will be redirected to authrorization page.")
        print("Copy the authorization code (you might have to log in first).")
        print("Paste the authorization code in stdout.")
        time.sleep(5)
        webbrowser.open(authorize_url)
        auth_code = input("Enter the authorization code here: ").strip()
        try:
            oauth_result = auth_flow.finish(auth_code)
            self._access_token = oauth_result.access_token
            self._dbx_user_account = Dropbox(self._access_token)
            return True
        except Exception as e:
            print('Error:% s' % e, )
            return False

    def unlink_account(self):
        self._access_token = None
        self._dbx_user_account = None
        return True

    def upload_file(self, local_file, backup_path):
        try:
            with open(local_file, mode='rb') as f:
                try:
                    self._dbx_user_account.files_upload(f.read(), backup_path, mode=WriteMode('overwrite'))
                    return True
                except ApiError as err:
                    print("Error occurred while uploading file to Dropbox.")
        except:
            print("Error occurred while opening local file.")

    def delete_file(self, filename):
        try:
            self._dbx_user_account.files_delete_v2(self.search(filename))
            return True
        except Exception:
            print("File wasn't found in DropBox.")

    def sync(self, local_path):
        try:
            backup_path = self.search(local_path.split('/')[-1])
            if '/' == local_path[0]:
                local_path = local_path[1:]
            self.upload_file(local_path, backup_path)
            print("Synchronized with Dropbox.")
        except:
            print("Failed to synchronize file with Dropbox.")

    def search(self, query_name):
        lst = [i.path_display for i in self._dbx_user_account.files_list_folder('', recursive=True).entries if
               query_name in i.path_display]
        if len(lst) > 0:
            return lst[0]
        else:
            return False

    def download_file(self, filename):
        try:
            temp_file = self._dbx_user_account.files_get_temporary_link(self.search(filename))
            webbrowser.open(temp_file.link)
        except:
            return False

    def list_files(self):
        for i in self._dbx_user_account.files_list_folder('', recursive=True).entries:
            print(i.path_display.split('/')[-1])
