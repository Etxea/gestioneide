from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from gestioneide.models import *
from forms import *


import logging
logger = logging.getLogger('gestioneide.debug')
debug = logger.debug

#Clase vase de lista de alumnos
class AlumnoListView(ListView):
    model=Alumno
    paginate_by = 75
    template_name = "alumnos/alumno_list.html"
        
class AlumnoActivosListView(AlumnoListView):
    #Solo listamos los activos
    def get_queryset(self):
        return Alumno.objects.filter(activo=True)

class AlumnoGrupoListView(AlumnoListView):
    #Solo listamos los activos y que estan en un grupo
    def get_queryset(self):
        return Alumno.objects.filter(activo=True).annotate(Count('asistencia')).filter(asistencia__count__gt=0)

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
            debug("No es un numero, buscamos los que coincidan con", cadena)
            filtro = Q(nombre__icontains=cadena) | Q(apellido1__icontains=cadena) | Q(apellido2__icontains=cadena)
            return Alumno.objects.filter(activo=True).filter(filtro)
        
        
class AlumnoCreateView(CreateView):
    form_class = AlumnoCreateForm
    template_name = "alumnos/alumno_form.html"
    def get_success_url(self):
        return reverse_lazy("alumnos_lista")

class AlumnoDetailView(DetailView):
    model = Alumno
    template_name = "alumnos/alumno_detail.html"

class AlumnoDeleteView(DeleteView):
    model = Alumno
    def get_success_url(self):
        return reverse_lazy("alumnos_lista")

class AlumnoUpdateView(UpdateView):
    model = Alumno
    form_class = AlumnoCreateForm
    template_name = "alumnos/alumno_update_form.html"

    def get_success_url(self):
        return reverse_lazy("alumnos_lista")

