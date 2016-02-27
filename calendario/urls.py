from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()
from views import *


urlpatterns = patterns("",
    url(r"^$", CalendarioFestivos.as_view(), name="festivos_calendario"),
    url(r"^nuevo/(?P<ano>\d+)/(?P<mes>\d+)/(?P<dia>\d+)/$", NuevoFestivo.as_view(), name="festivo_nuevo"),
    url(r"^nuevo/$", NuevoFestivo.as_view(), name="festivo_nuevo"),
    url(r"^lista/$", ListaFestivos.as_view(), name="festivos_lista"),
    url(r"^editar/(?P<pk>\d+)/$", EditarFestivo.as_view(), name="festivo_editar"),
    url(r"^borrar/(?P<pk>\d+)/$", BorrarFestivo.as_view(), name="festivo_borrar"),
    url(r"^(?P<pk>\d+)/$", DetalleFestivo.as_view(), name="festivo_detalle"),
    )
