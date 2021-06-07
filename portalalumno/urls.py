from django.conf.urls import url

from views import *

urlpatterns = [
    url(r'$', PortalAlumnoDetailView.as_view( ),name="portalalumno_index"),
    url(r'datos/$', PortalAlumnoDatosView.as_view( ),name="portalalumno_datospersonales"),
    url(r'notas/$', PortalAlumnoNotasView.as_view( ),name="portalalumno_notas"),
    url(r'faltas/$', PortalAlumnoFaltasView.as_view( ),name="portalalumno_faltas"),
    url(r'historico/$', PortalAlumnoHistoricoView.as_view( ),name="portalalumno_historico"),
]