"""
@File: send_message.py
@Author: HoshinoTouko
@License: (C) Copyright 2014 - 2018, HoshinoTouko
@Contact: i@insky.jp
@Website: https://touko.moe/
@Created at: 2018-06-17 19:03
@Desc: 
"""
from client import token_service, server_connect_service, message_service

import prettytable


def send_message_interface(my_pass):
    # Get server user list
    print('Get user from server....')
    online_users = server_connect_service.get_user_on_server()
    # Show server user list
    user_list_table = prettytable.PrettyTable()
    user_list_table.field_names = ['name']
    for user in online_users:
        user_list_table.add_row([user])
    print(user_list_table)
    # Select receiver
    receiver = False
    while receiver not in online_users:
        receiver = input('Please input the messgae\'s receiver.\n')
    # Download receiver key
    receiver_pk = server_connect_service.download_user_public_key(receiver)
    if not receiver_pk:
        return send_message_interface(my_pass)
    # Get message to send
    message = input('Please input your message...\n')
    message_service.send_message(
        receiver, receiver_pk,
        message, my_pass
    )
