from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from views import *

urlpatterns = [
    url(r'confirmar/crear/$',login_required(ConfirmacionesCrearView.as_view()), name="confirmaciones_crear"),
    url(r'confirmar/lista/$',(ConfirmacionListView.as_view()), name="confirmacion_lista"),
    url(r'confirmar/gracias/$',ConfirmacionGraciasView.as_view(), name="confirmacion_gracias"),
    url(r'confirmar/(?P<pk>\d+)/(?P<password>\w+)/$',ConfirmacionContestarView.as_view(), name="confirmacion_contestar"),
    #url(r'confirmar/enviar/$',login_required(ConfirmacionSendView.as_view()), name="confirmacion_envio"),
    url(r'nueva/$',login_required(ConsultaCreateView.as_view()), name="consulta_nueva"),
    url(r'enviar/(?P<pk>\d+)/$',login_required(ConsultaEnviarView.as_view()), name="consulta_enviar"),
    url(r'consultas/$', login_required(ConsultaListView.as_view()),name="consulta_lista"),
    url(r'respuesta/(?P<consulta_id>\d+)/(?P<alumno_id>\d+)$', RespuestaCreateView.as_view(),name="consulta_responder"),
    url(r'consulta/(?P<pk>\d+)/$',login_required(ConsultaDetailView.as_view()), name="consulta_detalle"),
    url(r'consulta/(?P<pk>\d+)/borrar/$',login_required(ConsultaDeleteView.as_view()), name="consulta_borrar"),
    url(r'consulta/(?P<pk>\d+)/editar/$',login_required(ConsultaUpdateView.as_view()), name="consulta_editar"),
]
