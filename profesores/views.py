from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required

from gestioneide.models import *
from profesores.forms import *

class ProfesorListView(ListView):
	model=Profesor
	template_name = "profesores/profesor_list.html"

@method_decorator(permission_required('gestioneide.profesor_add',raise_exception=True),name='dispatch')
class ProfesorCreateView(CreateView):
    form_class = ProfesorCreateForm
    template_name = "profesores/profesor_form.html"

    def get_success_url(self):
        return reverse_lazy("profesores_lista")

@method_decorator(permission_required('gestioneide.profesor_view',raise_exception=True),name='dispatch')
class ProfesorDetailView(DetailView):
    model = Profesor
    context_object_name = "profesor"
    template_name = "profesores/profesor_detail.html"

@method_decorator(permission_required('gestioneide.profesor_delete',raise_exception=True),name='dispatch')
class ProfesorDeleteView(DeleteView):
    model = Profesor
    template_name = "profesores/profesor_confirm_delete.html"
    def get_success_url(self):
        return reverse_lazy("profesores_lista")

@method_decorator(permission_required('gestioneide.profesor_change',raise_exception=True),name='dispatch')
class ProfesorUpdateView(UpdateView):
    model = Profesor
    form_class = ProfesorCreateForm
    template_name = "profesores/profesor_update_form.html"

    def get_success_url(self):
        return reverse_lazy("profesores_lista")
