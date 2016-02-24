from django.conf.urls import patterns, include, url
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required, permission_required

from models import *
from views import *
from forms import *

urlpatterns = patterns('',
    url(r'^$', CursosListView.as_view(),name="cursos_lista"),
    url(r'libros/(?P<pk>\d+)/$',CursoLibrolView.as_view(), name="curso_libro_detalle"),
    url(r'libros$', CursosLibrosListView.as_view(),name="cursos_libros_lista"),
    url(r'libros/nuevo/$',CursosLibrosCreateView.as_view(), name="curso_libro_nuevo"),
    #~ url(r'libros/(?P<pk>\d+)/borrar/$',CursoDeleteView.as_view(), name="curso_borrar"),
    #~ url(r'libros/(?P<pk>\d+)/editar/$',login_required(UpdateView.as_view(model=Curso)), name="curso_editar"),
    url(r'nuevo/$',login_required(CreateView.as_view(model=Curso,form_class = CursoForm)), name="curso_nuevo"),
    url(r'(?P<pk>\d+)/$',CursoDetailView.as_view(), name="curso_detalle"),
    url(r'(?P<pk>\d+)/borrar/$',CursoDeleteView.as_view(), name="curso_borrar"),
    url(r'(?P<pk>\d+)/editar/$',CursoUpdateView.as_view(), name="curso_editar"),
)
