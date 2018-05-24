class DropBoxStorage:
    def __init__(self):
        self._APP_KEY = 'orl3775x8jdgcg0'
        self._APP_SECRET = 'cgz8tvz8k4uiubx'
        self._access_token = None

    @property
    def access_token(self):
        return self._access_token

    @access_token.setter
    def access_token(self, value):
        self._access_token = value

    def upload_file(self, path):
        # call a function
        #
        pass

    def delete_file(self, name):
        # call a function to delete a file or folder
        pass

    def update_file(self, name):
        # call a function to delete a file of folder
        pass