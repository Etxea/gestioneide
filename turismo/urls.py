
from django.conf.urls import url

from views import *


from django.contrib import admin


urlpatterns = [
    url(r"^$", TurismoView.as_view(), name="turismo_home"),
    url(r"clase/nueva/asignatura/(?P<asignatura_id>\d+)/$", TurismoClaseAsignaturaCreateView.as_view(), name="turismo_clase_nueva_asignatura"),
    url(r"clase/nueva$", TurismoClaseCreateView.as_view(), name="turismo_clase_nueva"),
    url(r"clase/(?P<pk>\d+)/editar$", TurismoClaseUpdateView.as_view(), name="turismo_clase_editar"),
    url(r"clase/(?P<pk>\d+)/borrar$", TurismoClaseDeleteView.as_view(), name="turismo_clase_borrar"),
    url(r"curso/(?P<pk>\d+)/borrar/$", TurismoCursoDeleteView.as_view(), name="turismo_curso_borrar"),
    url(r"curso/nuevo/$", TurismoCursoCreateView.as_view(), name="turismo_curso_nuevo"),
    url(r"asignatura/nueva/$", TurismoAsignaturaCreateView.as_view(), name="turismo_asignatura_nueva"),
    url(r"asignatura/(?P<pk>\d+)/$", TurismoAsignaturaDetailView.as_view(), name="turismo_asignatura_detalle"),
    url(r"asistencia/nueva/(?P<asignatura_id>\d+)/$", TurismoAsistenciaCreateView.as_view(), name="turismo_asistencia_nueva"),
    url(r"asistencia/(?P<pk>\d+)/$", TurismoAsistenciaDetailView.as_view(), name="turismo_asistencia_detalle"),
    
]
