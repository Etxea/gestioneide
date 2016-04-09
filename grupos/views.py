from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from forms import *
from gestioneide.models import *
import calendar

from django_xhtml2pdf.utils import render_to_pdf_response


class GrupoListView(ListView):
    model=Grupo
    paginate_by = 50
    template_name = "grupos/grupo_list.html"
    def get_queryset(self):
        year = Year.objects.get(activo=True)
        #~ print "Listamos los grupos del ano",year
        return Grupo.objects.filter(year=year).order_by('nombre')
        
class GrupoCreateView(CreateView):
    form_class = GrupoCreateForm
    template_name = "grupos/grupo_form.html"

    def get_success_url(self):
        return reverse_lazy("grupo_lista")

class GrupoDetailView(DetailView):
    model = Grupo
    template_name = "grupos/grupo_detail.html"

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

class GrupoNotasView(DetailView):
    model = Grupo
    template_name = "grupos/grupo_planilla_notas.html"
    def get_context_data(self, **kwargs):
        context = super(GrupoNotasView, self).get_context_data(**kwargs)
        context['trimestre'] = self.kwargs['trimestre']
        conceptos = ['Grammar','lalala','lelele']
        context['conceptos'] = conceptos
        return context


class GrupoDeleteView(DeleteView):
    model = Grupo
    template_name = "grupos/grupo_confirm_delete.html"    
    def get_success_url(self):
        return reverse_lazy("grupo_lista")

class GrupoUpdateView(UpdateView):
    model = Grupo
    form_class = GrupoCreateForm
    template_name = "grupos/object_update_form.html"

    def get_success_url(self):
        return reverse_lazy("grupo_lista")
