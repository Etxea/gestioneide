from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.decorators import login_required, permission_required

admin.autodiscover()
from aulas.views import *


urlpatterns = [
    url(r"^$", login_required(ListaAulas.as_view()), name="aulas_lista"),
    url(r"^nueva/$", login_required(NuevaAula.as_view()), name="aula_nueva"),
    url(r"^editar/(?P<pk>\d+)/$", login_required(EditarAula.as_view()), name="aula_editar"),
    url(r"^(?P<pk>\d+)/$", login_required(DetalleAula.as_view()), name="aula_detalle"),
]
