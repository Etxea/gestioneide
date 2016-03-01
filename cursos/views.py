from django.shortcuts import render
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import DeletionMixin
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import render_to_response

## Para el calendario
from calendar import  Calendar

from gestioneide.models import *
from forms import *

class CursosListView(ListView):
    model=Curso
    template_name="cursos/curso_list.html"

class CursoDetailView(DetailView):
    model = Curso
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(CursoDetailView, self).get_context_data(**kwargs)
        # Add extra...
        data = {'curso': self.object.id}
        context['clase_form'] = ClaseForm(initial=data)
        return context

class CursoUpdateView(UpdateView):
    model = Curso
    fields = "__all__"
    template_name="cursos/curso_form.html"

class CursoDeleteView(DeleteView):
    model = Curso
    def get_success_url(self):
        return reverse_lazy("cursos_lista")

class CursosLibrosListView(ListView):
    model=Libro

class CursosLibrosCreateView(CreateView):
    model=Libro

class CursoLibrolView(DetailView):
    model = Libro
    
