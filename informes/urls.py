from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from views import *

from django.contrib.auth.decorators import login_required



urlpatterns = patterns("",
    url(r"^$", login_required(TemplateView.as_view(template_name="informes/home.html")), name="informes")
    #~ url(r"notas/$", EvaluacionListView.as_view(template_name="evaluacion/evaluacion_notas.html"), name="evaluacion_notas"),    
    
)
