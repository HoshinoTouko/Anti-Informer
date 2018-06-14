"""
@File: service.py
@Author: HoshinoTouko
@License: (C) Copyright 2014 - 2018, HoshinoTouko
@Contact: i@insky.jp
@Website: https://touko.moe/
@Created at: 2018-06-09 21:11
@Desc: 
"""
from core.encryption.asymmetric import V1 as rsa

import json
import collections
import base64

from server_key.server_key_service import get_public_key, get_private_key


def check_user_signature(public_key, payload, signature):
    """
    :type public_key: str
    :type payload: str
    :type signature: str
    :rtype: bool
    """
    return rsa.verify(public_key, payload, signature)


def pack_server_public_key(user_public_key):
    encrypt_session_key, ciphertext, tag = rsa.encrypt(user_public_key, get_public_key())

    ret = collections.OrderedDict()
    ret['encrypt_session_key'] = str(base64.b64encode(encrypt_session_key))[2:-2]
    ret['ciphertext'] = str(base64.b64encode(ciphertext))[2:-2]
    ret['tag'] = str(base64.b64encode(tag))[2:-2]

    signature = str(base64.b64encode(rsa.sign(get_private_key(), json.dumps(ret))), "utf-8")

    return ret, signature
