from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from gestioneide.models import *

@method_decorator(permission_required('gestioneide.asistencia_view',raise_exception=True),name='dispatch')
class AsistenciaListView(ListView):
    model=Asistencia
    paginate_by = 50
    template_name = "asistencias/asistencia_list.html"
    def get_queryset(self):
        year = Year().get_activo(self.request)
        return Asistencia.objects.filter(year=year)

@method_decorator(permission_required('gestioneide.asistencia_add',raise_exception=True),name='dispatch')        
class AsistenciaCreateView(CreateView):
    template_name = "asistencias/asistencia_form.html"
    model = Asistencia
    #~ fields = ["grupo","alumno","confirmado","factura","metalico","precio"]
    fields = "__all__"
    def get_success_url(self):
        return reverse_lazy("asistencia_lista")
    def get_initial(self):
        year = Year().get_activo(self.request)
        print "Establecemos el ano en ",year
        return { 'year': year }

@method_decorator(permission_required('gestioneide.asistencia_add',raise_exception=True),name='dispatch')        
class AsistenciaAlumnoCreateView(CreateView):
    template_name = "asistencias/asistencia_form.html"
    model = Asistencia
    #~ fields = ["grupo","confirmado","factura","metalico","precio"]
    fields = "__all__"
    def get_success_url(self):
        return reverse_lazy("alumno_detalle",kwargs = {'pk' : self.object })
    def get_initial(self):
        year = Year().get_activo(self.request)
        alumno = Alumno.objects.get(id=self.kwargs['alumno_id'])
        print "Establecemos el ano en ",year,"y el alumno en",alumno
        return { 'year': year , 'alumno': alumno }        

@method_decorator(permission_required('gestioneide.asistencia_add',raise_exception=True),name='dispatch')
class AsistenciaGrupoCreateView(CreateView):
    template_name = "asistencias/asistencia_form.html"
    model = Asistencia
    fields = ["alumno","confirmado","factura","metalico","precio"]
    #fields = "__all__"
    def get_success_url(self):
        return reverse_lazy("grupo_detalle",kwargs = {'pk' : self.object.grupo.id })
    def get_initial(self):
        year = Year().get_activo(self.request)
        grupo = Grupo.objects.get(id=self.kwargs['grupo_id'])
        print "Establecemos el ano en ",year, "y el grupo",grupo
        return { 'year': year , 'grupo': grupo }        

@method_decorator(permission_required('gestioneide.asistencia_change',raise_exception=True),name='dispatch')
class AsistenciaUpdateView(UpdateView):
    template_name = "asistencias/asistencia_form.html"
    model = Asistencia
    fields = "__all__"
    def get_success_url(self):
        
        return reverse_lazy("alumno_detalle",args=[self.object.alumno.id])

@method_decorator(permission_required('gestioneide.asistencia_delete',raise_exception=True),name='dispatch')
class AsistenciaDeleteView(DeleteView):
    template_name = "asistencias/asistencia_deleteconfirm.html"
    model = Asistencia
    ##FIXME esto deberia ser dinamico
    def get_success_url(self):
        return reverse_lazy("grupo_detalle",kwargs = {'pk' : self.object.grupo.id })

@method_decorator(permission_required('gestioneide.asistencia_view',raise_exception=True),name='dispatch')
class AsistenciaDetailView(DetailView):
    model = Asistencia
    template_name = "asistencias/asistencia_detail.html"

@permission_required('gestioneide.year_add',raise_exception=True)
def asistencia_domiciliacion(request):
    if request.method == 'POST':
        asistencia_id = request.POST.get('id')
        asistencia = Asistencia.objects.get(id=asistencia_id)
        
        asistencia.metalico=False
        asistencia.save()
        
        return JsonResponse({'state':'ok','msg': "done"})
    else:
        return HttpResponseRedirect(reverse('asistencia_lista'))
