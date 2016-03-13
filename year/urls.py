from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required, permission_required
from gestioneide.models import *
from views import *


urlpatterns = [
    url(r'^$', login_required(YearListView.as_view()),name="year_lista"),
    url(r'nuevo$',login_required(YearCreateView.as_view()), name="year_nuevo"),
    url(r'editar/(?P<pk>\d+)/$',login_required(YearUpdateView.as_view()), name="year_editar"),
    url(r'borrar/(?P<pk>\d+)/$',login_required(YearDeleteView.as_view()), name="year_borrar"),
    url(r'activar/(?P<pk>\d+)/$',login_required(YearActivateView.as_view()), name="year_activar"),
]
