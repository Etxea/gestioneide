from django.conf.urls import patterns, include, url
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView

from django.contrib.auth.decorators import login_required, permission_required

from models import *
from views import *


urlpatterns = patterns('',
    url(r'^$', GrupoListView.as_view(),name="grupo_lista"),
    url(r'nuevo$',GrupoCreateView.as_view(), name="grupo_nuevo"),
    url(r'editar/(?P<pk>\d+)/$',GrupoUpdateView.as_view(), name="grupo_editar"),
    url(r'borrar/(?P<pk>\d+)/$',GrupoDeleteView.as_view(), name="grupo_borrar"),
    url(r'(?P<pk>\d+)/planilla/asistencias/(?P<mes>\d+)/$',GrupoAsistenciaView.as_view(), name="grupo_asistencia_mes"),
    url(r'(?P<pk>\d+)/planilla/notas/(?P<trimestre>\d+)/$',GrupoNotasView.as_view(), name="grupo_notas_trimestre"),
    url(r'(?P<pk>\d+)/$',GrupoDetailView.as_view(), name="grupo_detalle"),
)
