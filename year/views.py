from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from gestioneide.models import *

class YearListView(ListView):
    model=Year
    paginate_by = 50
    template_name = "year/year_list.html"
        
class YearCreateView(CreateView):
    template_name = "year/year_form.html"
    model = Year
    fields = "__all__"
    def get_success_url(self):
        return reverse_lazy("year_lista")

class YearUpdateView(UpdateView):
    template_name = "year/year_form.html"
    model = Year
    fields = "__all__"
    def get_success_url(self):
        return reverse_lazy("year_lista")


class YearDeleteView(DeleteView):
    template_name = "year/year_deleteconfirm.html"
    def get_success_url(self):
        return reverse_lazy("year_lista")


class YearDetailView(DetailView):
    model = Year
    template_name = "year/year_detail.html"

def year_activate(request):
    if request.method == 'POST':
        year_id = request.POST.get('id')
        year_actual = Year.objects.get(activo=True)
        year_nuevo = Year.objects.get(id=year_id)
        
        year_actual.activo=False
        year_actual.save()
        year_nuevo.activo=True
        year_nuevo.save()
        return JsonResponse({'state':'ok','msg': "activate done"})
    else:
        return HttpResponseRedirect(reverse('year_lista'))

def year_clone(request):
    if request.method == 'POST':
        year_id = request.POST.get('id')
        year_actual = Year.objects.get(activo=True)
        year_nuevo = Year.objects.get(id=year_id)
        print "clonamos ",year_actual," hacia ",year_nuevo
        print "Limpiamos"
        for grupo_nuevo in year_nuevo.grupo_set.all():
            for asistencia_nueva in grupo_nuevo.asistencia_set.all():
                asistencia_nueva.delete()
            grupo_nuevo.delete()
        print "Creamos grupos"    
        for grupo in year_actual.grupo_set.all():
            grupo_new = Grupo(year = year_nuevo,\
                nombre = grupo.nombre,\
                curso = grupo.curso,\
                precio = grupo.precio,\
                num_max = grupo.num_max,\
                menores = grupo.menores)
            grupo_new.save()
            for asistencia in grupo.asistencia_set.all():
                asistencia_new = Asistencia (year = year_nuevo,\
                    grupo = grupo_new,\
                    alumno = asistencia.alumno,\
                    confirmado = False,\
                    factura = asistencia.factura,\
                    precio = asistencia.precio,\
                    metalico = asistencia.metalico)
                asistencia_new.save()
        return JsonResponse({'state':'ok','msg': "clone done"})
    else:
        return HttpResponseRedirect(reverse('year_lista'))
    
def year_empty(request):
    if request.method == 'POST':
        year_id = request.POST.get('id')
        
        year_nuevo = Year.objects.get(id=year_id)
        print "Limpiamos"
        for grupo_nuevo in year_nuevo.grupo_set.all():
            for asistencia_nueva in grupo_nuevo.asistencia_set.all():
                asistencia_nueva.delete()
            grupo_nuevo.delete()
        return JsonResponse({'state':'ok','msg': "empty done"})
    else:
        return HttpResponseRedirect(reverse('year_lista'))
