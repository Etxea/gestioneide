## FIXME habria que renombrar las clases para que sean CamelCase , editar tambien en urls.
## FIXME habria que eliminar o al menos comentar lo que no se use

from django.shortcuts import render, render_to_response
from django.template import RequestContext
#from utils import _getWeekDetails
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required
import datetime
from gestioneide.models import *
from clases.forms import *

@method_decorator(permission_required('gestioneide.clase_add',raise_exception=True),name='dispatch')
class ClaseCreateView(CreateView):
    model = Clase
    form_class = ClaseForm

@method_decorator(permission_required('gestioneide.clase_delete',raise_exception=True),name='dispatch')
class ClaseDeleteView(DeleteView):
    model = Clase
    def get_success_url(self):
        return reverse_lazy("grupo_detalle", kwargs={'pk': self.object.grupo.pk})

@method_decorator(permission_required('gestioneide.clase_add',raise_exception=True),name='dispatch')
class ClaseCursoCreateView(ClaseCreateView):
    ##Recogemos los datos iniciales (clientes)
    def get_initial(self):
        super(ClaseCursoCreateView, self).get_initial()
        cliente = Cliente.objects.get(pk=self.kwargs['cliente_id'])
        user = self.request.user
        self.initial = {"cliente":cliente.id}
        return self.initial

def calendario_mes(request,curso_id,ano,mes):
    ano = int(ano)
    mes = int(mes)
    cal = HTMLCalendar()
    
    dias_semana = []
    curso = Curso.objects.get(id=curso_id)
    for clase in curso.clase_set.all():
        dias_semana.append(clase.dia_semana-1)
    dias_clase = []
    
    
    c = Calendar()
    for d in c.itermonthdates(ano,mes):
        if d.weekday() in dias_semana:
            #evitamos recibir los dias que no son del mes que toca
            if d.month == mes:
                dias_clase.append(d.day)
            
    cal = ClasesCalendar(dias_clase)
    calendario = cal.formatmonth(ano,mes)
    return render_to_response('cursos/mes.html', {'calendario': calendario, "ano": ano, "mes": mes})




def vista_semana(request, numero):
    #datos_semana=_getWeekDetails(numero, 2013,2)
    inicio_semana = datetime.date(datos_semana[0].tm_year,datos_semana[0].tm_mon,datos_semana[0].tm_mday)
    fin_semana = datetime.date(datos_semana[1].tm_year,datos_semana[1].tm_mon,datos_semana[1].tm_mday)
    #cuartos = { "1": 00; "2": 15, "3": 30, "4": 45  }
    return render_to_response('ocupacion_semana.html', {"numero_semana": numero, "inicio_semana": inicio_semana, "fin_semana": fin_semana})

def vista_semana_aula(request, numero):
    #datos_semana=_getWeekDetails(numero, 2014,2)
    inicio_semana = datetime.date(datos_semana[0].tm_year,datos_semana[0].tm_mon,datos_semana[0].tm_mday)
    fin_semana = datetime.date(datos_semana[1].tm_year,datos_semana[1].tm_mon,datos_semana[1].tm_mday)
    #cuartos = { "1": 00; "2": 15, "3": 30, "4": 45  }
    return render_to_response('ocupacion_semana.html', {"numero_semana": numero, "inicio_semana": inicio_semana, "fin_semana": fin_semana})



dias_semana = ["lunes","martes","miercoles","jueves","viernes"]

class Semana():
    lunes = None
    martes = None
    miercoles = None
    jueves = None
    viernes = None

def vista_semana_aula(request, numero, id_aula):
    aula = Aula.objects.get(id=id_aula)
    aulas = Aula.objects.all()
    datos_semana=_getWeekDetails(numero, 2014,2)
    inicio_semana = datetime.date(datos_semana[0].tm_year,datos_semana[0].tm_mon,datos_semana[0].tm_mday)
    fin_semana = datetime.date(datos_semana[1].tm_year,datos_semana[1].tm_mon,datos_semana[1].tm_mday)
    count = 0
    clases_semana = []
    for dia in dias_semana:
        clases = programacion_aula_dia(aula,inicio_semana+datetime.timedelta(days=count))
        clases_semana.append({"nombre": dia, "clases":clases})
        count += 1
    
    return render(request,'ocupacion_semana_aula.html',\
        {"numero_semana": numero, "inicio_semana": inicio_semana, "fin_semana": fin_semana, \
        "clases_semana": clases_semana,"aula": aula, "aulas": aulas},context_instance=RequestContext(request),content_type='text/html')


