"""
@File: register.py
@Author: HoshinoTouko
@License: (C) Copyright 2014 - 2018, HoshinoTouko
@Contact: i@insky.jp
@Website: https://touko.moe/
@Created at: 2018-06-17 17:32
@Desc: 
"""
from client import userdata_service, key_service
from core.encryption.asymmetric import V1 as rsa
from collections import OrderedDict

import os
import json
import config_client
import requests
import getpass
import base64


def register_interface():
    name = input('Please input your name\n')
    r = requests.get(config_client.server_ip + '/user/query').json().get('name')

    # Prevent duplicate user name
    if name in r:
        print('Duplicate user name, please re enter it.')
        return register_interface()

    # Get password
    password = True
    re_password = False
    while password != re_password:
        password = getpass.getpass('Please input your password\n')
        re_password = getpass.getpass('Please re input your password\n')
    # Generate key pair
    userdata_service.save_unencrypted_data('name', name)
    userdata_service.generate_check_pass_file(name, password)
    key_service.generate_key(password)
    print('Register succeed! Hello, %s' % name)
    print('Please remember your password.')

    # Get server public key
    payload = OrderedDict()
    payload['name'] = name
    payload['public_key'] = key_service.get_rsa_key('pk')
    signature = base64.b64encode(
        rsa.sign(key_service.get_rsa_key('sk', password), json.dumps(payload)))
    payload = dict({
        'signature': signature
    }, **payload)
    r = requests.post(config_client.server_ip + '/user/register', payload)
    try:
        if r.json().get('err') != 0:
            print('Register failed.')
            return False
        else:
            print('Register succeed and upload succeed.')
            userdata_service.save_unencrypted_data('server_pk', r.json().get('server_public_key'))
    except Exception as e:
        print(str(e))
        return False
