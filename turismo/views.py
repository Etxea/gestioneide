from django.views.generic import ListView, DetailView
from django.views.generic.edit import View,CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import reverse, reverse_lazy
from django.http import JsonResponse
from turismo.models import *
from gestioneide.models import Falta, Presencia, Justificada

import logging
logger = logging.getLogger('gestioneide.debug')
debug = logger.debug

@method_decorator(permission_required('gestioneide.turismo_view',raise_exception=True),name='dispatch')
class View(ListView):
    model = Curso
    template_name = "turismo/home.html"
    def get_queryset(self):
        year = Year().get_activo(self.request)
        return Curso.objects.filter(year=year).order_by('nombre')

@method_decorator(permission_required('gestioneide.turismo_view',raise_exception=True),name='dispatch')    
class CursoDeleteView(DeleteView):
    model = Curso
    template_name = "turismo/curso_delete.html"
    success_url = "/turismo"

@method_decorator(permission_required('gestioneide.turismo_view',raise_exception=True),name='dispatch')    
class CursoCreateView(CreateView):
    model = Curso
    fields = "__all__"
    template_name = "turismo/curso_nuevo.html"
    success_url = "/turismo"
    def get_initial(self):
        super(CursoCreateView, self).get_initial()
        year = Year().get_activo(self.request)
        self.initial = {"year":year}
        return self.initial

@method_decorator(permission_required('gestioneide.turismo_view',raise_exception=True),name='dispatch')    
class AsignaturaCreateView(CreateView):
    model = Asignatura
    fields = "__all__"
    template_name = "turismo/asignatura_nueva.html"
    success_url = "/turismo"

@method_decorator(permission_required('gestioneide.turismo_view',raise_exception=True),name='dispatch')    
class AsignaturaDetailView(DetailView):
    model = Asignatura
    context_object_name = 'asignatura'
    template_name = "turismo/asignatura_detalle.html"

@method_decorator(permission_required('gestioneide.turismo_view',raise_exception=True),name='dispatch')
class AsistenciaCreateView(CreateView):
    model = Asistencia
    fields = "__all__"
    template_name = "turismo/asistencia_nueva.html"

    def get_success_url(self):
        return reverse('turismo_asignatura_detalle', kwargs ={'pk': self.object.asignatura.id})

    def get_initial(self):
        super(AsistenciaCreateView, self).get_initial()
        asignatura = Asignatura.objects.get(pk=self.kwargs['asignatura_id'])
        self.initial = {"asignatura":asignatura.id}
        return self.initial

@method_decorator(permission_required('gestioneide.turismo_view',raise_exception=True),name='dispatch')    
class AsistenciaDetailView(DetailView):
    model = Asistencia
    template_name = "turismo/asistencia_detalle.html"

@method_decorator(permission_required('gestioneide.turismo_view',raise_exception=True),name='dispatch')
class ClaseCreateView(CreateView):
    model = Clase
    fields = "__all__"
    template_name = "turismo/clase_nueva.html"
    def get_success_url(self):
        return reverse_lazy('turismo_asignatura_detalle', args = (self.object.asignatura.id,))

@method_decorator(permission_required('gestioneide.turismo_view',raise_exception=True),name='dispatch')
class ClaseAsignaturaCreateView(ClaseCreateView):
    template_name = "turismo/clase_nueva_form.html"
    def get_success_url(self):
        return reverse_lazy('turismo_asignatura_detalle', args = (self.object.asignatura.id,))
    def get_initial(self):
        super(ClaseAsignaturaCreateView, self).get_initial()
        asignatura = Asignatura.objects.get(pk=self.kwargs['asignatura_id'])
        user = self.request.user
        self.initial = {"asignatura":asignatura.id,"profesor":asignatura.profesor}
        return self.initial

@method_decorator(permission_required('gestioneide.turismo_view',raise_exception=True),name='dispatch')
class ClaseUpdateView(UpdateView):
    model = Clase
    fields = "__all__"
    template_name = "turismo/clase_nueva_form.html"
    def get_success_url(self):
        return reverse_lazy('turismo_asignatura_detalle', args = (self.object.asignatura.id))

@method_decorator(permission_required('gestioneide.turismo_view',raise_exception=True),name='dispatch')
class ClaseDeleteView(DeleteView):
    model = Clase
    fields = "__all__"
    template_name = "turismo/clase_borrar.html"
    def get_success_url(self):
        return reverse_lazy('turismo_asignatura_detalle', args = (self.object.asignatura.id,))

class PasarListaView(ListView):
    model = Asignatura
    template_name = "turismo/pasarlista_lista.html"
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(PasarListaView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['meses'] = [9,10,11,12,1,2,3,4,5,6,7]
        return context
    def get_queryset(self):
        year = Year().get_activo(self.request)
        if self.request.user.is_staff:
            return Asignatura.objects.filter(curso__in=Curso.objects.filter(year=year))
        else:
            return Asignatura.objects.filter(curso__in=Curso.objects.filter(year=year)).filter(clases__in=AsignaturaClase.objects.filter(profesor=Profesor.objects.get(user_id=self.request.user.id)))

class PasarListaAsignaturaView(DetailView):
    model =Asignatura
    template_name = "turismo/pasarlista.html"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(PasarListaAsignaturaView, self).get_context_data(**kwargs)

        dias_clase = self.object.get_dias_clase_mes(int(self.kwargs['mes']))
        presentes = []
        presentes_id = []
        faltas = []
        faltas_id = []
        justificadas = []
        justificadas_id = []

        presentes_queryset = Presencia.objects.filter(mes=self.kwargs['mes'])
        for presente in presentes_queryset:
            presentes.append("%s_%s_%s" % (presente.asistencia.id, presente.mes, presente.dia))
            presentes_id.append(presente.id)

        faltas_queryset = Falta.objects.filter(mes=self.kwargs['mes'])
        for falta in faltas_queryset:
            faltas.append("%s_%s_%s" % (falta.asistencia.id, falta.mes, falta.dia))
            faltas_id.append(falta.id)

        justificadas_queryset = Justificada.objects.filter(mes=self.kwargs['mes'])
        for justificada in justificadas_queryset:
            justificadas.append("%s_%s_%s" % (justificada.asistencia.id, justificada.mes, justificada.dia))
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
            data = {
                'pk': self.object.pk,
            }
            return JsonResponse(data)
        else:
            return response

class FaltaCreateView(AjaxableResponseMixin, CreateView):
    model = Falta
    template_name = "turismo/falta_form.html"
    fields = '__all__'
    success_url = reverse_lazy('evaluacion')

class FaltaDeleteView(AjaxableResponseMixin, DeleteView):
    model = Falta
    success_url = reverse_lazy('evaluacion')

class JustificadaCreateView(AjaxableResponseMixin, CreateView):
    model = Justificada
    template_name = "turismo/Justificada_form.html"
    fields = '__all__'
    success_url = reverse_lazy('evaluacion')

class JustificadaDeleteView(AjaxableResponseMixin, DeleteView):
    model = Justificada
    success_url = reverse_lazy('evaluacion')

class PresenciaCreateView(AjaxableResponseMixin, CreateView):
    model = Presencia
    template_name = "turismo/presencia_form.html"
    fields = '__all__'
    success_url = reverse_lazy('evaluacion')

class PresenciaDeleteView(AjaxableResponseMixin, DeleteView):
    model = Presencia
    success_url = reverse_lazy('evaluacion')
