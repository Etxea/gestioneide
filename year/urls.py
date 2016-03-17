from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required, permission_required
from gestioneide.models import *
from views import *


urlpatterns = [
    url(r'^$', login_required(YearListView.as_view()),name="year_lista"),
    url(r'nuevo$',login_required(YearCreateView.as_view()), name="year_nuevo"),
    url(r'editar/(?P<pk>\d+)/$',login_required(YearUpdateView.as_view()), name="year_editar"),
    url(r'borrar/(?P<pk>\d+)/$',login_required(YearDeleteView.as_view()), name="year_borrar"),
    url(r'activar/$',login_required(year_activate), name="year_activar"),
    url(r'clone/$',login_required(year_clone), name="year_clone"),
    url(r'empty/$',login_required(year_empty), name="year_empty"),
]
