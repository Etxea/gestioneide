from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required
from forms import *
from gestioneide.models import *
import calendar

@method_decorator(permission_required('gestioneide.grupo_view',raise_exception=True),name='dispatch')
class GrupoListView(ListView):
    model=Grupo
    paginate_by = 100
    template_name = "grupos/grupo_list.html"
    def get_queryset(self):
        year = Year.objects.get(activo=True)
        #Si es staff ve todos los grupos
        if self.request.user.is_staff:
            return Grupo.objects.filter(year=year).order_by('nombre')
        #Sino limitamos los grupos a los cuales el profesor da clase
        else:
            return Grupo.objects.filter(clases__in=Clase.objects.filter(profesor=Profesor.objects.get(user_id=self.request.user.id)))

@method_decorator(permission_required('gestioneide.grupo_add',raise_exception=True),name='dispatch')        
class GrupoCreateView(CreateView):
    form_class = GrupoCreateForm
    template_name = "grupos/grupo_form.html"
    def get_success_url(self):
        return reverse_lazy("grupo_lista")


@method_decorator(permission_required('gestioneide.grupo_view',raise_exception=True),name='dispatch')
class GrupoDetailView(DetailView):
    model = Grupo
    template_name = "grupos/grupo_detail.html"

@method_decorator(permission_required('gestioneide.grupo_view',raise_exception=True),name='dispatch')
class GrupoAsistenciaView(DetailView):
    model = Grupo
    template_name = "grupos/grupo_planilla_asistencias.html"
    def get_context_data(self, **kwargs):
        context = super(GrupoAsistenciaView, self).get_context_data(**kwargs)
        cal = calendar.Calendar()
        mes = int(self.kwargs['mes'])
        mes_nombre = calendar.month_name[mes]
        context['mes'] = mes
        context['mes_nombre'] = mes_nombre      
        return context

@method_decorator(permission_required('gestioneide.grupo_view',raise_exception=True),name='dispatch')
class GrupoNotasView(DetailView):
    model = Grupo
    template_name = "grupos/grupo_planilla_notas.html"
    def get_context_data(self, **kwargs):
        context = super(GrupoNotasView, self).get_context_data(**kwargs)
        context['trimestre'] = self.kwargs['trimestre']
        conceptos = ['Grammar','lalala','lelele']
        context['conceptos'] = conceptos
        return context

@method_decorator(permission_required('gestioneide.grupo_delete',raise_exception=True),name='dispatch')
class GrupoDeleteView(DeleteView):
    model = Grupo
    template_name = "grupos/grupo_confirm_delete.html"    
    def get_success_url(self):
        return reverse_lazy("grupo_lista")

@method_decorator(permission_required('gestioneide.grupo_change',raise_exception=True),name='dispatch')
class GrupoUpdateView(UpdateView):
    model = Grupo
    form_class = GrupoCreateForm
    template_name = "grupos/object_update_form.html"

    def get_success_url(self):
        return reverse_lazy("grupo_lista")
