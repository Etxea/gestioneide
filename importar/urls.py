# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.contrib.auth.decorators import login_required, permission_required

from views import *

urlpatterns = [
    #url(r'^list/$', 'list', name='list'),
    url(r'^list/$', login_required(DbListView.as_view()), name='importar_list'),
    url(r'^upload/$', login_required(upload), name='upload'),
    url(r'^load/$', login_required(load_olddb), name='load_olddb')
]
