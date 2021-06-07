# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from django.shortcuts import get_object_or_404

from gestioneide.models import Alumno

class PortalAlumnoDetailView(LoginRequiredMixin, DetailView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    template_name = "portalalumno/alumno_detail.html"
    
    def get_object(self):
        return get_object_or_404(Alumno, pk=self.request.user.alumno.pk)
        #return self.request.user.alumno

class PortalAlumnoDatosView(PortalAlumnoDetailView):
    template_name = "portalalumno/alumno_detail.html"

class PortalAlumnoNotasView(PortalAlumnoDetailView):
    template_name = "portalalumno/alumno_notas.html"

class PortalAlumnoFaltasView(PortalAlumnoDetailView):
    template_name = "portalalumno/alumno_faltas.html"

class PortalAlumnoHistoricoView(PortalAlumnoDetailView):
    template_name = "portalalumno/alumno_historico.html"
