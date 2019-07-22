from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required

from gestioneide.models import *
from centros.forms import *

@method_decorator(permission_required('gestioneide.centro_view',raise_exception=True),name='dispatch')
class CentroListView(ListView):
	model=Centro
	template_name = "centros/centro_list.html"

@method_decorator(permission_required('gestioneide.centro_add',raise_exception=True),name='dispatch')
class CentroCreateView(CreateView):
    form_class = CentroCreateForm
    template_name = "centros/centro_form.html"

    def get_success_url(self):
        return reverse_lazy("centros_lista")

@method_decorator(permission_required('gestioneide.centro_view',raise_exception=True),name='dispatch')
class CentroDetailView(DetailView):
    model = Centro
    context_object_name = "centro"
    template_name = "centros/centro_detail.html"

@method_decorator(permission_required('gestioneide.centro_delete',raise_exception=True),name='dispatch')
class CentroDeleteView(DeleteView):
    model = Centro
    template_name = "centros/centro_confirm_delete.html"
    def get_success_url(self):
        return reverse_lazy("centros_lista")

@method_decorator(permission_required('gestioneide.centro_change',raise_exception=True),name='dispatch')
class CentroUpdateView(UpdateView):
    model = Centro
    form_class = CentroCreateForm
    template_name = "centros/centro_update_form.html"

    def get_success_url(self):
        return reverse_lazy("centros_lista")
