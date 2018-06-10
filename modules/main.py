import sys

from GDrive_storage_class import GDrive_Storage
from dropbox_storage_class import DropBoxStorage


class CloudStorageManager:
    def __init__(self):
        self.google_drive_account = GDrive_Storage()
        self.google_drive_account_status = 0
        self.dropbox_account = DropBoxStorage()
        self.dropbox_account_status = 0

    def connect_google_drive(self):
        self.google_drive_account.link_account()
        self.google_drive_account_status = 1

    def connect_dropbox_storage(self):
        self.dropbox_account.link_account()
        self.dropbox_account_status = 1

    def disconnect_google_drive(self):
        self.google_drive_account.unlink_account()
        self.google_drive_account_status = 0

    def disconnect_dropbox_storage(self):
        self.dropbox_account.unlink_account()
        self.dropbox_account_status = 0

    def _get_filename_from_backup_path(self, path):
        name = []
        counter = 0
        for i in path[::-1]:
            if counter and i != '/':
                name.append(i)
            if i == '/':
                counter += 1
            if counter > 1: break
        return "".join(name[::-1])

    def upload_file(self, local_path, backup_path, storage):
        if storage:
            if backup_path:
                backup_path = [i for i in backup_path.split('/')[1:] if i]
                self.google_drive_account.upload_file(local_path, backup_path)
            else:
                self.google_drive_account.upload_file(local_path)
        else:
            backup_path += '/' + local_path.split('/')[-1]
            self.dropbox_account.upload_file(local_path, backup_path)

    def download_file(self, filename, storage):
        if storage == 1:
            self.google_drive_account.download_file(filename)
        elif storage == 0:
            self.dropbox_account.download_file(filename)
        else:
            self.google_drive_account.download_file(filename)
            self.dropbox_account.download_file(filename)

    def sync(self, filename, storage):
        if storage == 1:
            self.google_drive_account.sync(filename)
        elif storage == 0:
            self.dropbox_account.sync(filename)
        else:
            self.google_drive_account.sync(filename)
            self.dropbox_account.sync(filename)

    def delete_file(self, filename):
        self.dropbox_account.delete_file(filename)
        self.google_drive_account.delete_file(filename)

    def list_files(self):
        if self.dropbox_account_status:
            print("Dropbox files list:")
            self.dropbox_account.list_files()
        if self.google_drive_account_status:
            print("Google Drive files list:")
            self.google_drive_account.list_files()

    def menu(self):
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
                Menu
                
    1: Connect Dropbox account.\n
    2: Connect GoogleDrive account.\n
    3: Upload File.\n
    4: Download Files.\n
    5: Sync with local file.\n
    6: Delete file.\n
    7: Disconnect Dropbox account.\n
    8: Disconnect Google Drive account.\n
    9: List files.\n
    10: Exit
"""
        )
        option = int(input("Enter: "))
        if not (1 <= option <= 10):
            print('Invalid action chosen')
            return 0
        elif option == 10:
            sys.exit(0)
        elif option in [1, 2, 7, 8]:
            option_funct[option]()
        elif option == 6:
            self.delete_file(input('Enter the name of file to delete: '))
        else:
            if option == 3:
                storage = int(input("Google Drive - 1, Dropbox - 0 (skip if unimportant)? "))
                local_path = input("Enter the path to file: ")
                backup_path = input("To which folder to upload (root directory by default)? ")
                self.upload_file(local_path, backup_path, storage)
            elif option == 4:
                storage = int(input("Google Drive - 1, Dropbox - 0 (skip if you forgot)? "))
                filename = input("Enter the filename: ")
                self.download_file(filename, storage)
            elif option == 5:
                storage = int(input("Google Drive - 1, Dropbox - 0 (skip if you forgot)? "))
                local_path = input("Enter the local path to file: ")
                self.sync(local_path, storage)
            else:
                self.list_files()

    def run(self):
        while True:
            self.menu()


if __name__ == "__main__":
    app = CloudStorageManager()
    app.run()
