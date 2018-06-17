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

import os
import json
import base64
import config
import requests
import config_client


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
