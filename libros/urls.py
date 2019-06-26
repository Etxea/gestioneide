from django.conf.urls import url
from django.contrib.auth.decorators import login_required, permission_required
from gestioneide.models import *
from views import *


urlpatterns = [
    url(r'^$', login_required(LibroListView.as_view()),name="libro_lista"),
    url(r'nuevo$',login_required(LibroCreateView.as_view()), name="libro_nuevo"),
    url(r'editar/(?P<pk>\d+)/$',login_required(LibroUpdateView.as_view()), name="libro_editar"),
    url(r'borrar/(?P<pk>\d+)/$',login_required(LibroDeleteView.as_view()), name="libro_borrar"),
]
