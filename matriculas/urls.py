# -*- coding: utf-8 -*-
from django.conf.urls import url
from views import *

from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r"eide/^$", login_required(MatriculaEideListView.as_view()), name="matricula_eide_lista"),
    url(r'eide/nueva$',MatriculaEideCreateView.as_view(), name="matricula_eide_nueva"),
    url(r'eide/ver/(?P<pk>\d+)/$',login_required(MatriculaEideDetailView.as_view()), name="matricula_eide_detalle"),
]