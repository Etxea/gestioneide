from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from gestioneide.models import *
from forms import *

class EvaluacionListView(ListView):
    template_name="evaluacion/evaluacion.html"
    model = Grupo
    def get_context_data(self, **kwargs):
        context = super(EvaluacionListView, self).get_context_data(**kwargs)
        context['meses'] = [9,10,11,12,1,2,3,4,5,6,7]
        return context

def NotasGrupoView(request,pk,trimestre):
    grupo = get_object_or_404(Grupo, pk=pk)
    context = RequestContext(request,{'trimestre': trimestre})
    context['grupo']=grupo
    #~ context['grupo_siguiente']=grupo.get_next_by_nombre()
    #~ context['grupo_anterior']=grupo.get_previous_by_nombre()
    context['asistencias']=grupo.asistencia_set.all()

    if request.method == 'POST':
        notas_formset = NotaFormSet(request.POST, request.FILES)
        context['notas_formset']=notas_formset
        if notas_formset.is_valid():
            # do something with the formset.cleaned_data
            if notas_formset.is_valid():
                print "Guardamos"
                notas_formset.save()
            pass
        else:
            print "Formset mal"
    else:
        lista_asistencias = []
        for asistencia in grupo.asistencia_set.all().order_by('id'):
            print "Buscando la nota del trimestre %s de la asistencia %s"%(trimestre,asistencia.id)
            lista_asistencias.append(asistencia.id)
            obj, created = Nota.objects.get_or_create(trimestre=trimestre, asistencia=asistencia)
        notas_formset = NotaFormSet(queryset=Nota.objects.filter(asistencia__in=lista_asistencias,trimestre=trimestre).order_by('asistencia__id'))
        #print notas_formset
        context['notas_formset']=notas_formset
    return render_to_response('evaluacion/notas_grupo.html', context)
        
def FaltasGrupoView(request,pk,mes):
    grupo = get_object_or_404(Grupo, pk=pk)
    context = RequestContext(request,{'mes': mes})
    context['grupo']=grupo
    context['mes']=mes
    #~ context['grupo_siguiente']=grupo.get_next_by_nombre()
    #~ context['grupo_anterior']=grupo.get_previous_by_nombre()
    context['asistencias']=grupo.asistencia_set.all()

    if request.method == 'POST':
        faltas_formset = FaltaFormSet(request.POST, request.FILES)
        context['faltas_formset']=faltas_formset
        if faltas_formset.is_valid():
            # do something with the formset.cleaned_data
            if faltas_formset.is_valid():
                print "Guardamos"
                faltas_formset.save()
            pass
        else:
            print "Formset mal"
    else:
        lista_asistencias = []
        for asistencia in grupo.asistencia_set.all().order_by('id'):
            print "Buscando la nota del m %s sde la asistencia %s"%(mes,asistencia.id)
            lista_asistencias.append(asistencia.id)
            obj, created = Falta.objects.get_or_create(mes=mes, asistencia=asistencia)
        faltas_formset = FaltaFormSet(queryset=Falta.objects.filter(asistencia__in=lista_asistencias,mes=mes).order_by('asistencia__id'))
        #print notas_formset
        context['faltas_formset']=faltas_formset
    return render_to_response('evaluacion/faltas_grupo.html', context)
    
    
class NotasGrupo(DetailView):
    model = Grupo
    template_name = "evaluacion/notas_grupo.html"
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(NotasGrupo, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        trimestre = self.kwargs['trimestre']
        context['trimestre'] = trimestre
        notas_form_array = []
        grupo = super(NotasGrupo, self).get_object()
        #Habria que usar un formset, crear o cargar todas las notas y entonces invocar el formset con todos los objectos
        # file:///usr/share/doc/python-django-doc/html/topics/forms/modelforms.html#model-formsets
        #AuthorFormSet()
        for asistencia in grupo.asistencia_set.all():
            obj, created = Nota.objects.get_or_create(trimestre=trimestre, asistencia=asistencia)
            if created:
                print "Nueva nota creada"
            else:
                print "Nota vieja cargada"
        notas_formset = NotaFormSet(queryset=Nota.objects.filter(trimestre=trimestre))
        for asistencia in grupo.asistencia_set.all():
            notas_form_array.append( NotaCreateForm(initial={'trimestre': trimestre,'id_asistencia': asistencia.id}))
        context['notas_form_array'] = notas_form_array
        context['notas_formset'] = notas_formset
        return context

class FaltasGrupo(DetailView):
    model = Grupo
    template_name = "evaluacion/faltas_grupo.html"
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(FaltasGrupo, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['trimestre'] = self.kwargs['trimestre']
        return context
    
    
class NotaCreateView(CreateView):
    model = Nota
    template_name = "evaluacion/nota_form.html"
    form_class = NotaCreateForm
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(NotaCreateView, self).dispatch(*args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super(NotaCreateView, self).get_context_data(**kwargs)
        context['asistencia'] = Asistencia.objects.get(id=self.kwargs['asistencia'])
        context['trimestre'] = self.kwargs['asistencia']
        return context


