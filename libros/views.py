from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required

from gestioneide.models import *

@method_decorator(permission_required('gestioneide.libro_view',raise_exception=True),name='dispatch')
class LibroListView(ListView):
    model=Libro
    paginate_by = 50
    template_name = "libros/libro_list.html"

@method_decorator(permission_required('gestioneide.libro_add',raise_exception=True),name='dispatch')        
class LibroCreateView(CreateView):
    template_name = "libros/libro_form.html"
    model = Libro
    fields = "__all__"
    def get_success_url(self):
        return reverse_lazy("libro_lista")

@method_decorator(permission_required('gestioneide.libro_change',raise_exception=True),name='dispatch')
class LibroUpdateView(UpdateView):
    template_name = "libros/libro_form.html"
    model = Libro
    fields = "__all__"
    def get_success_url(self):
        return reverse_lazy("libro_lista")

@method_decorator(permission_required('gestioneide.libro_delete',raise_exception=True),name='dispatch')
class LibroDeleteView(DeleteView):
    model = Libro
    template_name = "libros/libro_confirm_delete.html"
    def get_success_url(self):
        return reverse_lazy("libro_lista")

@method_decorator(permission_required('gestioneide.libro_view',raise_exception=True),name='dispatch')
class LibroDetailView(DetailView):
    model = Libro
    template_name = "libros/libro_detail.html"
