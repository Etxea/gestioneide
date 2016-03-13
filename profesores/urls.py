from django.conf.urls import patterns, include, url
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView

from django.contrib.auth.decorators import login_required, permission_required

from models import *
from views import *


urlpatterns = [
    url(r'^$', login_required(ProfesorListView.as_view()),name="profesores_lista"),
    url(r'nuevo$',ProfesorCreateView.as_view(), name="profesor_nuevo"),
    url(r'editar/(?P<pk>\d+)/$',ProfesorUpdateView.as_view(), name="profesor_editar"),
    url(r'borrar/(?P<pk>\d+)/$',ProfesorDeleteView.as_view(), name="profesor_borrar"),
    url(r'(?P<pk>\d+)/$',ProfesorDetailView.as_view(), name="profesor_detalle"),
]
