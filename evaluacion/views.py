# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, FormView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import JsonResponse, HttpResponse

from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.template.loader import get_template

from datetime import date
from wkhtmltopdf.views import PDFTemplateView

from gestioneide.models import *
from evaluacion.forms import *

class EvaluacionListView(ListView):
    template_name="evaluacion/evaluacion.html"
    model = Grupo
    #Solo listamos los que tengan asistencias
    def get_queryset(self):
        year = Year().get_activo(self.request)
        if self.request.user.is_staff:
            return Grupo.objects.filter(year=year).annotate(Count('asistencia')).filter(asistencia__count__gt=0)
        else:
            return Grupo.objects.filter(year=year).filter(clases__in=Clase.objects.filter(profesor=Profesor.objects.get(user_id=self.request.user.id))).annotate(Count('asistencia')).filter(asistencia__count__gt=0)

    def get_context_data(self, **kwargs):
        context = super(EvaluacionListView, self).get_context_data(**kwargs)
        context['meses'] = [9,10,11,12,1,2,3,4,5,6,7]
        return context

def NotasGrupoTrimestreView(request,pk,trimestre):
    grupo = get_object_or_404(Grupo, pk=pk)
    tipo_evaluacion = grupo.curso.tipo_evaluacion
    #print "Tenemos el grupo %s y tipo evaluacion %s"%(grupo,tipo_evaluacion)
    contexto={}
    contexto['trimestre']=trimestre
    contexto['grupo']=grupo
    #~ context['grupo_siguiente']=grupo.get_next_by_nombre()
    #~ context['grupo_anterior']=grupo.get_previous_by_nombre()
    contexto['asistencias']=grupo.asistencia_set.all()
    #elegimos el tipo de formset y template en función de si es KIDs o no
    if tipo_evaluacion == 5:
        NotaFomsetClass = NotaTrimestralKidsFormSet
    else:
        NotaFomsetClass = NotaTrimestralFormSet
    template=get_template("evaluacion/notas_grupo_trimestre.html")
    if request.method == 'POST':
        notas_formset = NotaFomsetClass(request.POST, request.FILES)
        contexto['notas_formset']=notas_formset
        if notas_formset.is_valid():
            notas_formset.save()
            ##TODO: Volvemos a la lista de grupos, vamos al siguiente??
            pass
        else:
            #print "Formset mal"
            ##Volvemos renderizar con los errores
            contexto['notas_formset'] = notas_formset
    else:
        lista_asistencias = []
        for asistencia in grupo.asistencia_set.all().order_by('id'):
            #print "Buscando la nota del trimestre %s de la asistencia %s"%(trimestre,asistencia.id)
            lista_asistencias.append(asistencia.id)
            obj, created = NotaTrimestral.objects.get_or_create(trimestre=trimestre, asistencia=asistencia)
        notas_formset = NotaFomsetClass(queryset=NotaTrimestral.objects.filter(asistencia__in=lista_asistencias,trimestre=trimestre).order_by('asistencia__id'))
        contexto['notas_formset']=notas_formset
    return HttpResponse(template.render(contexto, request=request))

def NotasGrupoCuatrimestreView(request, pk, cuatrimestre):
    grupo = get_object_or_404(Grupo, pk=pk)
    tipo_evaluacion = grupo.curso.tipo_evaluacion
    template = get_template("evaluacion/notas_grupo_cuatrimestre.html")
    #print "Tenemos el grupo %s y tipo evaluacion %s" % (grupo, tipo_evaluacion)
    context={}
    context['cuatrimestre']= cuatrimestre
    context['grupo'] = grupo
    context['cuatrimestre'] = cuatrimestre
    # ~ context['grupo_siguiente']=grupo.get_next_by_nombre()
    # ~ context['grupo_anterior']=grupo.get_previous_by_nombre()
    context['asistencias'] = grupo.asistencia_set.all()
    # elegimos el tipo de formset y template
    if tipo_evaluacion == 2:
        #print "Tenemos una evaluacion de tipo elementary_intermediate"
        NotaFomsetClass = ElementayNotaFormSet
    elif tipo_evaluacion == 3:
        #print "Tenemos una evaluacion de tipo intermediate"
        NotaFomsetClass = IntermediateNotaFormSet
    elif tipo_evaluacion == 4:
        #print "Teneos una evaluacion de tipo upper"
        NotaFomsetClass = UpperNotaFormSet


    if request.method == 'POST':
        notas_formset = NotaFomsetClass(request.POST, request.FILES)
        context['notas_formset'] = notas_formset
        if notas_formset.is_valid():
            notas_formset.save()
            ## Volvemos a la lista
            return redirect(reverse_lazy('evaluacion'))
        else:
            #print "Formset mal"
            context['notas_formset'] = notas_formset
    else:
        lista_asistencias = []
        for asistencia in grupo.asistencia_set.all().order_by('id'):
            #print "Buscando la nota del cuatrimestre %s de la asistencia %s" % (cuatrimestre, asistencia.id)
            lista_asistencias.append(asistencia.id)
            obj, created = NotaCuatrimestral.objects.get_or_create(cuatrimestre=cuatrimestre, asistencia=asistencia)
        notas_formset = NotaFomsetClass(
            queryset=NotaCuatrimestral.objects.filter(asistencia__in=lista_asistencias, cuatrimestre=cuatrimestre).order_by(
                'asistencia__id'))
        # #print notas_formset
        context['notas_formset'] = notas_formset

    return HttpResponse(template.render(context, request=request))

