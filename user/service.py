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
from server_key.server_key_service import get_public_key, get_private_key
from user.models import User
from collections import OrderedDict

import json
import base64
import random

import config


def check_user_signature(public_key, payload, signature):
    """
    :type public_key: str
    :type payload: str
    :type signature: str
    :rtype: bool
    """
    return rsa.verify(public_key, payload, signature)


def get_public_key_by_username(username):
    try:
        user = User.objects.get(username=username)
    except Exception as e:
        return False
    # Get user's pk and sign
    user_public_key = user.public_key
    # Init a payload and add some random padding
    payload = OrderedDict()
    payload['rand_pad'] = random.random()
    payload['public_key'] = user_public_key
    # Signature
    signature = str(
        base64.b64encode(rsa.sign(get_private_key(), json.dumps(payload))),
        encoding=config.encoding
    )
    return payload, signature
