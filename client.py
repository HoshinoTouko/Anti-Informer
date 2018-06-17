from client import userdata_service
from client.interface.register import register_interface

import os
import config
import getpass


def client():
    # Welcome
    print('Welcome to anti-informer application. App version is %s' % config.version)
    # Check if the user is registered
    if not userdata_service.check_user_data_integrity():
        os.system('cls')
        register_interface()

    print('Login required')
    password = ''
    while not userdata_service.check_pass(password):
        password = getpass.getpass('Please input your password\n')
    while True:
        os.system('cls')
        command = input('Please input your command\n')
        if command == 'E':
            print('Good bye, see you next time.')
            exit(0)


if __name__ == '__main__':
    client()
