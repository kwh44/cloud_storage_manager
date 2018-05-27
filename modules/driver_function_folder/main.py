import sys

from GDrive_storage_class import GDrive_Storage
from dropbox_storage_class import DropBoxStorage


class CloudStorageManager:
    def __init__(self):
        self.google_drive_account = GDrive_Storage()
        self.dropbox_account = DropBoxStorage()

    def connect_google_drive(self):
        self.google_drive_account.link_account()

    def connect_dropbox_storage(self):
        self.dropbox_account.link_account()

    def disconnect_google_drive(self):
        self.google_drive_account.unlink_account()

    def disconnect_dropbox_storage(self):
        self.dropbox_account.unlink_account()

    def capacity_dropbox_storage(self):
        pass

    def capacity_google_drive_storage(self):
        pass

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
        try:
            if storage:
                if backup_path:
                    backup_path = self._get_filename_from_backup_path(backup_path)
                self.google_drive_account.upload_file(local_path, backup_path)
            else:
                backup_path += local_path[len(local_path) - local_path[::-1].find('/'):]
                self.dropbox_account.upload_file(local_path.backup_path)
        except:
            print("An error occurred. Please, try again.")

    def download_file(self, filename, storage):
        if storage:
            self.google_drive_account(filename)
        else:
            print("To complete downloading file visit the link")
            print("{}".format(self.dropbox_account.download_file(filename)))

    def sync(self, filename, backup_path, storage):
        pass

    def delete_file(self, filename):
        try:
            self.dropbox_account.delete_file(filename)
            return True
        except:
            try:
                self.google_drive_account.delet_file(filename)
                return True
            except:
                print("File wasn't found.")
                return False

    def menu(self):
        option_funct = {1: self.connect_dropbox_storage, 2: self.connect_google_drive,
                        3: self.upload_file, 4: self.download_file, 5: self.sync,
                        6: self.delete_file, 7: self.disconnect_dropbox_storage,
                        8: self.disconnect_google_drive}
        menu_str = """
		Menu:
		1: Connect Dropbox account.\n
		2: Connect GoogleDrive account.\n
		3: Upload File.\n
		4: Download Files.\n
		5: Sync with local file.\n
		6: Delete file.\n
		7: Disconnect Dropbox account.\n
		8: Disconnect Google Drive account.\n
		9: Exit"""
        option = int(input("Enter: "))
        if not (1 <= option <= 9):
            print('Invalid action chosen')
            return 0
        if option == 9:
            sys.exit(0)
        if option in [1, 2, 7, 8]:
            option_funct[option]()
        if option == 6:
            self.delete_file(input('Enter the name of file to delete: '))
        storage = int(input("Google Drive - 0, Dropbox - 1? "))
        if option == 3:
            local_path = input("Enter the path to file: ")
            backup_path = input("To which folder to upload (root directory by default)? ")
            self.upload_file(local_path, backup_path, storage)
        if option == 4:
            filename = input("Enter the filename: ")
            self.download_file(filename, storage)
        else:
            local_path = input("Enter the local path to file: ")
            backup_path = input("In what folder is it in cloud(root by default)? ")
            self.sync(local_path, backup_path, storage)

    def run(self):
        while True:
            self.menu()


if __name__ == "__main__":
    app = CloudStorageManager()
    app.run()
