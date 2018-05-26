from dropbox_storage_class import DropBoxStorage

def class_test():
    d = DropBoxStorage()
    d.link_account()
    print(d.dbx_user_account)

if __name__ == "__main__":
    class_test()