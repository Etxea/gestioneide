from django.conf.urls import url
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import admin
admin.autodiscover()
from clases.views import *


urlpatterns = [
    url(r"^$", login_required(TemplateView.as_view(template_name="home.html")), name="clases_lista"),
    url(r'clases/(?P<cliente_id>\d+)/nueva/$',login_required(CreateView.as_view(model=Clase)), name="clase_curso_nueva"),
    url(r'clases/nueva$',login_required(CreateView.as_view(model=Clase)), name="clase_nueva"),
    url(r'clases/(?P<pk>\d+)/editar/$',login_required(UpdateView.as_view(model=Clase)), name="clase_editar"),
    url(r'clases/(?P<pk>\d+)/borrar/$',login_required(ClaseDeleteView.as_view()), name="clase_borrar"),
    url(r"^nueva/grupo/(?P<grupo_id>\d+)/$", login_required(nueva_clase_grupo.as_view()), name="nueva_clase_grupo"),
    url(r"^nueva/$", login_required(nueva_clase.as_view()), name="nueva_clase"),
    url(r"^editar/(?P<pk>\d+)/$", login_required(editar_clase.as_view()), name="editar_clase"),
    url(r"^editar/(?P<pk>\d+)/modal$", login_required(editar_clase_modal.as_view()), name="editar_clase_modal"),
    url(r"^borrar/(?P<pk>\d+)/$", login_required(borrar_clase.as_view()), name="borrar_clase"),
    url(r"semana/(?P<numero>\d+)/profesor/(?P<id_profesor>\d+)/$", login_required(vista_semana_profesor), name="semana_profesor"),
    url(r"semana/(?P<numero>\d+)/aula/(?P<id_aula>\d+)/$", login_required(vista_semana_aula), name="semana_aula"),
    url(r"semana/(?P<numero>\d+)/$", login_required(vista_semana), name="semana"),
    url(r"^profesores/$", login_required(clases_lista_profesores.as_view()), name="clases_lista_profesores"),
    url(r"^profesor/(\d+)/$", login_required(clases_profesor.as_view()), name="clases_profesor"),
    #url(r"^profesor/libre/(?P<dia_semana>\d+)/$", libre_profesor, name="clases_profesor"),
    url(r"^aulas/$", login_required(clases_lista_aulas.as_view()), name="clases_lista_aulas"),
    url(r"^aula/(\d+)/$", login_required(clases_aula.as_view()), name="clases_aula"),
]
