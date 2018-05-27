import os

from GDrive_storage_class import GDrive_Storage


def test():
    test_results = []

    drive = GDrive_Storage()
    drive.link_account()

    if drive.upload_file('hello.txt', 'text/plain', 'root'):
        test_results.append('.')
    else:
        test_results.append('F')
    os.remove('hello.txt')

    if drive.search('hello.txt'):
        test_results.append('.')
    else:
        test_results.append('F')

    drive.download_file('hello.txt', drive.search('hello.txt'))
    if 'hello.txt' in os.listdir('.'):
        test_results.append('.')
    else:
        test_results.append('F')

    with open('hello.txt', 'w') as f:
        f.write("Updated hello.txt")

    if drive.sync(drive.search('hello.txt'), 'hello.txt'):
        test_results.append('.')
    else:
        test_results.append('F')
    print("".join(test_results))
    print("Passed: {}.".format(sum(1 for i in test_results if i == '.')))
    print("Passed: {}.".format(sum(1 for i in test_results if i == 'F')))
    return 0


def main():
    test()
    return 0


if __name__ == "__main__":
    main()
