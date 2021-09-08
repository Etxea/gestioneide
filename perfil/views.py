from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required

from gestioneide.models import Perfil

@method_decorator(permission_required('gestioneide.perfil_add',raise_exception=True),name='dispatch')
class PerfilListView(ListView):
    model=Perfil
    paginate_by = 50
    template_name = "perfil/perfil_list.html"

@method_decorator(permission_required('gestioneide.perfil_add',raise_exception=True),name='dispatch')
class PerfilCreateView(CreateView):
    template_name = "perfil/perfil_form.html"
    model = Perfil
    fields = "__all__"
    def get_success_url(self):
        return reverse_lazy("perfil_lista")

@method_decorator(permission_required('gestioneide.perfil_add',raise_exception=True),name='dispatch')
class PerfilUpdateView(UpdateView):
    template_name = "perfil/perfil_form.html"
    model = Perfil
    fields = "__all__"
    def get_success_url(self):
        return reverse_lazy("perfil_lista")

@method_decorator(permission_required('gestioneide.perfil_add',raise_exception=True),name='dispatch')
class PerfilPropio(UpdateView):
    template_name = "perfil/perfil_form.html"
    model = Perfil
    fields = ['ano_activo']
    def get_object(self):
        return Perfil.objects.get(user=self.request.user)
    def get_success_url(self):
        return reverse_lazy("home")