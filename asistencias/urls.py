from django.conf.urls import url
from django.contrib.auth.decorators import login_required, permission_required
from gestioneide.models import *
from views import *


urlpatterns = [
    url(r'^$', login_required(AsistenciaListView.as_view()),name="asistencia_lista"),
    url(r'deleted/$', login_required(AsistenciaDeletedListView.as_view()),name="asistencia_deleted_lista"),
    url(r'nueva$',login_required(AsistenciaCreateView.as_view()), name="asistencia_nuevo"),
    url(r'nueva/alumno/(?P<alumno_id>\d+)$',login_required(AsistenciaAlumnoCreateView.as_view()), name="asistencia_nueva_alumno"),
    url(r'nueva/grupo/(?P<grupo_id>\d+)$',login_required(AsistenciaGrupoCreateView.as_view()), name="asistencia_nueva_grupo"),
    url(r'editar/(?P<pk>\d+)/$',login_required(AsistenciaUpdateView.as_view()), name="asistencia_editar"),
    url(r'borrar/(?P<pk>\d+)/$',login_required(AsistenciaDeleteView.as_view()), name="asistencia_borrar"),
    url(r'recuperar/$',login_required(asistencia_recuperar), name="asistencia_recuperar"),
    url(r'pago/domiciliacion/$',login_required(asistencia_domiciliacion), name="asistencia_set_domiciliacion"),
    #~ url(r'activar/$',login_required(asistencia_activate), name="asistencia_activar"),
    #~ url(r'clone/$',login_required(asistencia_clone), name="asistencia_clone"),
    #~ url(r'empty/$',login_required(asistencia_empty), name="asistencia_empty"),
]
