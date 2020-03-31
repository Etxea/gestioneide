from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required
from datetime import date 

from pinax.documents.models import *

from gestioneide.models import *
from profesores.forms import *

class ProfesorListView(ListView):
	model=Profesor
	template_name = "profesores/profesor_list.html"

#@method_decorator(permission_required('gestioneide.profesor_view',raise_exception=True),name='dispatch')
class ProfesorDashboardView(ListView):
    model=Profesor
    template_name = "profesores/profesor_dashboad.html"
    context_object_name = 'profesor'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ProfesorDashboardView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['mes'] = date.today().month
        context['folders'] = Folder.objects.for_user(self.request.user)
        return context

    def get_queryset(self):
        return Profesor.objects.get(user=self.request.user)


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
