from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from gestioneide.models import *

class AsistenciaListView(ListView):
    model=Asistencia
    paginate_by = 50
    template_name = "asistencias/asistencia_list.html"
    def get_queryset(self):
        year = Year.objects.get(activo=True)
        return Asistencia.objects.filter(year=year)

        
class AsistenciaCreateView(CreateView):
    template_name = "asistencias/asistencia_form.html"
    model = Asistencia
    #~ fields = ["grupo","alumno","confirmado","factura","metalico","precio"]
    fields = "__all__"
    def get_success_url(self):
        return reverse_lazy("asistencia_lista")
    def get_initial(self):
        year = Year.objects.get(activo=True)
        print "Establecemos el ano en ",year
        return { 'year': year }
        
class AsistenciaAlumnoCreateView(CreateView):
    template_name = "asistencias/asistencia_form.html"
    model = Asistencia
    #~ fields = ["grupo","confirmado","factura","metalico","precio"]
    fields = "__all__"
    def get_success_url(self):
        return reverse_lazy("alumno_detalle",kwargs = {'pk' : self.object })
    def get_initial(self):
        year = Year.objects.get(activo=True)
        alumno = Alumno.objects.get(id=self.kwargs['alumno_id'])
        print "Establecemos el ano en ",year,"y el alumno en",alumno
        return { 'year': year , 'alumno': alumno }        

class AsistenciaGrupoCreateView(CreateView):
    template_name = "asistencias/asistencia_form.html"
    model = Asistencia
    #~ fields = ["alumno","confirmado","factura","metalico","precio"]
    fields = "__all__"
    def get_success_url(self):
        return reverse_lazy("grupo_detalle",kwargs = {'pk' : self.object })
    def get_initial(self):
        year = Year.objects.get(activo=True)
        grupo = Grupo.objects.get(id=self.kwargs['alumno_id'])
        print "Establecemos el ano en ",year, "y el grupo",grupo
        return { 'year': year , 'grupo': grupo }        

class AsistenciaUpdateView(UpdateView):
    template_name = "asistencias/asistencia_form.html"
    model = Asistencia
    fields = "__all__"
    def get_success_url(self):
        return reverse_lazy("asistencia_lista")


class AsistenciaDeleteView(DeleteView):
    template_name = "asistencias/asistencia_deleteconfirm.html"
    model = Asistencia
    ##FIXME esto deberia ser dinamico
    def get_success_url(self):
        return reverse_lazy("asistencia_lista")


class AsistenciaDetailView(DetailView):
    model = Asistencia
    template_name = "asistencias/asistencia_detail.html"