from django.conf.urls import include, url
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView

from django.contrib.auth.decorators import login_required, permission_required

from gestioneide.models import *
from grupos.views import *


urlpatterns = [
    url(r'^$', login_required(GrupoListView.as_view()),name="grupo_lista"),
    url(r'lista$', login_required(GrupoProfesorListView.as_view()),name="grupo_lista_profesor"),
    url(r'centro/(?P<centro>\d+)/$', login_required(GrupoListView.as_view()),name="grupo_lista_centro"),
    url(r'nuevo$',login_required(GrupoCreateView.as_view()), name="grupo_nuevo"),
    url(r'editar/(?P<pk>\d+)/$',login_required(GrupoUpdateView.as_view()), name="grupo_editar"),
    url(r'borrar/(?P<pk>\d+)/$',login_required(GrupoDeleteView.as_view()), name="grupo_borrar"),
    url(r'alumno/email/(?P<pk>\d+)/$',login_required(GrupoAlumnoEmailView.as_view()), name="grupo_alumno_email"),
    url(r'email/(?P<pk>\d+)/$',login_required(GrupoEmailView.as_view()), name="grupo_email"),
    url(r'profesor/(?P<pk>\d+)/$',login_required(GrupoProfesorDetailView.as_view()), name="grupo_profesor_detalle"),
    url(r'anotacion/(?P<grupo_id>\d+)/nueva/$',login_required(GrupoAnotacionCreateView.as_view()), name="grupo_anotacion_nueva"),
    url(r'anotacion/(?P<pk>\d+)/borrar/',login_required(GrupoAnotacionDeleteView.as_view()), name="grupo_anotacion_borrar"),
    url(r'anotacion/(?P<pk>\d+)/',login_required(GrupoAnotacionDetailView.as_view()), name="grupo_anotacion_ver"),
    url(r'clase/videourl/(?P<grupo_id>\d+)/(?P<pk>\d+)/$',login_required(GrupoClaseVideurlCreateView.as_view()), name="grupo_videourl"),
    url(r'(?P<pk>\d+)/envionotas/trimestre/(?P<trimestre>\d+)/$',login_required(GrupoNotasTrimestreEmailView.as_view()), name="envio_notas_trimestre"),
    url(r'(?P<pk>\d+)/envionotas/cuatrimestre/(?P<cuatrimestre>\d+)/$',login_required(GrupoNotasCuatrimestreEmailView.as_view()), name="envio_notas_cuatrimestre"),
    url(r'(?P<pk>\d+)/planilla/asistencias/(?P<mes>\d+)/$',login_required(GrupoAnotacionCreateView.as_view()), name="grupo_asistencia_mes"),
    url(r'(?P<pk>\d+)/planilla/notas/(?P<trimestre>\d+)/$',login_required(GrupoAnotacionDeleteView.as_view()), name="grupo_notas_trimestre"),
    url(r'(?P<pk>\d+)/$',login_required(GrupoDetailView.as_view()), name="grupo_detalle"),
]
