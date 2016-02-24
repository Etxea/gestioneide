from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()
from views import *


urlpatterns = patterns("",
    url(r"^$", ListaAulas.as_view(), name="aulas_lista"),
    url(r"^nueva/$", NuevaAula.as_view(), name="aula_nueva"),
    url(r"^editar/(?P<pk>\d+)/$", EditarAula.as_view(), name="aula_editar"),
    url(r"^(?P<pk>\d+)/$", DetalleAula.as_view(), name="aula_detalle"),
    )
