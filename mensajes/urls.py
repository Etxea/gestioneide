from django.conf.urls import patterns, include, url
from views import *

from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r"^$", login_required(MensajesListView.as_view()), name="mensajes"),
    url(r'nuevo$',login_required(MensajeCreateView.as_view()), name="mensaje_nuevo"),
    url(r'nuevo/todos$',login_required(MensajeAllView.as_view()), name="mensaje_todos_nuevo"),
    url(r'ver/(?P<pk>\d+)/$',login_required(MensajeDetailView.as_view()), name="mensaje_ver"),
    url(r'responder/(?P<mensaje_id>\d+)/$',login_required(MensajeRespuestaCreateView.as_view()), name="mensaje_responder"),
]