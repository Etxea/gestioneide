from django.conf.urls import include, url
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView

from django.contrib.auth.decorators import login_required, permission_required

from gestioneide.models import *
from alumnos.views import *


urlpatterns = [
    url(r'^$', login_required(AlumnoGrupoListView.as_view()),name="alumnos_lista"),
    url(r'todos/$', login_required(AlumnoListView.as_view()),name="alumnos_lista_todos"),
    url(r'activos/$', login_required(AlumnoActivosListView.as_view()),name="alumnos_lista_activos"),
    url(r'nuevo/$',login_required(AlumnoCreateView.as_view()), name="alumno_nuevo"),
    url(r'editar/(?P<pk>\d+)/$',login_required(AlumnoUpdateView.as_view()), name="alumno_editar"),
    url(r'borrar/(?P<pk>\d+)/$',login_required(AlumnoDeleteView.as_view()), name="alumno_borrar"),
    url(r'baja/(?P<pk>\d+)/$',login_required(AlumnoBajaView.as_view()), name="alumno_baja"),
    #url(r'buscar/(?P<cadena>\w+)/$',login_required(AlumnoBuscarView.as_view()), name="alumno_buscar"),
    url(r'buscar/$',login_required(AlumnoBuscarView.as_view()), name="alumno_buscar"),
    url(r'detalle/(?P<pk>\d+)/$',login_required(AlumnoDetailView.as_view()), name="alumno_detalle"),
    url(r'anotacion/(?P<alumno_id>\d+)/nueva$',login_required(AlumnoAnotacionCreateView.as_view()), name="alumno_anotacion_nueva"),
    url(r'anotacion/(?P<pk>\d+)/borrar',login_required(AlumnoAnotacionDeleteView.as_view()), name="alumno_anotacion_borrar"),
    url(r'pruebanivel/(?P<alumno_id>\d+)/nueva$',login_required(AlumnoPruebaNivelCreateView.as_view()), name="alumno_pruebanivel_nueva"),
    url(r'pruebanivel/(?P<pk>\d+)/borrar',login_required(AlumnoPruebaNivelDeleteView.as_view()), name="alumno_pruebanivel_borrar"),url(r'pruebanivel/(?P<alumno_id>\d+)/nueva$',login_required(AlumnoPruebaNivelCreateView.as_view()), name="alumno_pruebanivel_nueva"),
    url(r'cambridge/(?P<alumno_id>\d+)/nueva$',login_required(AlumnoResultadoCambridgeCreateView.as_view()), name="alumno_resultadocambridge_nuevo"),
    url(r'cambridge/(?P<pk>\d+)/borrar',login_required(AlumnoResultadoCambridgeDeleteView.as_view()), name="alumno_resultadocambridge_borrar"),
]
