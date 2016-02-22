# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from views import *

urlpatterns = [
    url(r'^list/$', 'list', name='list'),
    url(r'^uploads/$', DbListView.as_view(), name='list'),
]
