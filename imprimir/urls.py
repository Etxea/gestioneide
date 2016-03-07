from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required, permission_required
from views import *

urlpatterns = patterns('',
    url(r'grupos$',login_required(ImprimirGrupos), name="imprimir_grupos"),
    url(r'grupos/planilla/asistencia/(?P<mes>\d+)/$',login_required(ImprimirGruposPlanillaAsistencia), name="imprimir_grupos_planilla_asistencia"),
)
