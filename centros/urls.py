from django.conf.urls import url

from views import *

urlpatterns = [
    url(r'^$',CentroListView.as_view(),name="centros_lista"),
    url(r'nuevo$',CentroCreateView.as_view(), name="centro_nuevo"),
    url(r'editar/(?P<pk>\d+)/$',CentroUpdateView.as_view(), name="centro_editar"),
    url(r'borrar/(?P<pk>\d+)/$',CentroDeleteView.as_view(), name="centro_borrar"),
    url(r'(?P<pk>\d+)/$',CentroDetailView.as_view(), name="centro_detalle"),
]
