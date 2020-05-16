# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.generic import TemplateView, ListView, CreateView, DeleteView, DetailView, View
from django.core.urlresolvers import reverse, reverse_lazy

from django.shortcuts import render
from models import *
from forms import *

class MatriculaEideCreateView(CreateView):
    model = MatriculaEide
    template_name = "matriculas/matricula_eide_nueva.html"
    from_class = MatriculaEideForm
    fields = '__all__'

class MatriculaEideListView(ListView):
    model = MatriculaEide
    template_name = "matriculas/matricula_eide_lista.html"

class MatriculaEideDetailView(DetailView):
    model = MatriculaEide
    template_name = "matriculas/matricula_eide_detalle.html"
