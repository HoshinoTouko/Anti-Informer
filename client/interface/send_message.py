"""
@File: send_message.py
@Author: HoshinoTouko
@License: (C) Copyright 2014 - 2018, HoshinoTouko
@Contact: i@insky.jp
@Website: https://touko.moe/
@Created at: 2018-06-17 19:03
@Desc: 
"""
from client import token_service


def send_message_interface():
    print(token_service.get_token())
    message = input('Please input your message...\n')
