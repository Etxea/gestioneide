from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from views import *

urlpatterns = [
    url(r'^$', login_required(ConsultaListView.as_view()),name="consulta_lista"),
    url(r'nueva/$',login_required(ConsultaCreateView.as_view()), name="consulta_nueva"),
    url(r'enviar/(?P<pk>\d+)/$',login_required(ConsultaEnviarView.as_view()), name="consulta_enviar"),
    url(r'confirmados/(?P<consulta_id>\d+)/$', login_required(ConfirmacionListView.as_view()),name="confirmacion_lista"),
    url(r'confirmar/gracias/$',ConfirmacionGraciasView.as_view(), name="confirmacion_gracias"),
    url(r'confirmar/(?P<consulta_id>\d+)/(?P<asistencia_id>\d+)/$',ConfirmacionCreateView.as_view(), name="confirmacion_nuevo"),
    url(r'(?P<pk>\d+)/$',login_required(ConsultaDetailView.as_view()), name="consulta_detalle"),
    url(r'(?P<pk>\d+)/borrar/$',login_required(ConsultaDeleteView.as_view()), name="consulta_borrar"),
    url(r'(?P<pk>\d+)/editar/$',login_required(ConsultaUpdateView.as_view()), name="consulta_editar"),
]
