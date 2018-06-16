"""
@File: key_service.py
@Author: HoshinoTouko
@License: (C) Copyright 2014 - 2018, HoshinoTouko
@Contact: i@insky.jp
@Website: https://touko.moe/
@Created at: 2018-06-15 22:59
@Desc: 
"""
from core.encryption.asymmetric import V1 as rsa
from core.encryption.symmetric import V1 as chacha20
from paths import public_key_path, private_key_path, root_dir

import os
import base64

import config


def get_rsa_key(password, key_type):
    if key_type == 'pk':
        res = ''.join(open(public_key_path, 'r').readlines())
    elif key_type == 'sk':
        enc_key = base64.b64decode(''.join(open(private_key_path, 'r').readlines()))
        res = str(chacha20.decrypt(password, enc_key), encoding=config.encoding)
    else:
        return False
    return res


def generate_key(password, force=False):
    # Check if key exist
    if not os.path.exists(root_dir):
        os.makedirs(root_dir)
    # Create
    if not os.path.exists(private_key_path) or force:
        print('Generating key pairs...')
        sk, pk = rsa.generate_key()
        with open(private_key_path, 'w') as fi:
            b64_res = base64.b64encode(chacha20.encrypt(password, sk))
            fi.write(str(b64_res, encoding=config.encoding))
        with open(public_key_path, 'w') as fi:
            fi.write(str(pk, encoding=config.encoding))
    else:
        raise Exception('Key pair exist')


if __name__ == '__main__':
    # generate_key('123')
    print(get_rsa_key('123', 'sk'))
    print(get_rsa_key('123', 'pk'))
