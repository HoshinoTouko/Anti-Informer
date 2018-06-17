"""
@File: userdata_service.py
@Author: HoshinoTouko
@License: (C) Copyright 2014 - 2018, HoshinoTouko
@Contact: i@insky.jp
@Website: https://touko.moe/
@Created at: 2018-06-15 23:26
@Desc: 
"""
from core.encryption.symmetric import V1 as chacha20
from paths import password_check_path, unencrypted_data_path, private_key_path, public_key_path

import os
import json
import base64
import random
import string

import config


def check_user_data_integrity():
    userdata_file_paths = [
        password_check_path,
        unencrypted_data_path,
        private_key_path,
        public_key_path,
    ]
    for path in userdata_file_paths:
        if not os.path.exists(path):
            return False
    return True


def load_unencrypted_data(key):
    if not os.path.exists(unencrypted_data_path):
        json.dump({}, open(unencrypted_data_path, 'w+'))
        return False
    try:
        unencrypted_data = json.load(open(unencrypted_data_path, 'r'))
        value = unencrypted_data.get(key)
        if not value:
            return False
        return value
    except Exception as e:
        print('Error: ' + str(e))
    return False


def save_unencrypted_data(key, value):
    if not os.path.exists(unencrypted_data_path):
        json.dump({}, open(unencrypted_data_path, 'w'))
    try:
        unencrypted_data = json.load(open(unencrypted_data_path, 'r'))
        new_data = dict(
            {key: value}, **unencrypted_data
        )
        if len(value) > 20:
            value = value[:19] + '....'
        print('Save unencrypted data `%s` - `%s`' % (key, value))
        json.dump(new_data, open(unencrypted_data_path, 'w'))
        return True
    except Exception as e:
        print('Error: ' + str(e))
    return False


def check_pass(password):
    if not check_user_data_integrity():
        raise Exception('No password auth file')

    username = load_unencrypted_data('name')
    with open(password_check_path, 'r+') as fi:
        try:
            check_data = base64.b64decode(bytes(''.join(fi.readlines()), encoding=config.encoding))
            plaintext = str(
                chacha20.decrypt(password, check_data),
                encoding=config.encoding
            )
            if username in plaintext:
                fi.close()
                generate_check_pass_file(username, password)
                return True
        except:
            return False
        return False


def generate_check_pass_file(username, password):
    with open(password_check_path, 'w+') as fi:
        new_check_data = '%s:%s:%s' % (
            ''.join(random.sample(string.ascii_letters + string.digits, random.randint(16, 32))),
            username,
            ''.join(random.sample(string.ascii_letters + string.digits, random.randint(16, 32)))
        )
        enc_check_data = chacha20.encrypt(password, new_check_data)
        fi.write(str(base64.b64encode(enc_check_data), encoding=config.encoding))
    return True


if __name__ == '__main__':
    # save_unencrypted_data('name', 'touko')
    # print(load_unencrypted_data('name'))
    # print(load_unencrypted_data('name1'))
    generate_check_pass_file('touko', '123')
    print(check_pass('123'))
