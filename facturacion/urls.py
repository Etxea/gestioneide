from django.conf.urls import patterns, include, url
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView

from django.contrib.auth.decorators import login_required, permission_required

from models import *
from views import *


urlpatterns = patterns('',
    url(r'recibos/$',ReciboListView.as_view(), name="recibos"),
    url(r'recibo/nuevo$',ReciboCreateView.as_view(), name="recibo_nuevo"),
    url(r'recibo/(?P<pk>\d+)/borrar/$',ReciboDeleteView.as_view(), name="recibo_borrar"),
    url(r'recibo/(?P<pk>\d+)/fichero/$',ReciboFicheroView.as_view(), name="recibo_fichero"),
    url(r'recibo/(?P<pk>\d+)/$',ReciboDetailView.as_view(), name="recibo_detalle"),

)
