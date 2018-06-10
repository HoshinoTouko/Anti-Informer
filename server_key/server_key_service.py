"""
@File: server_key_service.py
@Author: HoshinoTouko
@License: (C) Copyright 2014 - 2018, HoshinoTouko
@Contact: i@insky.jp
@Website: https://touko.moe/
@Created at: 2018-06-09 20:54
@Desc: 
"""
from core.encryption.asymmetric import V1 as rsa

import os
import config


def get_private_key_path():
    return os.path.split(os.path.realpath(__file__))[0] + '/private_key.txt'


def get_public_key_path():
    return os.path.split(os.path.realpath(__file__))[0] + '/public_key.txt'


def get_public_key():
    public_key_path = get_public_key_path()
    with open(public_key_path, 'r') as fi:
        return ''.join(fi.readlines())


def get_private_key():
    private_key_path = get_private_key_path()
    with open(private_key_path, 'r') as fi:
        return ''.join(fi.readlines())


def generate_server_key_pair(force=False):
    # Set key path
    private_key_path = get_private_key_path()
    public_key_path = get_public_key_path()
    # Check if it needed to regenerate
    if os.path.exists(private_key_path) and os.path.exists(public_key_path) or force:
        return print('No need to regenerate.')
    # Generate and write back
    private_key, public_key = rsa.generate_key()
    with open(private_key_path, 'w+') as fi:
        fi.write(str(private_key, encoding=config.encoding))
    with open(public_key_path, 'w+') as fi:
        fi.write(str(public_key, encoding=config.encoding))
    return print('Generate succeed')


def main():
    generate_server_key_pair()


if __name__ == '__main__':
    main()
