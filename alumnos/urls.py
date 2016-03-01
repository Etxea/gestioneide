from django.conf.urls import patterns, include, url
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView

from django.contrib.auth.decorators import login_required, permission_required

from models import *
from views import *


urlpatterns = [
    url(r'^$', login_required(AlumnoListView.as_view()),name="alumnos_lista"),
    url(r'nuevo$',login_required(AlumnoCreateView.as_view()), name="alumno_nuevo"),
    url(r'editar/(?P<pk>\d+)/$',login_required(AlumnoUpdateView.as_view()), name="alumno_editar"),
    url(r'borrar/(?P<pk>\d+)/$',login_required(AlumnoDeleteView.as_view()), name="alumno_borrar"),
    url(r'buscar/$',login_required(AlumnoBuscarView.as_view()), name="alumno_buscar"),
    url(r'(?P<pk>\d+)/$',login_required(AlumnoDetailView.as_view()), name="alumno_detalle"),

]
