# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, FormView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.core.urlresolvers import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required

from models import *

class ConsultaListView(ListView):
    model = Consulta

class ConsultaCreateView(CreateView):
    model = Consulta
    fields = '__all__'

class ConsultaDetailView(DetailView):
    model = Consulta

class ConsultaEnviarView(DetailView):
    model = Consulta    
    template_name = 'confirmaciones/consulta_enviar.html'
    def post(self, request, *args, **kwargs):
        consul = Consulta.objects.get(id=self.kwargs['pk'])
        consul.enviar()
        return reverse_lazy("consulta_lista")

class ConsultaDeleteView(DeleteView):
    model = Consulta

class ConsultaUpdateView(UpdateView):
    model = Consulta

class ConfirmacionListView(ListView):
    model = Confirmacion

class ConfirmacionCreateView(CreateView):
    model = Confirmacion
    fields = '__all__'
