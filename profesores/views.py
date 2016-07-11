from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse, reverse_lazy
from gestioneide.models import *
from forms import *

class ProfesorListView(ListView):
	model=Profesor
	template_name = "profesores/profesor_list.html"

class ProfesorCreateView(CreateView):
    form_class = ProfesorCreateForm
    template_name = "profesores/profesor_form.html"

    def get_success_url(self):
        return reverse_lazy("profesores_lista")

class ProfesorDetailView(DetailView):
    model = Profesor
    context_object_name = "profesor"
    template_name = "profesores/profesor_detail.html"

class ProfesorDeleteView(DeleteView):
    model = Profesor
    template_name = "profesores/profesor_confirm_delete.html"
    def get_success_url(self):
        return reverse_lazy("profesores_lista")

class ProfesorUpdateView(UpdateView):
    model = Profesor
    form_class = ProfesorCreateForm
    template_name = "profesores/profesor_update_form.html"

    def get_success_url(self):
        return reverse_lazy("profesores_lista")

        
