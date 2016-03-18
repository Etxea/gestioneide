from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.views.generic import TemplateView

from django.contrib import admin


urlpatterns = [
    url(r"^$", TemplateView.as_view(template_name="homepage.html"), name="home"),
    url(r"^admin/", include(admin.site.urls)),
    url(r"^accounts/", include("account.urls")),
    url(r"^alumnos/", include("alumnos.urls")),
    url(r"^grupos/", include("grupos.urls")),
    url(r"^profesores/", include("profesores.urls")),
    url(r"^aulas/", include("aulas.urls")),
    url(r"^cursos/", include("cursos.urls")),
    url(r"^calendario/", include("calendario.urls")),
    url(r"^evaluacion/", include("evaluacion.urls")),
    url(r"^importar/", include("importar.urls")),
    url(r"^facturacion/", include("facturacion.urls")),
    url(r"^informes/", include("informes.urls")),
    url(r"^libros/", include("libros.urls")),
    url(r"^imprimir/", include("imprimir.urls")),
    url(r"^year/", include("year.urls")),
    url(r"^asistencias/", include("asistencias.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
