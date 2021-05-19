# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, FormView, TemplateView
#from django.views.generic.edit import CreateView, UpdateView, DeleteView
#from django.contrib.auth.models import User
#from django.core.urlresolvers import reverse, reverse_lazy
#from django.http import HttpResponseRedirect
#from django.utils.decorators import method_decorator
#from django.contrib.auth.decorators import login_required, permission_required

from gestioneide.models import Alumno

class PortalAlumnoDetailView(LoginRequiredMixin, DetailView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    template_name = "portalalumno/alumno_detail.html"
    
    def get_object(self):
        #return get_object_or_404(Alumno, pk=self.request.user.alumno.pk)
        return self.request.user.alumno


