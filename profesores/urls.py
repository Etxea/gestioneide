from django.conf.urls import include, url
from django.views.generic import ListView, DetailView
from django.views.generic.edit import UpdateView

from django.contrib.auth.decorators import login_required, permission_required

from profesores.views import *


urlpatterns = [
    url(r'^$', login_required(ProfesorDashboardView.as_view()),name="profesores_dashboard"),
    url(r'lista/$', login_required(ProfesorListView.as_view()),name="profesores_lista"),
    url(r'nuevo/$',ProfesorCreateView.as_view(), name="profesor_nuevo"),
    url(r'editar/(?P<pk>\d+)/$',ProfesorUpdateView.as_view(), name="profesor_editar"),
    url(r'borrar/(?P<pk>\d+)/$',ProfesorDeleteView.as_view(), name="profesor_borrar"),
    url(r'passwordreset/(?P<pk>\d+)/$',ProfesorPasswordResetView.as_view(), name="profesor_passwordreset"),
    url(r'createuser/(?P<pk>\d+)/$',ProfesorCreateUserView.as_view(), name="profesor_createuser"),
    url(r'disableuser/(?P<pk>\d+)/$',ProfesorDisableUserView.as_view(), name="profesor_disableuser"),
    url(r'enableuser/(?P<pk>\d+)/$',ProfesorEnableUserView.as_view(), name="profesor_enableuser"),
    url(r'(?P<pk>\d+)/$',ProfesorDetailView.as_view(), name="profesor_detalle"),
]
