from django.conf.urls import patterns, include, url
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView

from django.contrib.auth.decorators import login_required, permission_required

from models import *
from views import *


urlpatterns = patterns('',
    url(r'^$', login_required(ListView.as_view(model=Profesor)),name="profesores_lista"),
    url(r'nuevo$',ProfesorCreateView.as_view(), name="profesor_nuevo"),
    url(r'editar/(?P<pk>\d+)/$',ProfesorUpdateView.as_view(), name="profesor_editar"),
    url(r'borrar/(?P<pk>\d+)/$',ProfesorDeleteView.as_view(), name="profesor_borrar"),
    url(r'(?P<pk>\d+)/$',ProfesorDetailView.as_view(), name="profesor_detalle"),
)
