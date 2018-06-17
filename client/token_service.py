"""
@File: token_service.py
@Author: HoshinoTouko
@License: (C) Copyright 2014 - 2018, HoshinoTouko
@Contact: i@insky.jp
@Website: https://touko.moe/
@Created at: 2018-06-15 22:59
@Desc: 
"""
from client import userdata_service
from collections import OrderedDict
from core.encryption.asymmetric import V1 as rsa

import config_client
import requests
import base64
import json


def get_token():
    name = userdata_service.load_unencrypted_data('name')
    print('Get token...')
    r = requests.post(config_client.server_ip + '/session/start', {'user': name})
    try:
        if r.json().get('err') != 0:
            return False
        payload = OrderedDict()
        payload['key'] = r.json().get('key')
        signature = base64.b64decode(r.json().get('signature'))
        if rsa.verify(
            userdata_service.load_unencrypted_data('server_pk'),
            json.dumps(payload),
            signature
        ):
            print('Token signature auth succeed.')
            return payload['key']
        else:
            print('Token signature auth failed.')
            return False
    except Exception as e:
        print(str(e))
        return False
