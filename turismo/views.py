from django.views.generic import ListView, DetailView
from django.views.generic.edit import View,CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required
from django.core.urlresolvers import reverse, reverse_lazy
from gestioneide.models import *

import logging
logger = logging.getLogger('gestioneide.debug')
debug = logger.debug

# Create your views here.

@method_decorator(permission_required('gestioneide.turismo_view',raise_exception=True),name='dispatch')
class TurismoView(ListView):
    model = TurismoCurso
    template_name = "turismo/home.html"

@method_decorator(permission_required('gestioneide.turismo_view',raise_exception=True),name='dispatch')    
class TurismoAsignaturaCreateView(CreateView):
    model = TurismoAsignatura
    fields = "__all__"
    template_name = "turismo/asignatura_nueva.html"
    success_url = "/turismo"

@method_decorator(permission_required('gestioneide.turismo_view',raise_exception=True),name='dispatch')    
class TurismoAsignaturaDetailView(DetailView):
    model = TurismoAsignatura
    context_object_name = 'asignatura'
    template_name = "turismo/asignatura_detalle.html"

@method_decorator(permission_required('gestioneide.turismo_view',raise_exception=True),name='dispatch')
class TurismoAsistenciaCreateView(CreateView):
    model = TurismoAsistencia
    fields = "__all__"
    template_name = "turismo/asistencia_nueva.html"
    success_url = "/turismo"
    
@method_decorator(permission_required('gestioneide.turismo_view',raise_exception=True),name='dispatch')    
class TurismoAsistenciaDetailView(DetailView):
    model = TurismoAsistencia
    template_name = "turismo/asistencia_detalle.html"

@method_decorator(permission_required('gestioneide.turismo_view',raise_exception=True),name='dispatch')
class TurismoClaseCreateView(CreateView):
    model = TurismoClase
    fields = "__all__"
    template_name = "turismo/clase_nueva.html"
    def get_success_url(self):
        return reverse_lazy('turismo_asignatura_detalle', args = (self.object.asignatura.id,))

@method_decorator(permission_required('gestioneide.turismo_view',raise_exception=True),name='dispatch')
class TurismoClaseAsignaturaCreateView(TurismoClaseCreateView):
    template_name = "turismo/clase_nueva_form.html"
    def get_success_url(self):
        return reverse_lazy('turismo_asignatura_detalle', args = (self.object.asignatura.id,))
    def get_initial(self):
        super(TurismoClaseAsignaturaCreateView, self).get_initial()
        asignatura = TurismoAsignatura.objects.get(pk=self.kwargs['asignatura_id'])
        user = self.request.user
        self.initial = {"asignatura":asignatura.id}
        return self.initial

@method_decorator(permission_required('gestioneide.turismo_view',raise_exception=True),name='dispatch')
class TurismoClaseUpdateView(UpdateView):
    model = TurismoClase
    fields = "__all__"
    template_name = "turismo/clase_nueva_form.html"
    def get_success_url(self):
        return reverse_lazy('turismo_asignatura_detalle', args = (self.object.asignatura.id))

@method_decorator(permission_required('gestioneide.turismo_view',raise_exception=True),name='dispatch')
class TurismoClaseDeleteView(DeleteView):
    model = TurismoClase
    fields = "__all__"
    template_name = "turismo/clase_borrar.html"
    def get_success_url(self):
        return reverse_lazy('turismo_asignatura_detalle', args = (self.object.asignatura.id,))

