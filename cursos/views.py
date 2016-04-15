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
    paginate_by = 50

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
    def get_success_url(self):
        return reverse_lazy("cursos_lista")

class CursoDeleteView(DeleteView):
    model = Curso
    template_name="cursos/curso_confirm_delete.html"
    def get_success_url(self):
        return reverse_lazy("cursos_lista")

class CursoCreateView(CreateView):
    model = Curso
    fields = "__all__"
    template_name="cursos/curso_form.html"
    def get_success_url(self):
        return reverse_lazy("cursos_lista")

##Libros
class LibroCreateView(CreateView):
    model = Libro
    fields = "__all__"
    template_name="cursos/libro_form.html"

class LibroListView(ListView):
    model=Libro

class LibrolView(DetailView):
    model = Libro
    
