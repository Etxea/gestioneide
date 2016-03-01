from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse, reverse_lazy
from gestioneide.models import *

class LibroListView(ListView):
    model=Libro
    paginate_by = 50
    template_name = "libros/libro_list.html"
        
class LibroCreateView(CreateView):
    template_name = "libros/libro_form.html"
    def get_success_url(self):
        return reverse_lazy("libro_lista")

class LibroUpdateView(UpdateView):
    template_name = "libros/libro_form.html"
    def get_success_url(self):
        return reverse_lazy("libro_lista")


class LibroDeleteView(DeleteView):
    template_name = "libros/libro_deleteconfirm.html"
    def get_success_url(self):
        return reverse_lazy("libro_lista")


class LibroDetailView(DetailView):
    model = Libro
    template_name = "libros/libro_detail.html"
