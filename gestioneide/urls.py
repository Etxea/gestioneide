from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView

from views import *
from django.contrib import admin

admin.site.site_header = 'Gestion EIDE'
admin.site.site_title = 'GE'
admin.site.index_title = 'Welcome Admin'

urlpatterns = [
    url(r"^$", HomeView.as_view(), name="home"),
    url(r"^admin/", include(admin.site.urls)),
    url(r"^accounts/", include("account.urls")),
    url(r"^alumnos/", include("alumnos.urls")),
    url(r"^grupos/", include("grupos.urls")),
    url(r"^profesores/", include("profesores.urls")),
    url(r"^aulas/", include("aulas.urls")),
    url(r"^clases/", include("clases.urls")),
    url(r"^cursos/", include("cursos.urls")),
    url(r"^calendario/", include("calendario.urls")),
    url(r"^evaluacion/", include("evaluacion.urls")),
    url(r"^facturacion/", include("facturacion.urls")),
    url(r"^informes/", include("informes.urls")),
    url(r"^libros/", include("libros.urls")),
    url(r"^imprimir/", include("imprimir.urls")),
    url(r"^year/", include("year.urls")),
    url(r"^asistencias/", include("asistencias.urls")),
    url(r"^turismo/", include("turismo.urls")),
    url(r"^centros/", include("centros.urls")),
    url(r"^empresas/", include("empresas.urls")),
    url(r"^perfil/", include("perfil.urls")),
    url(r"^mensajes/", include("mensajes.urls")),
    url(r"^consultas/", include("consultas.urls")),
    url(r"^docs/", include("pinax.documents.urls", namespace="pinax_documents")),
    url(r"^messages/", include("pinax.messages.urls", namespace="pinax_messages")),
    url(r"^notifications/", include("pinax.notifications.urls", namespace="pinax_notifications")),
    url(r"^sermepa/", include("sermepa.urls")),
    url(r"^pasarela/", include("pasarela.urls")),
    url(r"^pagosonline/", include("pagosonline.urls")),
    #rl(r"^cambridge/", include("cambridge.urls")),
    url(r"^matriculas/", include("matriculas.urls")),
    url(r'^cookies/', include('cookie_consent.urls')),
    url(r'^hobetuz/', include('hobetuz.urls')),
    url(r'^ticketbai/', include('ticketbai.urls')),
    url(r'^portalalumno/', include('portalalumno.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
