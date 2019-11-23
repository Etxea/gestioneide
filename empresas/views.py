from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required


from empresas.forms import *

@method_decorator(permission_required('gestioneide.empresa_view',raise_exception=True),name='dispatch')
class EmpresaListView(ListView):
	model=Empresa
	template_name = "empresas/empresa_list.html"

@method_decorator(permission_required('gestioneide.empresa_add',raise_exception=True),name='dispatch')
class EmpresaCreateView(CreateView):
    form_class = EmpresaCreateForm
    template_name = "empresas/empresa_form.html"

    def get_success_url(self):
        return reverse_lazy("empresas_lista")

@method_decorator(permission_required('gestioneide.empresa_view',raise_exception=True),name='dispatch')
class EmpresaDetailView(DetailView):
    model = Empresa
    context_object_name = "empresa"
    template_name = "empresas/empresa_detail.html"

@method_decorator(permission_required('gestioneide.empresa_delete',raise_exception=True),name='dispatch')
class EmpresaDeleteView(DeleteView):
    model = Empresa
    template_name = "empresas/empresa_confirm_delete.html"
    def get_success_url(self):
        return reverse_lazy("empresas_lista")

@method_decorator(permission_required('gestioneide.empresa_change',raise_exception=True),name='dispatch')
class EmpresaUpdateView(UpdateView):
    model = Empresa
    form_class = EmpresaCreateForm
    template_name = "empresas/empresa_update_form.html"

    def get_success_url(self):
        return reverse_lazy("empresas_lista")
