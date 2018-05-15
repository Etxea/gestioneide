from django.conf.urls import url
from views import *


urlpatterns = [
    url(r'^$',EmpresaListView.as_view(),name="empresas_lista"),
    url(r'nuevo$',EmpresaCreateView.as_view(), name="empresa_nueva"),
    url(r'editar/(?P<pk>\d+)/$',EmpresaUpdateView.as_view(), name="empresa_editar"),
    url(r'borrar/(?P<pk>\d+)/$',EmpresaDeleteView.as_view(), name="empresa_borrar"),
    url(r'(?P<pk>\d+)/$',EmpresaDetailView.as_view(), name="empresa_detalle"),
]
