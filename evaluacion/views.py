from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from datetime import date
from wkhtmltopdf.views import PDFTemplateView

from gestioneide.models import *
from forms import *

class EvaluacionListView(ListView):
    template_name="evaluacion/evaluacion.html"
    model = Grupo
    #Solo listamos los que tengan asistencias
    def get_queryset(self):
        year = Year.objects.get(activo=True)
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
    print "Tenemos el grupo %s y tipo evaluacion %s"%(grupo,tipo_evaluacion)
    context = RequestContext(request,{'trimestre': trimestre})
    context['grupo']=grupo
    #~ context['grupo_siguiente']=grupo.get_next_by_nombre()
    #~ context['grupo_anterior']=grupo.get_previous_by_nombre()
    context['asistencias']=grupo.asistencia_set.all()
    #elegimos el tipo de formset y template

    NotaFomsetClass = NotaTrimestralFormSet
    template="evaluacion/notas_grupo_trimestre.html"
    if request.method == 'POST':
        notas_formset = NotaFomsetClass(request.POST, request.FILES)
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
            obj, created = NotaTrimestral.objects.get_or_create(trimestre=trimestre, asistencia=asistencia)
        notas_formset = NotaFomsetClass(queryset=NotaTrimestral.objects.filter(asistencia__in=lista_asistencias,trimestre=trimestre).order_by('asistencia__id'))
        #print notas_formset
        context['notas_formset']=notas_formset


    return render_to_response(template, context)

def NotasGrupoCuatrimestreView(request, pk, cuatrimestre):
    grupo = get_object_or_404(Grupo, pk=pk)
    tipo_evaluacion = grupo.curso.tipo_evaluacion
    print "Tenemos el grupo %s y tipo evaluacion %s" % (grupo, tipo_evaluacion)
    context = RequestContext(request, {'cuatrimestre': cuatrimestre})
    context['grupo'] = grupo
    # ~ context['grupo_siguiente']=grupo.get_next_by_nombre()
    # ~ context['grupo_anterior']=grupo.get_previous_by_nombre()
    context['asistencias'] = grupo.asistencia_set.all()
    # elegimos el tipo de formset y template
    if tipo_evaluacion == 2:
        print "Teneos una evaluacion de tipo elementary_intermediate"
        NotaFomsetClass = ElementayNotaFormSet
        template = "evaluacion/notas_grupo_elementary.html"

    elif tipo_evaluacion == 3:
        print "Tenemos una evaluacion de tipo elementary"
        NotaFomsetClass = ElementayNotaFormSet
        template = "evaluacion/notas_grupo_elementary.html"
    elif tipo_evaluacion == 4:
        print "Teneos una evaluacion de tipo upper"
        NotaFomsetClass = UpperNotaFormSet
        template = "evaluacion/notas_grupo_upper.html"

    if request.method == 'POST':
        notas_formset = NotaFomsetClass(request.POST, request.FILES)
        context['notas_formset'] = notas_formset
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
            print "Buscando la nota del cuatrimestre %s de la asistencia %s" % (cuatrimestre, asistencia.id)
            lista_asistencias.append(asistencia.id)
            obj, created = NotaCuatrimestral.objects.get_or_create(cuatrimestre=cuatrimestre, asistencia=asistencia)
        notas_formset = NotaFomsetClass(
            queryset=NotaCuatrimestral.objects.filter(asistencia__in=lista_asistencias, cuatrimestre=cuatrimestre).order_by(
                'asistencia__id'))
        # print notas_formset
        context['notas_formset'] = notas_formset

    return render_to_response(template, context)

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
    def get_template_names(self):
        grupo = self.get_object()
        tipo_evaluacion = grupo.curso.tipo_evaluacion
        print "Tenemos el grupo %s y tipo evaluacion %s"%(grupo,tipo_evaluacion)
        if tipo_evaluacion == 2:
            print "Teneos una evaluacion de tipo elementary_intermediate"
            return "evaluacion/notas_grupo_elementary.html"
        elif tipo_evaluacion == 3:
            print "Teneos una evaluacion de tipo upper"
            return "evaluacion/notas_grupo_upper.html"
        else:
            print "Teneos una evaluacion de tipo elementary_intermediate"
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
                print "Nueva nota creada"
            else:
                print "Nota vieja cargada"
                
        tipo_evaluacion = grupo.curso.tipo_evaluacion
        if tipo_evaluacion == 2:
            print "Teneos una evaluacion de tipo elementary_intermediate"
            notas_formset = ElementayNotaFormSet(queryset=Nota.objects.filter(trimestre=trimestre))
        elif tipo_evaluacion == 3:
            print "Teneos una evaluacion de tipo elementary_intermediate"
            notas_formset = UpperNotaFormSet(queryset=Nota.objects.filter(trimestre=trimestre))
        else:
            print "Teneos una evaluacion de tipo elementary_intermediate"
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
            print "Teneos una evaluacion de tipo elementary_intermediate"
            return ElementaryNotaCreateForm
        elif tipo_evaluacion == 2:
            print "Teneos una evaluacion de tipo upper"
            return UpperNotaCreateForm
        else:
            print "Tenemos una evaluacion de otro tipo"
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
        year = Year.objects.get(activo=True)
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
        year = Year.objects.get(activo=True)
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
        year = Year.objects.get(activo=True)
        if self.request.user.is_staff:
            return Grupo.objects.filter(year=year).annotate(Count('asistencia')).filter(asistencia__count__gt=0)
        else:
            return Grupo.objects.filter(year=year).filter(clases__in=Clase.objects.filter(profesor=Profesor.objects.get(user_id=self.request.user.id))).annotate(Count('asistencia')).filter(asistencia__count__gt=0)

class PasarListaGrupoView(DetailView):
    model = Grupo
    template_name="evaluacion/evaluacion_pasarlista.html"
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
            print "somo ajaxianos"
            data = {
                'pk': self.object.pk,
            }
            return JsonResponse(data)
        else:
            print "NO somo ajaxianos"
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
