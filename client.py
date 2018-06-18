from client import userdata_service
from client.interface.register import register_interface
from client.interface.send_message import send_message_interface
from client.interface.receive_message import receive_message_interface

import os
import time
import config
import getpass


def client():
    # Welcome
    os.system('cls')
    print('Welcome to anti-informer application. App version is %s' % config.version)
    # Check if the user is registered
    if not userdata_service.check_user_data_integrity():
        register_interface()

    print('Login required')
    password = ''
    while not userdata_service.check_pass(password):
        password = getpass.getpass('Please input your password\n')
    print('Password check succeed.')
    time.sleep(1)
    os.system('cls')
    while True:
        print('(E)xit\t(S)end\t(R)eceive')
        command = input('Please input your command\n')
        if command == 'E':
            os.system('cls')
            print('Good bye, see you next time.')
            time.sleep(2)
            exit(0)
        elif command == 'S':
            os.system('cls')
            print('Send message')
            send_message_interface(password)
        elif command == 'R':
            os.system('cls')
            print('Receive message')
            receive_message_interface(password)


if __name__ == '__main__':
    client()
