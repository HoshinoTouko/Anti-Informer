"""
@File: server_connection.py
@Author: HoshinoTouko
@License: (C) Copyright 2014 - 2018, HoshinoTouko
@Contact: i@insky.jp
@Website: https://touko.moe/
@Created at: 2018-06-17 17:26
@Desc: 
"""
import requests
import config_client


def get_user_on_server():
    return requests.get(config_client.server_ip + '/user/query').json().get('name')
