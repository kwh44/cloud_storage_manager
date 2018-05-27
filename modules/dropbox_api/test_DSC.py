from dropbox_storage_class import DropBoxStorage


def test():
    """Test uploading, download, delete file using DropBoxStorage class"""
    test_results = []
    dropbox = DropBoxStorage()
    dropbox.link_account()
    dropbox.upload('hello.txt', '/hello.txt')
    if dropbox.search('hello.txt'):
        test_results.append('.')
    else:
        test_results.append('F')
    dropbox.upload('hello.txt', '/hello.txt')
    if dropbox.download_file('/hello.txt'):
        test_results.append('.')
    else:
        test_results.append('F')
    if dropbox.delete_file('/hello.txt'):
        test_results.append('.')
    else:
        test_results.append('F')
    dropbox.unlink_account()
    print("".join(test_results))
    print("Passed: {}".format(sum(1 for i in test_results if i == '.')))
    print("Failed: {}".format(sum(1 for i in test_results if i == 'F')))
    return 0


def main():
    test()
    return 0


if __name__ == "__main__":
    main()