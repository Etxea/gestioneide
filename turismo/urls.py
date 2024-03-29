from django.conf.urls import url
from turismo.views import *

urlpatterns = [
    url(r"^$", View.as_view(), name="turismo_home"),
    url(r"clase/nueva/asignatura/(?P<asignatura_id>\d+)/$", ClaseAsignaturaCreateView.as_view(), name="turismo_clase_nueva_asignatura"),
    url(r"clase/nueva$", ClaseCreateView.as_view(), name="turismo_clase_nueva"),
    url(r"clase/(?P<pk>\d+)/editar$", ClaseUpdateView.as_view(), name="turismo_clase_editar"),
    url(r"clase/(?P<pk>\d+)/borrar$", ClaseDeleteView.as_view(), name="turismo_clase_borrar"),
    url(r"curso/(?P<pk>\d+)/borrar/$", CursoDeleteView.as_view(), name="turismo_curso_borrar"),
    url(r"curso/nuevo/$", CursoCreateView.as_view(), name="turismo_curso_nuevo"),
    url(r"asignatura/nueva/$", AsignaturaCreateView.as_view(), name="turismo_asignatura_nueva"),
    url(r"asignatura/(?P<pk>\d+)/$", AsignaturaDetailView.as_view(), name="turismo_asignatura_detalle"),
    url(r"asistencia/nueva/(?P<asignatura_id>\d+)/$", AsistenciaCreateView.as_view(), name="turismo_asistencia_nueva"),
    url(r"asistencia/(?P<pk>\d+)/$", AsistenciaDetailView.as_view(), name="turismo_asistencia_detalle"),

    url(r"pasarlista/$", login_required(PasarListaView.as_view()), name="turismo_pasarlista"),
    url(r"pasarlista/grupo/(?P<pk>\d+)/(?P<mes>\d+)/$", login_required(PasarListaAsignaturaView.as_view()), name="turismo_pasarlista_mes"),

    url(r'falta/nueva/$', login_required(FaltaCreateView.as_view()), name="turismo_falta_nueva"),
    url(r'falta/(?P<pk>\d+)/editar/$', login_required(UpdateView.as_view(model=Falta)), name="turismo_falta_editar"),
    url(r'falta/(?P<pk>\d+)/borrar/$', login_required(FaltaDeleteView.as_view()), name="turismo_falta_borrar"),

    url(r'presente/nueva/$', login_required(PresenciaCreateView.as_view()), name="turismo_presencia_nueva"),
    url(r'presente/(?P<pk>\d+)/editar/$', login_required(UpdateView.as_view(model=Presencia)), name="turismo_presencia_editar"),
    url(r'presente/(?P<pk>\d+)/borrar/$', login_required(PresenciaDeleteView.as_view()), name="turismo_presencia_borrar"),


    url(r'justificada/nueva/$', login_required(JustificadaCreateView.as_view()), name="turismo_justificada_nueva"),
    url(r'justificada/(?P<pk>\d+)/editar/$', login_required(UpdateView.as_view(model=Justificada)),
        name="turismo_justificada_editar"),
    url(r'justificada/(?P<pk>\d+)/borrar/$', login_required(JustificadaDeleteView.as_view()), name="turismo_justificada_borrar")
]
