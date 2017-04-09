from django.views.generic import ListView, DetailView
from django.views.generic.edit import View,CreateView, UpdateView, DeleteView
from django.views.generic.detail import SingleObjectMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.db.models import Q
from gestioneide.models import *
from forms import *


import logging
logger = logging.getLogger('gestioneide.debug')
debug = logger.debug

#Clase base de lista de alumnos

@method_decorator(permission_required('gestioneide.alumno_view',raise_exception=True),name='dispatch')
class AlumnoListView(ListView):
    model=Alumno
    paginate_by = 75
    template_name = "alumnos/alumno_list.html"
        
@method_decorator(permission_required('gestioneide.alumno_view',raise_exception=True),name='dispatch')
class AlumnoActivosListView(AlumnoListView):
    #Solo listamos los activos
    def get_queryset(self):
        return Alumno.objects.filter(activo=True)

@method_decorator(permission_required('gestioneide.alumno_view',raise_exception=True),name='dispatch')
class AlumnoGrupoListView(AlumnoListView):
    #Solo listamos los activos y que estan en un grupo
    def get_queryset(self):
        ano = Year().get_activo(self.request)
        lista = Asistencia.objects.filter(year=ano)
        return Alumno.objects.filter(asistencia__in=lista)

@method_decorator(permission_required('gestioneide.alumno_view',raise_exception=True),name='dispatch')
class AlumnoBuscarView(AlumnoListView):
    #Solo listamos los que coinciden conla busqueda
    def get_queryset(self):
        #~ cadena = self.kwargs['cadena']
        cadena = self.request.GET.get("cadena")
        try:
            numero = int(cadena)
            debug("tenemos el numero de alumno ",numero)
            return Alumno.objects.filter(id=numero)
        except:
            debug("No es un numero, buscamos los que el primer apellido coincida con", cadena)
            palabras = cadena.split(" ")
            if len(palabras)>1:
                filtro = (Q(apellido1__icontains=palabras[0]) & Q(apellido2__icontains=palabras[1])) | (Q(nombre__icontains=palabras[0]) & Q(apellido1__icontains=palabras[1]))
            else:
                filtro = Q(apellido1__icontains=cadena)
            return Alumno.objects.filter(activo=True).filter(filtro)

@method_decorator(permission_required('gestioneide.alumno_add',raise_exception=True),name='dispatch')        
class AlumnoCreateView(CreateView):
    form_class = AlumnoCreateForm
    template_name = "alumnos/alumno_form.html"
    def get_success_url(self):
        return reverse_lazy("alumnos_lista")

@method_decorator(permission_required('gestioneide.alumno_view',raise_exception=True),name='dispatch')
class AlumnoDetailView(DetailView):
    model = Alumno
    template_name = "alumnos/alumno_detail.html"

@method_decorator(permission_required('gestioneide.alumno_add',raise_exception=True),name='dispatch')
class AlumnoDeleteView(DeleteView):
    model = Alumno
    def get_success_url(self):
        return reverse_lazy("alumnos_lista")

@method_decorator(permission_required('gestioneide.alumno_add',raise_exception=True),name='dispatch')
class AlumnoUpdateView(UpdateView):
    model = Alumno
    form_class = AlumnoCreateForm
    template_name = "alumnos/alumno_update_form.html"

    def get_success_url(self):
        return reverse_lazy("alumnos_lista")

@method_decorator(permission_required('gestioneide.alumno_view',raise_exception=True),name='dispatch')
class AlumnoBajaView(View,SingleObjectMixin):
    model = Alumno
    def get(self, request, *args, **kwargs):
        return HttpResponse('Hello, World!')
    def post(self, request, *args, **kwargs):
        # Look up the author we're interested in.
        self.object = self.get_object()
        print "Vamos a dar de baja al alumno", self.object
        for asistencia in self.object.asistencia_set.all():
            print "Borrando asistencia",asistencia
            asistencia.delete()
        hist = Historia(alumno=self.object,tipo="baja",anotacion="")
        hist.save()
        self.object.activo = False
        self.object.save()
        return HttpResponseRedirect(reverse_lazy("alumnos_lista"))

@method_decorator(permission_required('gestioneide.alumno_add',raise_exception=True),name='dispatch')
class AlumnoAnotacionCreateView(CreateView):
    model = Anotacion
    template_name = "alumnos/anotacion_nueva.html"
    fields = ["texto"]
    def get_success_url(self):
        return reverse_lazy("alumno_detalle", kwargs={'pk': self.object.alumno.pk})
    def form_valid(self, form):
        form.instance.creador = self.request.user
        alumno = Alumno.objects.get(pk=self.kwargs['alumno_id'])
        form.instance.alumno = alumno
        return super(AlumnoAnotacionCreateView, self).form_valid(form)
    #~ def get_initial(self):
        #~ super(AlumnoAnotacionCreateView, self).get_initial()
        #~ alumno = Alumno.objects.get(pk=self.kwargs['alumno_id'])
        #~ self.initial = {"alumno":alumno.id}
        #~ return self.initial

class AlumnoAnotacionDeleteView(DeleteView):
    model = Anotacion
    template_name = "alumnos/anotacion_borrar.html"
    def get_success_url(self):
        return reverse_lazy("alumno_detalle",kwargs={'pk': self.object.alumno.pk})

@method_decorator(permission_required('gestioneide.alumno_add',raise_exception=True),name='dispatch')
class AlumnoPruebaNivelCreateView(CreateView):
    model = PruebaNivel
    template_name = "alumnos/pruebanivel_nueva.html"
    fields = ["resultado","nivel_recomendado","observaciones"]
    def get_success_url(self):
        return reverse_lazy("alumno_detalle", kwargs={'pk': self.object.alumno.pk})
    def form_valid(self, form):
        form.instance.creador = self.request.user
        alumno = Alumno.objects.get(pk=self.kwargs['alumno_id'])
        form.instance.alumno = alumno
        return super(AlumnoPruebaNivelCreateView, self).form_valid(form)

@method_decorator(permission_required('gestioneide.alumno_add',raise_exception=True),name='dispatch')
class AlumnoPruebaNivelDeleteView(DeleteView):
    model = PruebaNivel
    template_name = "alumnos/confirmar_borrar.html"
    def get_success_url(self):
        return reverse_lazy("alumno_detalle",kwargs={'pk': self.object.alumno.pk})

@method_decorator(permission_required('gestioneide.alumno_add',raise_exception=True),name='dispatch')
class AlumnoResultadoCambridgeCreateView(CreateView):
    model = ResultadoCambridge
    template_name = "alumnos/resultadocambridge_nuevo.html"
    fields = ["ano","nivel","resultado","observaciones"]
    def get_success_url(self):
        return reverse_lazy("alumno_detalle", kwargs={'pk': self.object.alumno.pk})
    def form_valid(self, form):
        form.instance.creador = self.request.user
        alumno = Alumno.objects.get(pk=self.kwargs['alumno_id'])
        form.instance.alumno = alumno
        return super(AlumnoResultadoCambridgeCreateView, self).form_valid(form)

@method_decorator(permission_required('gestioneide.alumno_add',raise_exception=True),name='dispatch')
class AlumnoResultadoCambridgeDeleteView(DeleteView):
    model = ResultadoCambridge
    template_name = "alumnos/confirmar_borrar.html"
    def get_success_url(self):
        return reverse_lazy("alumno_detalle",kwargs={'pk': self.object.alumno.pk})
