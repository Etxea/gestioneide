from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib import admin
from views import *
from gestioneide.models import Nota,Falta
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required, permission_required



urlpatterns = [
    url(r"^$", login_required(EvaluacionListView.as_view()), name="evaluacion"),
    url(r"notas/$", login_required(EvaluacionListView.as_view(template_name="evaluacion/evaluacion_notas.html")), name="evaluacion_notas"),
    url(r"pasarlista/grupo/(?P<pk>\d+)/(?P<mes>\d+)/$", login_required(PasarListaGrupoView.as_view()), name="evaluacion_pasarlista"),
    url(r"faltas/$", login_required(EvaluacionListView.as_view(template_name="evaluacion/evaluacion_faltas.html")), name="evaluacion_faltas"),
    url(r'nota/grupo/(?P<pk>\d+)/(?P<trimestre>\d+)/$',login_required(NotasGrupoView), name="notas_grupo"),
    url(r'nota/(?P<asistencia>\d+)/(?P<trimestre>\d+)/$',login_required(NotaCreateView.as_view()), name="nota_nueva"),
    url(r'nota/(?P<asistencia>\d+)/(?P<trimestre>\d+)/editar/$',login_required(NotaCreateView.as_view()), name="nota_nueva"),
    url(r'nota/(?P<pk>\d+)/borrar/$',login_required(DeleteView.as_view(model=Nota)), name="nota_borrar"),
    url(r'falta/nueva/$',login_required(FaltaCreateView.as_view()), name="falta_nueva"),
    url(r'falta/grupo/(?P<pk>\d+)/(?P<mes>\d+)/$',login_required(FaltasGrupoView), name="faltas_grupo"),
    url(r'falta/(?P<pk>\d+)/editar/$',login_required(UpdateView.as_view(model=Falta)), name="falta_editar"),
    url(r'falta/(?P<pk>\d+)/borrar/$',login_required(DeleteView.as_view(model=Falta)), name="falta_borrar")
]
