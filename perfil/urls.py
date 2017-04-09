from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from views import *


urlpatterns = [
    url(r'^$', login_required(PerfilListView.as_view()),name="perfil_lista"),
    url(r'nuevo$',login_required(PerfilCreateView.as_view()), name="perfil_nuevo"),
    url(r'editar/(?P<pk>\d+)/$',login_required(PerfilUpdateView.as_view()), name="perfil_editar"),
    url(r'yo/$',login_required(PerfilPropio.as_view()), name="perfil_propio"),
]
