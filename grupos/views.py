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
        
class GrupoCreateView(CreateView):
    form_class = GrupoCreateForm
    template_name = "grupos/grupo_form.html"

    def get_success_url(self):
        return reverse_lazy("grupo_lista")

class GrupoDetailView(DetailView):
    model = Grupo
    template_name = "grupos/object_detail.html"

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
        grupo = context['object']
        dias_semana_clase = []
        dias_clase = []
        for dia in grupo.clases.all():
            dias_semana_clase.append(dia.dia_semana)
        
        #FIXME esto habria que sacarlo de algun lado
        ano = 2015
        if mes < 8 :
            ano = ano + 1 
        context['ano'] = ano
        for semana in cal.monthdays2calendar(ano,mes):
            for dia in semana:
				#COmprobamos que ese dia de la semana haya clase y no sea 0 (es de otro mes)
                if ( dia[1] in dias_semana_clase ) and ( dia[0] > 0 ):
                    fecha = "%s-%s-%s"%(ano,mes,dia[0])
                    try:
                        festivo = Festivo.objects.get(fecha=fecha)
                        continue
                    except:
                        dias_clase.append(dia[0])
        context['dias_clase'] = dias_clase
      
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
    def get_success_url(self):
        return reverse_lazy("grupo_lista")

class GrupoUpdateView(UpdateView):
    model = Grupo
    form_class = GrupoCreateForm
    template_name = "grupos/object_update_form.html"

    def get_success_url(self):
        return reverse_lazy("grupo_lista")