def vista_semana_profesor(request, numero, id_profesor):
    profesor = Profesor.objects.get(id=id_profesor)
    profesores = Profesor.objects.all()
    datos_semana=_getWeekDetails(numero, 2013,2)
    inicio_semana = datetime.date(datos_semana[0].tm_year,datos_semana[0].tm_mon,datos_semana[0].tm_mday)
    fin_semana = datetime.date(datos_semana[1].tm_year,datos_semana[1].tm_mon,datos_semana[1].tm_mday)
    count = 0
    clases_semana = []
    for dia in dias_semana:
        clases = programacion_profesor_dia(profesor,inicio_semana+datetime.timedelta(days=count))
        clases_semana.append({"nombre": dia, "clases":clases})
        count += 1
    return render(request,'ocupacion_semana_profesor.html', \
        {"numero_semana": numero, "inicio_semana": inicio_semana, "fin_semana": fin_semana, \
        "clases_semana": clases_semana,"profesor": profesor, "profesores": profesores})

@method_decorator(permission_required('gestioneide.clase_view',raise_exception=True),name='dispatch')
#Fixme que solo lo vea el admin  el propio profe
class clases_profesor(ListView):
    model = Clase
    context_object_name = "clases_list"
    template_name = "clases_profesor.html"
    ##Listamos las clases del profesor
    def get_queryset(self):
        #print "Buscamos el profesor con el id",self.args[0]
        self.profesor = get_object_or_404(Profesor, id=self.args[0])
        return Clase.objects.filter(profesor=self.profesor)
        
    ## Anadimos el profesor al contexto
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(clases_profesor, self).get_context_data(**kwargs)
        # Add in the publisher
        context['profesor'] = self.profesor
        return context

@method_decorator(permission_required('gestioneide.clase_view',raise_exception=True),name='dispatch')        
class clases_lista_profesores(ListView):
    model = Profesor
    template_name="clases_profesores.html"
    context_object_name = "profesores_list"
    ## Anadimos el numero de esta semana
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(clases_lista_profesores, self).get_context_data(**kwargs)
        # Add in the publisher
        hoy = datetime.date.today()
        context['num_semana'] = hoy.isocalendar()[1]
        return context

@method_decorator(permission_required('gestioneide.clase_view',raise_exception=True),name='dispatch')    
class clases_lista_aulas(ListView):
    model = Aula
    template_name="clases_aulas.html"
    context_object_name = "aulas_list"
    ## Anadimos el numero de esta semana
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(clases_lista_aulas, self).get_context_data(**kwargs)
        # Add in the publisher
        hoy = datetime.date.today()
        context['num_semana'] = hoy.isocalendar()[1]
        return context

@method_decorator(permission_required('gestioneide.clase_view',raise_exception=True),name='dispatch')
class clases_aula(ListView):
    model = Clase
    context_object_name = "clases_list"
    template_name = "clases_aula.html"
    ##Listamos las clases del profesor
    def get_queryset(self):
        #print "Buscamos el aula con el id",self.args[0]
        self.aula = get_object_or_404(Aula, id=self.args[0])
        return Clase.objects.filter(aula=self.aula)
        
    ## Anadimos el profesor al contexto
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(clases_aula, self).get_context_data(**kwargs)
        # Add in the publisher
        context['aula'] = self.aula
        return context

@method_decorator(permission_required('gestioneide.clase_add',raise_exception=True),name='dispatch')
class nueva_clase(CreateView):
    model = Clase
    template_name = "clase_form.html"
    form_class = ClaseForm
    success_url = "/clases"

@method_decorator(permission_required('gestioneide.clase_add',raise_exception=True),name='dispatch')
class nueva_clase_grupo(CreateView):
    model = Clase
    template_name = "clase_grupo_form.html"
    form_class = ClaseForm
    def get_success_url(self):
        return reverse_lazy("grupo_detalle", kwargs={'pk': self.object.grupo.pk})
    def get_context_data(self, **kwargs):
        context = super(nueva_clase_grupo, self).get_context_data(**kwargs)
        context['grupo_id'] = self.kwargs['grupo_id']
        return context
    def get_initial(self):
        grupo = Grupo.objects.get(id=self.kwargs['grupo_id'])
        return { 'grupo': grupo }

@method_decorator(permission_required('gestioneide.clase_delete',raise_exception=True),name='dispatch')
class borrar_clase(DeleteView):
    model = Clase
    template_name = "clase_confirm_delete.html"
    def get_success_url(self):
        return reverse_lazy("grupo_detalle", kwargs={'pk': self.object.grupo.pk})

@method_decorator(permission_required('gestioneide.clase_change',raise_exception=True),name='dispatch')    
class editar_clase(UpdateView):
    model = Clase
    template_name = "clase_editar.html"
    form_class = ClaseForm
    def get_success_url(self):
        return reverse_lazy("grupo_detalle", kwargs={'pk': self.object.grupo.pk})

@method_decorator(permission_required('gestioneide.clase_change',raise_exception=True),name='dispatch')    
class editar_clase_modal(editar_clase):
    template_name = "clase_editar_modal.html"
