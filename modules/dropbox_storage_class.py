import time
import webbrowser

from dropbox import Dropbox
from dropbox import DropboxOAuth2FlowNoRedirect
from dropbox.exceptions import ApiError
from dropbox.files import WriteMode


class DropBoxStorage:
    def __init__(self):
        """Initialize the class object with attribute only for internal use."""
        self._APP_KEY = 'orl3775x8jdgcg0'
        self._APP_SECRET = 'cgz8tvz8k4uiubx'
        self._dbx_user_account = None
        self._access_token = None

    @property
    def access_token(self):
        """Return reference to the only internal attribute"""
        return self._access_token

    @property
    def dbx_user_account(self):
        """Return user's Dropbox account information"""
        return self._dbx_user_account.users_get_current_account()

    def link_account(self):
        """Link user's Dropbox storage, in case of failure return False,
        indicating that the error occurred."""
        auth_flow = DropboxOAuth2FlowNoRedirect(self._APP_KEY,
                                                self._APP_SECRET)
        authorize_url = auth_flow.start()
        print("You will be redirected to the authorization page.")
        print("Copy the authorization code and paste it to the terminal window.")
        time.sleep(3)
        webbrowser.open(authorize_url)
        auth_code = input("Enter the code: ").strip()
        try:
            oauth_result = auth_flow.finish(auth_code)
            self._access_token = oauth_result.access_token
            self._dbx_user_account = Dropbox(self._access_token)
            return True
        except Exception as e:
            print('Error:% s' % e, )
            return False

    def unlink_account(self):
        """Delete user's access tokens"""
        self._access_token = None
        self._dbx_user_account = None
        return True

    def upload_file(self, local_file, backup_path):
        """Upload file to the path, specified by backup_path argument,
        in case of failure write the message to the stdout."""
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
        """Delete a file in the user's Dropbox storage"""
        try:
            self._dbx_user_account.files_delete_v2(self.search(filename))
            return True
        except Exception:
            print("File wasn't found in DropBox.")

    def sync(self, local_path):
        """Update the file in the user's Dropbox storage,
        if file wasn't found, write the message to the stdout."""
        try:
            backup_path = self.search(local_path.split('/')[-1])
            if '/' == local_path[0]:
                local_path = local_path[1:]
            self.upload_file(local_path, backup_path)
            print("Synchronized with Dropbox.")
        except:
            print("Failed to synchronize file with Dropbox.")

    def search(self, query_name):
        """Return the path to file if it was found in the user's Dropbox storage,
        otherwise return False, indicating that file wasn't found."""
        lst = [i.path_display for i in self._dbx_user_account.files_list_folder('', recursive=True).entries if
               query_name in i.path_display]
        if len(lst) > 0:
            return lst[0]
        else:
            return False

    def download_file(self, filename):
        """Open a link to download a file from the user's Dropbox storage,
        in case of failure returns False."""
        try:
            temp_file = self._dbx_user_account.files_get_temporary_link(self.search(filename))
            webbrowser.open(temp_file.link)
        except:
            return False

    def list_files(self):
        """Write to the stdout the list of all files in the user's Dropbox storage."""
        for i in self._dbx_user_account.files_list_folder('', recursive=True).entries:
            print(i.path_display.split('/')[-1])
