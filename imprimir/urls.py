from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required, permission_required
from views import *

urlpatterns = [
    url(r'grupos$',login_required(ImprimirGrupos.as_view()), name="imprimir_grupos"),
    url(r'grupos/alumnos/$',login_required(ImprimirGruposAlumnos.as_view()), name="imprimir_grupos_alumnos"),
    url(r'grupos/alumnos/id/(?P<grupo_id>\d+)/$',login_required(ImprimirGruposAlumnos.as_view()),  name="imprimir_grupo_unico_alumnos"),
    url(r'grupos/planilla/asistencia/(?P<mes>\d+)/$',login_required(ImprimirGruposPlanillaAsistencia.as_view()), name="imprimir_grupos_planilla_asistencia"),
    url(r'alumno/matricula/(?P<alumno_id>\d+)/$',login_required(ImprimirAlumnoMatricula.as_view()), name="imprimir_alumno_matricula"),
    url(r'alumno/octavilla/(?P<alumno_id>\d+)/$',login_required(ImprimirAlumnoOctavilla.as_view()), name="imprimir_alumno_octavilla"),
    url(r'alumnos/carta/faltas/(?P<mes>\d+)/$',login_required(ImprimirAlumnosCartaFaltas.as_view()), name="imprimir_alumnos_cartas_falta"),
    url(r'asistencia/(?P<asistencia_id>\d+)/horario$',login_required(ImprimirAsistenciaHorario.as_view()), name="imprimir_asistencia_horario"),
]
