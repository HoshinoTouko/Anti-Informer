"""
@File: utils.py
@Author: HoshinoTouko
@License: (C) Copyright 2014 - 2018, HoshinoTouko
@Contact: i@insky.jp
@Website: https://touko.moe/
@Created at: 2018-06-06 15:25
@Desc: 
"""
import config


def trans_to_bytes(text):
    if not isinstance(text, bytes):
        text = bytes(text, encoding=config.encoding)
    return text
