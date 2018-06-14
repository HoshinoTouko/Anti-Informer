"""
@File: urls.py
@Author: HoshinoTouko
@License: (C) Copyright 2014 - 2018, HoshinoTouko
@Contact: i@insky.jp
@Website: https://touko.moe/
@Created at: 2018-06-09 17:09
@Desc: 
"""
from . import views

from django.urls import path


urlpatterns = [
    path('start',
         views.start_new_session, name='start_new_session'),
]
