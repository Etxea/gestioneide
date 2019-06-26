from django.conf.urls import url
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required, permission_required

from models import *
from views import *
from forms import *

urlpatterns = [
    url(r'^$', login_required(CursosListView.as_view()),name="cursos_lista"),
    url(r'libros/(?P<pk>\d+)/$',login_required(LibrolView.as_view()), name="curso_libro_detalle"),
    url(r'libros$', login_required(LibroListView.as_view()),name="cursos_libros_lista"),
    url(r'libros/nuevo/$',login_required(LibroCreateView.as_view()), name="curso_libro_nuevo"),
    #~ url(r'libros/(?P<pk>\d+)/borrar/$',CursoDeleteView.as_view()), name="curso_borrar"),
    #~ url(r'libros/(?P<pk>\d+)/editar/$',login_required(UpdateView.as_view(model=Curso)), name="curso_editar"),
    url(r'nuevo/$',login_required(CursoCreateView.as_view()), name="curso_nuevo"),
    url(r'(?P<pk>\d+)/$',login_required(CursoDetailView.as_view()), name="curso_detalle"),
    url(r'(?P<pk>\d+)/borrar/$',login_required(CursoDeleteView.as_view()), name="curso_borrar"),
    url(r'(?P<pk>\d+)/editar/$',login_required(CursoUpdateView.as_view()), name="curso_editar"),
]
