from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from views import *

from django.contrib.auth.decorators import login_required

urlpatterns = [
    #url(r"^$", login_required(TemplateView.as_view(template_name="informes/home.html")), name="informes"),
    url(r"^$", login_required(InformesHomeView.as_view()), name="informes"),
    url(r"alumnos/errores/$",login_required(AlumnosErroresListView.as_view()),name="listado_alumnos_errores"),
    url(r"alumnos/banco/errores/$",login_required(AlumnosBancoErroresListView.as_view()),name="listado_alumnos_banco_errores"),
    url(r"asistencias/errores/$",login_required(AsistenciasErroresListView.as_view()),name="listado_asistencias_errores"),
    url(r"alumnos/xls/$",login_required(export_alumnos_xls),name="listado_alumnos_xls"),
    url(r"grupos/xls/$",login_required(export_grupos_xls),name="listado_grupos_xls"),
    url(r"alumnos/telefonos/xls/(?P<ano>\d+)/$",login_required(export_telefonos_alumnos_xls),name="listado_telefonos_alumnos_xls"),
    url(r"grupos/alumnos/$",login_required(GruposAlumnosListView.as_view()),name="listado_grupos_alumnos")
    
    #~ url(r"notas/$", EvaluacionListView.as_view(template_name="evaluacion/evaluacion_notas.html"), name="evaluacion_notas"),    
]
