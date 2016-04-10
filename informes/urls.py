from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from views import *

from django.contrib.auth.decorators import login_required



urlpatterns = [
    url(r"^$", login_required(TemplateView.as_view(template_name="informes/home.html")), name="informes"),
    url(r"alumnos/errores/$",login_required(AlumnosErroresListView.as_view()),name="listado_alumnos_errores"),
    url(r"asistencias/errores/$",login_required(AsistenciasErroresListView.as_view()),name="listado_asistencias_errores"),
    url(r"alumnos/xls/$",login_required(export_alumnos_xls),name="listado_alumnos_xls")
    
    #~ url(r"notas/$", EvaluacionListView.as_view(template_name="evaluacion/evaluacion_notas.html"), name="evaluacion_notas"),    
]
