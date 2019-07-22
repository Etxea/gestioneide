from django.conf.urls import url
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView

from django.contrib.auth.decorators import login_required, permission_required

from gestioneide.models import *
from facturacion.views import *


urlpatterns = [
    url(r'recibos/$',login_required(ReciboListView.as_view()), name="recibos"),
    url(r'recibo/nuevo$',login_required(ReciboCreateView.as_view()), name="recibo_nuevo"),
    url(r'recibo/(?P<pk>\d+)/editar/$',login_required(ReciboUpdateView.as_view()), name="recibo_editar"),
    url(r'recibo/(?P<pk>\d+)/borrar/$',login_required(ReciboDeleteView.as_view()), name="recibo_borrar"),
    url(r'recibo/(?P<pk>\d+)/fichero/$',login_required(ReciboFicheroView.as_view()), name="recibo_fichero"),
    url(r'recibo/(?P<pk>\d+)/$',login_required(ReciboDetailView.as_view()), name="recibo_detalle"),
    url(r'recibo/(?P<pk>\d+)/informe$',login_required(ReciboInformeView.as_view()), name="recibo_informe"),
    url(r'recibo/(?P<pk>\d+)/xls$',login_required(ReciboInformeExcelView), name="recibo_informe_xls"),
]