def FaltasGrupoView(request,pk,mes):
    grupo = get_object_or_404(Grupo, pk=pk)
    context={}
    context['mes']=mes
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
                #print "Guardamos"
                faltas_formset.save()
            pass
        else:
            print("Formset mal")
    else:
        lista_asistencias = []
        for asistencia in grupo.asistencia_set.all().order_by('id'):
            #print "Buscando la nota del m %s sde la asistencia %s"%(mes,asistencia.id)
            lista_asistencias.append(asistencia.id)
            obj, created = Falta.objects.get_or_create(mes=mes, asistencia=asistencia)
        faltas_formset = FaltaFormSet(queryset=Falta.objects.filter(asistencia__in=lista_asistencias,mes=mes).order_by('asistencia__id'))
        ##print notas_formset
        context['faltas_formset']=faltas_formset
    return HttpResponse(get_template('evaluacion/faltas_grupo.html').render(context, request=request))

class NotasGrupo(DetailView):
    model = Grupo
    def get_template_names(self):
        grupo = self.get_object()
        tipo_evaluacion = grupo.curso.tipo_evaluacion
        #print "Tenemos el grupo %s y tipo evaluacion %s"%(grupo,tipo_evaluacion)
        if tipo_evaluacion == 2:
            #print "Teneos una evaluacion de tipo elementary_intermediate"
            return "evaluacion/notas_grupo_elementary.html"
        elif tipo_evaluacion == 3:
            #print "Teneos una evaluacion de tipo upper"
            return "evaluacion/notas_grupo_upper.html"
        else:
            #print "Teneos una evaluacion de tipo elementary_intermediate"
            return "evaluacion/notas_grupo.html"
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
                print("Nueva nota creada")
            else:
                print("Nota vieja cargada")
                
        tipo_evaluacion = grupo.curso.tipo_evaluacion
        if tipo_evaluacion == 2:
            #print "Teneos una evaluacion de tipo elementary_intermediate"
            notas_formset = ElementayNotaFormSet(queryset=Nota.objects.filter(trimestre=trimestre))
        elif tipo_evaluacion == 3:
            #print "Teneos una evaluacion de tipo elementary_intermediate"
            notas_formset = UpperNotaFormSet(queryset=Nota.objects.filter(trimestre=trimestre))
        else:
            #print "Teneos una evaluacion de tipo elementary_intermediate"
            notas_formset = NotaFormSet(queryset=Nota.objects.filter(trimestre=trimestre))

        for asistencia in grupo.asistencia_set.all():
            notas_form_array.append(NotaCreateForm(initial={'trimestre': trimestre, 'id_asistencia': asistencia.id}))
        context['notas_form_array'] = notas_form_array
        context['notas_formset'] = notas_formset
        return context

class NotaCreateView(CreateView):
    model = Nota
    template_name = "evaluacion/nota_form.html"
    form_class = NotaCreateForm

    def get_context_data(self, **kwargs):
        context = super(NotaCreateView, self).get_context_data(**kwargs)
        context['asistencia'] = Asistencia.objects.get(id=self.kwargs['asistencia'])
        context['trimestre'] = self.kwargs['trimestre']
        return context

    def get_initials(self):
        return {
            'trimestre': self.kwargs['trimestre'],
            'asistencia': self.kwargs['asistencia']
        }
    def get_form_class(self):
        asistencia = Asistencia.objects.get(id=self.kwargs['asistencia'])
        tipo_evaluacion = asistencia.grupo.curso.tipo_evaluacion
        if tipo_evaluacion == 2:
            #print "Teneos una evaluacion de tipo elementary_intermediate"
            return ElementaryNotaCreateForm
        elif tipo_evaluacion == 2:
            #print "Teneos una evaluacion de tipo upper"
            return UpperNotaCreateForm
        else:
            #print "Tenemos una evaluacion de otro tipo"
            return NotaCreateForm

