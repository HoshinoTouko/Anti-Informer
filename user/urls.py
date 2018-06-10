"""
@File: urls.py
@Author: HoshinoTouko
@License: (C) Copyright 2014 - 2018, HoshinoTouko
@Contact: i@insky.jp
@Website: https://touko.moe/
@Created at: 2018-06-09 17:09
@Desc: 
"""
from django.urls import path

from . import views


urlpatterns = [
    path('start_public_key_upload',
         views.start_public_key_upload, name='start_public_key_upload'),
]
