import sys
import dropbox
from dropbox.files import WriteMode
from dropbox.exceptions import ApiError
from dropbox import Dropbox
from dropbox import DropboxOAuth2FlowNoRedirect


class DropBoxStorage:
    def __init__(self):
        """Initialize attributes for only internal use"""
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
        """Return True if the the user's Dropbox account was successfully connected, otherwise False"""
        auth_flow = DropboxOAuth2FlowNoRedirect(self._APP_KEY,
                                                self._APP_SECRET)
        authorize_url = auth_flow.start()
        print("1. Visit: " + authorize_url)
        print("2. Copy the authorization code (you might have to log in first)")
        print("3. Paste the authorization code in stdout")
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
        """Return True if the user's Dropbox account was successfully disconnected, otherwise False"""
        self._access_token = None
        self._dbx_user_account = None
        return True

    def upload(self, local_file, backup_path):
        """Return True if the upload of the file was successful, otherwise False"""
        with open(local_file, 'rb') as f:
            try:
                self._dbx_user_account.files_upload(f.read(), backup_path, mode=WriteMode('overwrite'))
                return True
            except ApiError as err:
                if (err.error.is_path() and
                        err.error.get_path().error.is_insufficient_space()):
                    sys.exit("ERROR: Cannot back up; insufficient space.")
                elif err.user_message_text:
                    print(err.user_message_text)
                else:
                    print(err)
                return False

    def delete_file(self, path):
        """Return True if the deletion was successfully executed, otherwise False"""
        try:
            self._dbx_user_account.files_delete_v2(path)
            return True
        except Exception:
            return False

    def sync(self):
        """Return True if the local synchronization of files was successfully executed, otherwise False."""
        lst = self._dbx_user_account.files_list_folder('', recursive=True).entries
        file_id = dict(
            (i, lst[i].path_display) for i in range(len(lst)) if type(lst[i]) is not dropbox.files.FolderMetadata)
        print(file_id)
        option_id = [i.strip() for i in input("Enter the number of files to synchronize locally(1, 11,...): ").split(',')]
        for key in option_id:
            local_path = input(
                "Enter the local path of {}: ".format(file_id[int(key)][-file_id[int(key)][::-1].index('/'):]))
            try:
                self.upload(local_path, file_id[int(key)])
            except Exception:
                return False
        return True

    def search(self, query_name):
        """Returns path to the file if it was uploaded to the Dropbox storage, otherwise False."""
        lst = [i.path_display for i in self._dbx_user_account.files_list_folder('', recursive=True).entries if
               query_name in i.path_display]
        if len(lst) > 0:
            return lst[0]
        else:
            return False

    def download_file(self, id):
        """Return link to download contents of the path, otherwise False"""
        try:
            temp_file = self._dbx_user_account.files_get_temporary_link(self.search(id))
            return temp_file.link
        except Exception:
            return False

if __name__ == "__main__":
    obj = DropBoxStorage()
    obj.link_account()
    print(obj.search('hello.txt'))
    obj.sync()

