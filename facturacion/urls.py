from django.conf.urls import patterns, include, url
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView

from django.contrib.auth.decorators import login_required, permission_required

from models import *
from views import *


urlpatterns = [
    url(r'recibos/$',login_required(ReciboListView.as_view()), name="recibos"),
    url(r'recibo/nuevo$',login_required(ReciboCreateView.as_view()), name="recibo_nuevo"),
    url(r'recibo/(?P<pk>\d+)/borrar/$',login_required(ReciboDeleteView.as_view()), name="recibo_borrar"),
    url(r'recibo/(?P<pk>\d+)/fichero/$',login_required(ReciboFicheroView.as_view()), name="recibo_fichero"),
    url(r'recibo/(?P<pk>\d+)/$',login_required(ReciboDetailView.as_view()), name="recibo_detalle"),
    url(r'recibo/(?P<pk>\d+)/informe$',login_required(ReciboInformeView.as_view()), name="recibo_informe"),
]
