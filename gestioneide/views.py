# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from gestioneide.models import Alumno
from matriculas.models import MatriculaCurso, MatriculaEide, MatriculaLinguaskill

class HomeView(TemplateView,LoginRequiredMixin):
    login_url = '/accounts/login/'
    redirect_field_name = 'redirect_to'
    template_name='home.html'

    def get_context_data(self, **kwargs):
        context = super(TemplateView,self).get_context_data(**kwargs)
        context['ultimos_alumnos'] = Alumno.objects.all().order_by('-id')[:5]
        context['ultimas_matriculas_cursos'] = MatriculaCurso.objects.all().order_by('-id')[:5]
        context['ultimas_matriculas_eide'] = MatriculaEide.objects.all().order_by('-id')[:5]
        context['ultimas_matriculas_ls'] = MatriculaLinguaskill.objects.all().order_by('-id')[:5]
        return context