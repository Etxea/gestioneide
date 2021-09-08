# -*- coding: utf-8 -*-

from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required

import logging
log = logging.getLogger("django")

from gestioneide.models import *

@method_decorator(permission_required('gestioneide.year_add',raise_exception=True),name='dispatch')
class YearListView(ListView):
    model=Year
    paginate_by = 50
    template_name = "year/year_list.html"

@method_decorator(permission_required('gestioneide.year_add',raise_exception=True),name='dispatch')        
class YearCreateView(CreateView):
    template_name = "year/year_form.html"
    model = Year
    fields = "__all__"
    def get_success_url(self):
        return reverse_lazy("year_lista")

@method_decorator(permission_required('gestioneide.year_add',raise_exception=True),name='dispatch')
class YearUpdateView(UpdateView):
    template_name = "year/year_form.html"
    model = Year
    fields = "__all__"
    def get_success_url(self):
        return reverse_lazy("year_lista")

@method_decorator(permission_required('gestioneide.year_add',raise_exception=True),name='dispatch')
class YearDeleteView(DeleteView):
    template_name = "year/year_deleteconfirm.html"
    def get_success_url(self):
        return reverse_lazy("year_lista")

@method_decorator(permission_required('gestioneide.year_add',raise_exception=True),name='dispatch')
class YearDetailView(DetailView):
    model = Year
    template_name = "year/year_detail.html"

@permission_required('gestioneide.year_add',raise_exception=True)
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

@permission_required('gestioneide.year_add',raise_exception=True)
def year_clone(request):
    if request.method == 'POST':
        year_id = request.POST.get('id')
        year_actual = Year.objects.get(activo=True)
        year_nuevo = Year.objects.get(id=year_id)
        log.debug("Vamos a copiar el ano activo %s al ano elegido %s"%(year_actual,year_nuevo))
        print("Vamos a copiar el ano activo %s al ano elegido %s"%(year_actual,year_nuevo))
        log.debug("Primero limpiamos")
        for grupo_nuevo in year_nuevo.grupo_set.all():
            for asistencia_nueva in grupo_nuevo.asistencia_set.all():
                asistencia_nueva.delete()
            grupo_nuevo.delete()
        for grupo in year_actual.grupo_set.all():
            log.debug("Copiando grupo %s"%grupo)
            print("Copiando grupo %s"%grupo)
            grupo_new = Grupo(\
                year = year_nuevo,\
                nombre = grupo.nombre,\
                curso = grupo.curso,\
                #precio = grupo.precio,\
                num_max = grupo.num_max,\
                menores = grupo.menores)
            grupo_new.save()
            print("Creado nuevo grupo %s"%grupo_new)
            log.debug("Copiando Asistencias")
            print("Copiando Asistencias")
            for asistencia in grupo.asistencia_set.all():
                log.debug("Copiando asistencia %s"%asistencia)
                print("Copiando asistencia %s"%asistencia)
                asistencia_new = Asistencia (
                    year = year_nuevo,\
                    grupo = grupo_new,\
                    alumno = asistencia.alumno,\
                    confirmado = False,\
                    factura = asistencia.factura,\
                    precio = asistencia.precio,\
                    metalico = asistencia.metalico)
                asistencia_new.save()
                print("Creada asistencia nueva %s"%asistencia_new)
        return JsonResponse({'state':'ok','msg': "clone done"})
    else:
        return HttpResponseRedirect(reverse('year_lista'))

@permission_required('gestioneide.year_add',raise_exception=True)    
def year_empty(request):
    if request.method == 'POST':
        year_id = request.POST.get('id')
        year_nuevo = Year.objects.get(id=year_id)
        for grupo_nuevo in year_nuevo.grupo_set.all():
            for asistencia_nueva in grupo_nuevo.asistencia_set.all():
                asistencia_nueva.delete()
            grupo_nuevo.delete()
        return JsonResponse({'state':'ok','msg': "empty done"})
    else:
        return HttpResponseRedirect(reverse('year_lista'))


