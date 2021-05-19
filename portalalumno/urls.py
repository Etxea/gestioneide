from django.conf.urls import url

from views import *

urlpatterns = [
    url(r'$', PortalAlumnoDetailView.as_view( ),name="portalalumno_index"),
]