"""
@File: paths.py
@Author: HoshinoTouko
@License: (C) Copyright 2014 - 2018, HoshinoTouko
@Contact: i@insky.jp
@Website: https://touko.moe/
@Created at: 2018-06-16 00:31
@Desc: 
"""
import os


root_dir = os.path.dirname(os.path.abspath(__file__)) + './.data/user'

password_check_path = root_dir + '/pass'
unencrypted_data_path = root_dir + '/unencrypted_data.json'

public_key_path = root_dir + '/public_key'
private_key_path = root_dir + '/private_key'
