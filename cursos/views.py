from django.shortcuts import render
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import DeletionMixin
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import render_to_response

## Para el calendario
from calendar import  Calendar

from gestioneide.models import *
from forms import *

class CursosListView(ListView):
    model=Curso
    template_name="cursos/curso_list.html"
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CursosListView, self).dispatch(*args, **kwargs)

class CursoDetailView(DetailView):
    model = Curso
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CursoDetailView, self).dispatch(*args, **kwargs)
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
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CursoUpdateView, self).dispatch(*args, **kwargs)

class CursoDeleteView(DeleteView):
    model = Curso
    def get_success_url(self):
        return reverse_lazy("cursos_lista")

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CursoDeleteView, self).dispatch(*args, **kwargs)


class CursosLibrosListView(ListView):
    model=Libro
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CursosLibrosListView, self).dispatch(*args, **kwargs)

class CursosLibrosCreateView(CreateView):
    model=Libro
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CursosLibrosCreateView, self).dispatch(*args, **kwargs)
class CursoLibrolView(DetailView):
    model = Libro
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CursoLibrolView, self).dispatch(*args, **kwargs)
    