class FaltasGrupo(DetailView):
    model = Grupo
    template_name = "evaluacion/faltas_grupo.html"
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(FaltasGrupo, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['trimestre'] = self.kwargs['trimestre']
        return context

class FaltasMesView(ListView):
    model = Asistencia
    template_name = "evaluacion/faltas_mes.html"
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(FaltasMesView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['mes'] = self.kwargs['mes']
        return context
    def get_queryset(self):
        year = Year().get_activo(self.request)
        #return Asistencia.objects.filter(year=year).filter(falta__mes=self.kwargs['mes']).annotate(faltas_mes=Count('falta')).\
        #    filter(justificada__mes=self.kwargs['mes']).annotate(justificadas_mes=Count('justificada')).order_by('-faltas_mes')
        #return Asistencia.objects.filter(year=year).filter(falta__mes=self.kwargs['mes']).filter(falta__year=year).annotate(faltas_mes=Count('falta')).order_by('-faltas_mes')
        lista = []
        mes = self.kwargs['mes']
        for asis in Asistencia.objects.filter(year=year):
            faltas = Falta.objects.filter(asistencia=asis,mes=mes).count()
            justificadas = Justificada.objects.filter(asistencia=asis,mes=mes).count()
            if faltas > 0 or justificadas > 0:
                lista.append({'asistencia':asis,'faltas_mes':faltas,'justificadas_mes':justificadas})
            else:
                pass
        return sorted(lista, key=lambda student: student['faltas_mes'], reverse=True)

@method_decorator(permission_required('gestioneide.informes_view',raise_exception=True),name='dispatch')
class FaltasMesCartas(PDFTemplateView):
    filename='cartas_faltas.pdf'
    template_name = "evaluacion/faltas_mes_cartas.html"
    cmd_options = {
        'margin-bottom': 20,
        'margin-top': 20,
        'margin-left': 25,
        'margin-right': 25
    }
    def get_context_data(self, **kwargs):
        context = super(FaltasMesCartas, self).get_context_data(**kwargs)
        year = Year().get_activo(self.request)
        context['mes'] = self.kwargs['mes']
        lista = []
        mes = self.kwargs['mes']
        for asis in Asistencia.objects.filter(year=year):
            if date.today().year - asis.alumno.fecha_nacimiento.year > 19:
                continue
            faltas = Falta.objects.filter(asistencia=asis,mes=mes).count()
            justificadas = Justificada.objects.filter(asistencia=asis,mes=mes).count()
            if faltas > 3:
                lista.append({'asistencia':asis,'faltas_mes':faltas,'justificadas_mes':justificadas})
            else:
                pass
        context['lista']=lista
        return context

class PasarListaView(ListView):
    model = Grupo
    template_name = "evaluacion/evaluacion_pasarlista_lista.html"
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(PasarListaView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['meses'] = [9,10,11,12,1,2,3,4,5,6,7]
        return context
    def get_queryset(self):
        year = Year().get_activo(self.request)
        if self.request.user.is_staff:
            return Grupo.objects.filter(year=year).annotate(Count('asistencia')).filter(asistencia__count__gt=0)
        else:
            return Grupo.objects.filter(year=year).filter(clases__in=Clase.objects.filter(profesor=Profesor.objects.get(user_id=self.request.user.id))).annotate(Count('asistencia')).filter(asistencia__count__gt=0)

class PasarListaGrupoView(DetailView):
    model = Grupo
    template_name = "evaluacion/evaluacion_pasarlista.html"
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(PasarListaGrupoView, self).get_context_data(**kwargs)
        
        dias_clase = self.object.get_dias_clase_mes(int(self.kwargs['mes']))
        presentes = []
        presentes_id = []
        faltas = []
        faltas_id = []
        justificadas = []
        justificadas_id = []
        
        presentes_queryset = Presencia.objects.filter(mes=self.kwargs['mes'])
        for presente in presentes_queryset:
            presentes.append("%s_%s_%s"%(presente.asistencia.id,presente.mes,presente.dia))
            presentes_id.append(presente.id)
        
        faltas_queryset = Falta.objects.filter(mes=self.kwargs['mes'])
        for falta in faltas_queryset:
            faltas.append("%s_%s_%s"%(falta.asistencia.id,falta.mes,falta.dia))
            faltas_id.append(falta.id)
        
        justificadas_queryset = Justificada.objects.filter(mes=self.kwargs['mes'])
        for justificada in justificadas_queryset:
            justificadas.append("%s_%s_%s"%(justificada.asistencia.id,justificada.mes,justificada.dia))
            justificadas_id.append(justificada.id)
        
        context['presentes'] = presentes
        context['faltas'] = faltas
        context['justificadas'] = justificadas
        
        context['presentes_id'] = presentes_id
        context['faltas_id'] = faltas_id
        context['justificadas_id'] = justificadas_id
        
        context['mes'] = self.kwargs['mes']
        context['dias_clase'] = dias_clase
        return context

class AjaxableResponseMixin(object):
    """
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """
    def form_invalid(self, form):
        response = super(AjaxableResponseMixin, self).form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        response = super(AjaxableResponseMixin, self).form_valid(form)
        if self.request.is_ajax():
            #print "somo ajaxianos"
            data = {
                'pk': self.object.pk,
            }
            return JsonResponse(data)
        else:
            #print "NO somo ajaxianos"
            return response

class FaltaCreateView(AjaxableResponseMixin, CreateView):
    model = Falta
    template_name = "evaluacion/falta_form.html"
    fields = '__all__'
    success_url = reverse_lazy('evaluacion')

class FaltaDeleteView(AjaxableResponseMixin, DeleteView):
    model = Falta
    success_url = reverse_lazy('evaluacion')

class JustificadaCreateView(AjaxableResponseMixin, CreateView):
    model = Justificada
    template_name = "evaluacion/Justificada_form.html"
    fields = '__all__'
    success_url = reverse_lazy('evaluacion')

class JustificadaDeleteView(AjaxableResponseMixin, DeleteView):
    model = Justificada
    success_url = reverse_lazy('evaluacion')

class PresenciaCreateView(AjaxableResponseMixin, CreateView):
    model = Presencia
    template_name = "evaluacion/presencia_form.html"
    fields = '__all__'
    success_url = reverse_lazy('evaluacion')

class PresenciaDeleteView(AjaxableResponseMixin, DeleteView):
    model = Presencia
    success_url = reverse_lazy('evaluacion')

class NotasParcialesGrupoCreateView(CreateView):
    model = GrupoNotasParciales
    template_name = 'evaluacion/notas_parciales_grupo_nueva.html'
    form_class = GrupoNotasParcialesCreateForm

    def get_success_url(self):
        return reverse_lazy('notas_parciales_grupo', kwargs={'pk': self.kwargs['grupo_id'] })

    def get_initial(self):
        initial = super(NotasParcialesGrupoCreateView, self).get_initial()
        initial['grupo'] = Grupo.objects.get(id=self.kwargs['grupo_id'])
        return initial

    def get_form_kwargs(self, **kwargs):
        form_kwargs = super(NotasParcialesGrupoCreateView, self).get_form_kwargs()
        form_kwargs['initial'] = {'grupo': Grupo.objects.get(id=self.kwargs['grupo_id'])}
        return form_kwargs

class NotasParcialesGrupoUpdateView(UpdateView):
    model = GrupoNotasParciales
    template_name = 'evaluacion/notas_parciales_grupo_nueva.html'
    form_class = GrupoNotasParcialesCreateForm

    def get_success_url(self):
        return reverse_lazy('notas_parciales_grupo', kwargs={'pk': self.object.grupo.pk })

class NotasParcialesGrupoDeleteView(DeleteView):
    model = GrupoNotasParciales
    template_name = 'evaluacion/notas_parciales_grupo_delete.html'

    def get_success_url(self):
        return reverse_lazy('notas_parciales_grupo', kwargs={'pk': self.object.grupo.pk })

class NotasParcialesGrupoView(DetailView):
    model = Grupo
    template_name = "evaluacion/notas_parciales_grupo.html"
    context_object_name = 'grupo'

    def get_context_data(self, **kwargs):
        context = super(NotasParcialesGrupoView, self).get_context_data(**kwargs)
        grupo = super(NotasParcialesGrupoView, self).get_object()
        context['grupo_notas_parciales_form'] = GrupoNotasParcialesCreateForm(initial={"grupo": grupo.pk})
        lista_asistencias = grupo.asistencia_set.all()
        notas_parciales_array = {}
        for grupo_notas_parciales in grupo.notas_parciales.all():
            notas_array = {}
            #Leemos o creamos cada nota parcial de este grupo de notas parciales
            for asistencia in lista_asistencias:
                nota_parcial, created = NotaParcial.objects.get_or_create(grupo_notas_parciales=grupo_notas_parciales, asistencia=asistencia)
                notas_array[nota_parcial.id] = nota_parcial.nota
            notas_parciales_array[grupo_notas_parciales.nombre]=notas_array
        context['grupo_notas_parciales'] = notas_parciales_array
        return context

class NotaParcialUpdateView(UpdateView):
    model = NotaParcial
    template_name = "evaluacion/notas_parciales_grupo_nota_update.html"
    form_class = NotaParcialCreateForm
    context_object_name = "nota"
    def get_success_url(self):
        grupo = NotaParcial.objects.get(id=self.kwargs['pk']).grupo_notas_parciales.grupo.pk
        return reverse_lazy('notas_parciales_grupo', kwargs={'pk': grupo })
