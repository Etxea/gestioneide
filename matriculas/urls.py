# -*- coding: utf-8 -*-
from django.conf.urls import url
from views import *

from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r"eide/lista/$", login_required(MatriculaEideListView.as_view()), name="matricula_eide_lista"),
    url(r'eide/nueva/$',MatriculaEideCreateView.as_view(), name="matricula_eide_nueva"),
    url(r'eide/gracias/$',MatriculaEideGracias.as_view(), name="matricula_eide_gracias"),
    url(r'eide/error/$',MatriculaEideError.as_view(), name="matricula_eide_error"),
    url(r'eide/ver/(?P<pk>\d+)/$',login_required(MatriculaEideDetailView.as_view()), name="matricula_eide_detalle"),
    url(r'eide/editar/(?P<pk>\d+)/$',login_required(MatriculaEideUpdateView.as_view()), name="matricula_eide_editar"),
    url(r'eide/pagar/(?P<pk>\d+)/$',MatriculaEidePayView.as_view(), name="matricula_eide_pagar"),
]