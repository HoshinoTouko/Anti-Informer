"""
@File: service.py
@Author: HoshinoTouko
@License: (C) Copyright 2014 - 2018, HoshinoTouko
@Contact: i@insky.jp
@Website: https://touko.moe/
@Created at: 2018-06-13 10:17
@Desc: 
"""
from .models import Session
from user.models import User

import time
import base64
import random
import string


def create_session(username):
    user = User.objects.filter(username=username)
    if len(user) != 1:
        return False
    user = user[0]

    session = Session.objects.filter(
        user=user,
        finish=False
    )
    if len(session) > 0:
        session[0].delete()

    salt = ''.join(random.sample(string.ascii_letters + string.digits, 32))
    key = user.username + '-' +  salt + '-' + str(time.time())

    return Session.objects.create(
        key=key,
        user=user
    )


def auth_and_delete(username):
    user = User.objects.filter(username=username)
    if len(user) != 1:
        return False
    user = user[0]

    session = Session.objects.filter(
        user=user,
        finish=False
    )
    if len(session) == 0:
        return False

    current_session = session[0]
    current_session.delete()

    return True
