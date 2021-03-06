"""
@File: message_service.py
@Author: HoshinoTouko
@License: (C) Copyright 2014 - 2018, HoshinoTouko
@Contact: i@insky.jp
@Website: https://touko.moe/
@Created at: 2018-06-15 22:59
@Desc: 
"""
from core.encryption.asymmetric import V1 as rsa
from collections import OrderedDict
from client import userdata_service, token_service, key_service
from client import server_connect_service

import os
import json
import base64
import config
import requests
import config_client
import prettytable


def send_message(receiver, receiver_pk, message, my_pass, is_block=False):
    # Encrypt message
    encrypt_session_key, ciphertext, tag = rsa.encrypt(receiver_pk, message)
    msg_payload = OrderedDict()
    msg_payload['encrypt_session_key'] = str(
        base64.b64encode(encrypt_session_key), encoding=config.encoding)
    msg_payload['ciphertext'] = str(base64.b64encode(ciphertext), encoding=config.encoding)
    msg_payload['tag'] = str(base64.b64encode(tag), encoding=config.encoding)

    # Init payload
    payload = OrderedDict()
    payload['sender'] = userdata_service.load_unencrypted_data('name')
    payload['receiver'] = receiver
    payload['message'] = json.dumps(msg_payload)
    payload['is_block'] = is_block
    payload['token'] = token_service.get_token()

    signature = rsa.sign(key_service.get_rsa_key('sk', my_pass), json.dumps(payload))
    payload['signature'] = base64.b64encode(signature)
    r = requests.post(config_client.server_ip + '/message/send', payload)

    try:
        if r.json().get('err') == 0:
            os.system('cls')
            print('Send message to %s succeed.' % receiver)
            return True
        return False
    except Exception as e:
        print(str(e))
        return False


def receive_message(receiver, my_pass, is_read=False):
    payload = OrderedDict()
    payload['receiver'] = receiver
    payload['token'] = token_service.get_token()
    signature = rsa.sign(key_service.get_rsa_key('sk', my_pass), json.dumps(payload))
    payload['signature'] = base64.b64encode(signature)
    payload['is_read'] = is_read
    r = requests.post(config_client.server_ip + '/message/receive', payload)

    try:
        if r.json().get('err') == 0:
            os.system('cls')
            print("Receive message succeed!")
        else:
            print("Receive message failed")
    except Exception as e:
        print(str(e))
        return False
    msg = r.json().get('msg')
    signature = base64.b64decode(r.json().get('signature'))
    if not rsa.verify(userdata_service.load_unencrypted_data('server_pk'), json.dumps(msg), signature):
        print("您可能遇到了假的服务器")
        return False
    message_table = prettytable.PrettyTable()
    message_table.field_names = ['id', 'sender', 'message', 'verified']
    # Reverse msg
    msg.reverse()
    # Msg cut
    if len(msg) > 0:
        if len(msg) > 5:
            msg = msg[:5]
        for i in msg:
            message = json.loads(i['message'])
            encrypt_session_key = base64.b64decode(message['encrypt_session_key'])
            ciphertext = base64.b64decode(message['ciphertext'])
            tag = base64.b64decode(message['tag'])
            plain, verify = rsa.decrypt(key_service.get_rsa_key('sk', my_pass), encrypt_session_key, ciphertext, tag)
            # Add message to table
            message_table.add_row([
                i['id'],
                i['sender'],
                str(plain, encoding=config.encoding),
                '√' if verify else '×',
            ])
        print(message_table)
    else:
        print("No new message!")
    return True
