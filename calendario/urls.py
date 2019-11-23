from django.conf.urls import url
from django.contrib.auth.decorators import login_required, permission_required

from django.contrib import admin
admin.autodiscover()
from calendario.views import *


urlpatterns = [
    url(r"^$", login_required(CalendarioFestivos.as_view()), name="festivos_calendario"),
    url(r"^nuevo/(?P<ano>\d+)/(?P<mes>\d+)/(?P<dia>\d+)/$", login_required(NuevoFestivo.as_view()), name="festivo_nuevo"),
    url(r"^nuevo/$", login_required(NuevoFestivo.as_view()), name="festivo_nuevo"),
    url(r"^lista/$", login_required(ListaFestivos.as_view()), name="festivos_lista"),
    url(r"^editar/(?P<pk>\d+)/$", login_required(EditarFestivo.as_view()), name="festivo_editar"),
    url(r"^borrar/(?P<pk>\d+)/$", login_required(BorrarFestivo.as_view()), name="festivo_borrar"),
    url(r"^(?P<pk>\d+)/$", login_required(DetalleFestivo.as_view()), name="festivo_detalle"),
]
