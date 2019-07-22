from django.conf.urls import url
from django.contrib.auth.decorators import login_required, permission_required
from imprimir.views import *

urlpatterns = [
    url(r'grupos$',login_required(ImprimirGrupos.as_view()), name="imprimir_grupos"),
    url(r'grupos/alumnos/$',login_required(ImprimirGruposAlumnos.as_view()), name="imprimir_grupos_alumnos"),
    url(r'grupos/alumnos/id/(?P<grupo_id>\d+)/$',login_required(ImprimirGruposAlumnos.as_view()),  name="imprimir_grupo_unico_alumnos"),
    url(r'grupos/planilla/asistencia/(?P<mes>\d+)/$',login_required(ImprimirGruposPlanillaAsistencia.as_view()), name="imprimir_grupos_planilla_asistencia"),
    url(r'alumno/matricula/(?P<alumno_id>\d+)/$',login_required(ImprimirAlumnoMatricula.as_view()), name="imprimir_alumno_matricula"),
    url(r'alumno/octavilla/(?P<alumno_id>\d+)/$',login_required(ImprimirAlumnoOctavilla.as_view()), name="imprimir_alumno_octavilla"),
    url(r'alumnos/carta/faltas/(?P<mes>\d+)/$',login_required(ImprimirAlumnosCartaFaltas.as_view()), name="imprimir_alumnos_cartas_falta"),
    url(r'asistencia/(?P<asistencia_id>\d+)/horario$',login_required(ImprimirAsistenciaHorario.as_view()), name="imprimir_asistencia_horario"),
    url(r'alumnos/carta/notas/trimestre/(?P<trimestre>\d+)/(?P<grupo_id>\d+)/$',login_required(ImprimirCartaNotasTrimestre.as_view()), name="imprimir_alumnos_notas_trimestre"),
    url(r'alumnos/carta/notas/trimestre/(?P<trimestre>\d+)/(?P<grupo_id>\d+)/html$',login_required(ImprimirCartaNotasTrimestreHtml.as_view()), name="imprimir_alumnos_notas_trimestre_html"),
    url(r'alumnos/carta/notas/cuatrimestre/(?P<cuatrimestre>\d+)/(?P<grupo_id>\d+)/$',login_required(ImprimirCartaNotasCuatrimestre.as_view()), name="imprimir_alumnos_notas_cuatrimestre"),
    url(r'alumnos/carta/notas/final/$',login_required(ImprimirCartaNotasFinal.as_view()), name="imprimir_alumnos_notas_final"),
]
