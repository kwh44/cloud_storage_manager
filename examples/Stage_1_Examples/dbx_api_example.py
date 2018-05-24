import dropbox


class DropBox:
    """
    Return information of a user whose access token is provided and
    the list of files on their Dropbox storage.
    """

    def __init__(self, token):
        '''Initialize the access token and createa an instance of Dropbox class from the dropbox module'''
        self.token = token
        self.dbx = dropbox.Dropbox(self.token)

    def account_info(self):
        '''Return all available information about the user provided the access token'''
        return self.dbx.users_get_current_account()

    def files_list(self):
        '''Print name of files in the specified user directory'''
        for file in self.dbx.files_list_folder('', recursive=True).entries:
            print(file.path_display)
        return 0


if __name__ == "__main__":
    dbx = DropBox('Mb8FAtKIhmAAAAAAAAAAKv5Nkai4U7MCyTvQvhINotDrbqj5Wqehrrmi2bkI_Lc7')
    print(dbx.account_info())
    dbx.files_list()
