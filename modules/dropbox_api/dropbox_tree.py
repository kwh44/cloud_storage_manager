import dropbox


def tree_files():
    """Return list with path of all files stored on the Dropbox account"""
    dbx = dropbox.Dropbox('Mb8FAtKIhmAAAAAAAAAANOqp6KdydV2NnfEs1EY4aVnl0FrDqHOiz5XmNUPoPGdy')
    return [i.path_display for i in dbx.files_list_folder('', recursive=True).entries if
            not type(i) is dropbox.files.FolderMetadata]


if __name__ == "__main__":
    print("\n".join(tree_files()))
