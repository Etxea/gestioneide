from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from gestioneide.models import *
from forms import *


class AlumnoListView(ListView):
    model=Alumno
    paginate_by = 50
    template_name = "alumnos/alumno_list.html"
    #Solo listamos los activos
    def get_queryset(self):
        return Alumno.objects.filter(activo=True)

class AlumnoBuscarView(ListView):
    model=Alumno
    paginate_by = 50
    template_name = "alumnos/alumno_list.html"
    #Solo listamos los activos
    def get_queryset(self):
        try:
            return Alumno.objects.filter(activo=True).filter(nombre__icontains=self.POST['busqueda'])
        except:
            return Alumno.objects.filter(activo=True)
        
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

