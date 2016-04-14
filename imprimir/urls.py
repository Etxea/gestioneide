from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required, permission_required
from views import *

urlpatterns = [
    url(r'grupos$',login_required(ImprimirGrupos), name="imprimir_grupos"),
    url(r'grupos/alumnos/$',login_required(ImprimirGruposAlumnos), name="imprimir_grupos_alumnos"),
    url(r'grupos/planilla/asistencia/(?P<mes>\d+)/$',login_required(ImprimirGruposPlanillaAsistencia), name="imprimir_grupos_planilla_asistencia"),
    url(r'alumno/matricula/(?P<alumno_id>\d+)/$',login_required(ImprimirAlumnoMatricula), name="imprimir_alumno_matricula"),
    url(r'alumno/octavilla/(?P<alumno_id>\d+)/$',login_required(ImprimirAlumnoOctavilla), name="imprimir_alumno_octavilla"),
]
