import socket
import sys

from GDrive_storage_class import GDrive_Storage
from dropbox_storage_class import DropBoxStorage


class CloudStorageManager:
    def __init__(self):
        """Initialize the class object with auxiliary class object as attributes and bool
         variables indicating connection status (whether or not the user's storage is linked)."""
        self.google_drive_account = GDrive_Storage()
        self.google_drive_account_status = 0
        self.dropbox_account = DropBoxStorage()
        self.dropbox_account_status = 0

    def connect_google_drive(self):
        """Link the user's Google Drive storage"""
        self.google_drive_account.link_account()
        self.google_drive_account_status = 1

    def connect_dropbox_storage(self):
        """Link the user's Dropbox storage"""
        self.dropbox_account.link_account()
        self.dropbox_account_status = 1

    def disconnect_google_drive(self):
        """Unlink the user's Google Drive storage"""
        self.google_drive_account.unlink_account()
        self.google_drive_account_status = 0

    def disconnect_dropbox_storage(self):
        """Unlink the user's Dropbox storage"""
        self.dropbox_account.unlink_account()
        self.dropbox_account_status = 0

    def _connected(self):
        try:
            socketInstance = socket.create_connection(("www.google.com", 80))
            socketInstance.close()
            return True
        except:
            return False

    def _alert(self):
        if not (self.google_drive_account_status or self.dropbox_account_status):
            print("None of the storage account was connected.")
            return True
        else:
            return False

    def upload_file(self, local_path, backup_path, storage):
        """Upload file to one of the user's cloud storages"""
        if storage and self.google_drive_account_status:
            if backup_path:
                backup_path = [i for i in backup_path.split('/') if i]
                self.google_drive_account.upload_file(local_path, backup_path)
            else:
                self.google_drive_account.upload_file(local_path)
        else:
            if self.dropbox_account_status:
                if '/' != backup_path[0]:
                    backup_path = '/' + backup_path
                if '/' != backup_path[-1]:
                    backup_path += '/'
                backup_path += local_path.split('/')[-1]
                self.dropbox_account.upload_file(local_path, backup_path)

    def download_file(self, filename, storage):
        """Download file from one of the user's cloud storages"""
        if storage == 1 and self.google_drive_account_status:
            self.google_drive_account.download_file(filename)
        elif storage == 0 and self.dropbox_account_status:
            self.dropbox_account.download_file(filename)
        else:
            if self.google_drive_account_status:
                self.google_drive_account.download_file(filename)
            if self.dropbox_account_status:
                self.dropbox_account.download_file(filename)

    def sync(self, filename, storage):
        """Update file's content in user's cloud storages"""
        if storage == 1 and self.google_drive_account_status:
            self.google_drive_account.sync(filename)
        elif storage == 0 and self.dropbox_account_status:
            self.dropbox_account.sync(filename)
        else:
            if self.google_drive_account_status:
                self.google_drive_account.sync(filename)
            if self.dropbox_account_status:
                self.dropbox_account.sync(filename)

    def delete_file(self, filename):
        """Delete file in user's cloud storages"""
        if self.dropbox_account_status:
            self.dropbox_account.delete_file(filename)
        if self.google_drive_account_status:
            self.google_drive_account.delete_file(filename)

    def list_files(self):
        """Write to the std all files in user's cloud storages"""
        if self.dropbox_account_status:
            print("Dropbox files list:")
            self.dropbox_account.list_files()
        if self.google_drive_account_status:
            print("Google Drive files list:")
            self.google_drive_account.list_files()

    def menu(self):
        """Present all the functionality available with the ability to choose an option."""
        option_funct = {
            1: self.connect_dropbox_storage,
            2: self.connect_google_drive,
            3: self.upload_file,
            4: self.download_file,
            5: self.sync,
            6: self.delete_file,
            7: self.disconnect_dropbox_storage,
            8: self.disconnect_google_drive
        }
        print(
            """
                Menu\n\n
    1: Connect Dropbox account.\n
    2: Connect GoogleDrive account.\n
    3: Upload File.\n
    4: Download Files.\n
    5: Sync with local file.\n
    6: Delete file.\n
    7: Disconnect Dropbox account.\n
    8: Disconnect Google Drive account.\n
    9: List files.\n
    10: Exit\n""")
        try:
            option = int(input("Enter: "))
        except:
            return 0
        if not (1 <= option <= 10):
            print('Invalid action chosen')
        elif option == 10:
            if self.google_drive_account_status:
                self.disconnect_google_drive()
            if self.dropbox_account_status:
                self.disconnect_dropbox_storage()
            sys.exit(0)
        elif option in (1, 2):
            option_funct[option]()
        elif option == 7:
            if not self.dropbox_account_status:
                return print("Dropbox storage wasn't connected.")
            option_funct[7]()
        elif option == 8:
            if not self.google_drive_account_status:
                return print("Google Drive storage wasn't connected.")
            option_funct[8]()
        elif self._alert():
            return
        elif option == 6:
            return self.delete_file(input('Enter the name of file to delete: '))
        else:
            if option == 3:
                try:
                    storage = int(input("Google Drive - 1, Dropbox - 0 (skip if unimportant)? "))
                except:
                    storage = -1
                local_path = input("Enter the path to file: ")
                backup_path = input("To which folder to upload (root directory by default)? ")
                self.upload_file(local_path, backup_path, storage)
            elif option == 4:
                try:
                    storage = int(input("Google Drive - 1, Dropbox - 0 (skip if you forgot)? "))
                except:
                    storage = -1
                filename = input("Enter the filename: ")
                self.download_file(filename, storage)
            elif option == 5:
                try:
                    storage = int(input("Google Drive - 1, Dropbox - 0 (skip if you forgot)? "))
                except:
                    storage = -1
                local_path = input("Enter the local path to file: ")
                self.sync(local_path, storage)
            else:
                self.list_files()

    def run(self):
        """Run the main routine"""
        while True:
            if self._connected():
                self.menu()
            else:
                return print("No internet connection.")


if __name__ == "__main__":
    app = CloudStorageManager()
    app.run()


    # Thank you 
