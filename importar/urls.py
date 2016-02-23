# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from views import *

urlpatterns = [
    #url(r'^list/$', 'list', name='list'),
    url(r'^list/$', DbListView.as_view(), name='list'),
    url(r'^upload/$', upload, name='upload'),
    url(r'^load/$', load_olddb, name='load_olddb')
]
