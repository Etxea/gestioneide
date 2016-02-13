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
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(AlumnoListView, self).dispatch(*args, **kwargs)
    #Solo listamos los activos
    def get_queryset(self):
        return Alumno.objects.filter(activo=True)

class AlumnoBuscarView(ListView):
    model=Alumno
    paginate_by = 50
    template_name = "alumnos/alumno_list.html"
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(AlumnoBuscarView, self).dispatch(*args, **kwargs)
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

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(AlumnoCreateView, self).dispatch(*args, **kwargs)
class AlumnoDetailView(DetailView):
    model = Alumno
    template_name = "alumnos/alumno_detail.html"
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(AlumnoDetailView, self).dispatch(*args, **kwargs)

class AlumnoDeleteView(DeleteView):
    model = Alumno
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(AlumnoDeleteView, self).dispatch(*args, **kwargs)
    def get_success_url(self):
        return reverse_lazy("alumnos_lista")

class AlumnoUpdateView(UpdateView):
    model = Alumno
    form_class = AlumnoCreateForm
    template_name = "alumnos/alumno_update_form.html"

    def get_success_url(self):
        return reverse_lazy("alumnos_lista")

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(AlumnoUpdateView, self).dispatch(*args, **kwargs)



