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
    path('send', views.send, name='send'),
    path('receive', views.receive, name='receive'),
]
