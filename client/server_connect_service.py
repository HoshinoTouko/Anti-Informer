"""
@File: server_connection.py
@Author: HoshinoTouko
@License: (C) Copyright 2014 - 2018, HoshinoTouko
@Contact: i@insky.jp
@Website: https://touko.moe/
@Created at: 2018-06-17 17:26
@Desc: 
"""
from collections import OrderedDict
from core.encryption.asymmetric import V1 as rsa
from client.userdata_service import load_unencrypted_data

import json
import base64
import requests
import config_client


def download_user_public_key(username):
    print('Get %s\'s public key...' % username)
    r = requests.get(config_client.server_ip + '/user/query', {'name': username})
    data = r.json()
    try:
        payload = OrderedDict()
        payload['rand_pad'] = data.get('rand_pad')
        payload['public_key'] = data.get('public_key')
        signature = base64.b64decode(data.get('signature'))
        print('Verifying...')
        if rsa.verify(
            load_unencrypted_data('server_pk'),
            json.dumps(payload),
            signature
        ):
            print('User %s\'s public key verified.' % username)
            return data.get('public_key')
        else:
            print('User %s\'s public key not verified.' % username)
            return False
    except Exception as e:
        print(str(e))
        return False


def get_user_on_server():
    return requests.get(config_client.server_ip + '/user/query').json().get('name')
