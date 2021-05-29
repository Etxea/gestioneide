# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic import ListView, DetailView, FormView, TemplateView, View
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required
from django import forms
from django.contrib.sites.shortcuts import get_current_site

from excel_response import ExcelView

from models import Consulta, Confirmacion
from forms import *
from gestioneide.models import Asistencia,Year,Grupo,MailAlumno

@method_decorator(permission_required('gestioneide.alumno_add',raise_exception=True),name='dispatch')
class ConsultaListView(ListView):
    model = Consulta

@method_decorator(permission_required('gestioneide.alumno_add',raise_exception=True),name='dispatch')
class ConsultaCreateView(CreateView):
    model = Consulta
    fields = '__all__'

    def get_form(self):
        form = super(ConsultaCreateView, self).get_form()
        form.fields['texto'].widget = forms.Textarea()
        year = Year.objects.get(activo=True)
        form.fields['grupo'].queryset = Grupo.objects.filter(year=year)
        return form

    def get_success_url(self):
        return reverse("consulta_lista")

@method_decorator(permission_required('gestioneide.alumno_add',raise_exception=True),name='dispatch')
class ConsultaDetailView(DetailView):
    model = Consulta

@method_decorator(permission_required('gestioneide.alumno_add',raise_exception=True),name='dispatch')
class ConsultaEnviarView(DetailView):
    model = Consulta    
    template_name = 'confirmaciones/consulta_enviar.html'

    def post(self, request, *args, **kwargs):
        consulta = Consulta.objects.get(id=self.kwargs['pk'])
        for asistencia in consulta.grupo.asistencia_set.all(): 
            print("Enviando a alumno: %s"%asistencia.alumno.id)
            confirmacion_url = "https://%s%s"%(get_current_site(self.request),reverse('confirmacion_nuevo', kwargs={'consulta_id': consulta.id, 'asistencia_id': asistencia.id}))
            mensaje = "%s\nPuedes contestar en la siguiente url: %s"%(consulta.texto,confirmacion_url)
            #print mensaje
            alumno = asistencia.alumno
            mail = MailAlumno()
            mail.alumno = alumno
            mail.creador = self.request.user
            mail.titulo = consulta.nombre
            #Cortamos el mensaje
            resumen_mensaje = "Confirmacion %s"%consulta.nombre
            mail.mensaje = resumen_mensaje
            mail.enviado = alumno.enviar_mail(consulta.nombre,mensaje)
            mail.save()
            
        return HttpResponseRedirect(reverse("consulta_lista"))

@method_decorator(permission_required('gestioneide.alumno_add',raise_exception=True),name='dispatch')
class ConsultaDeleteView(DeleteView):
    model = Consulta

    def get_success_url(self):
        return reverse("consulta_lista")

@method_decorator(permission_required('gestioneide.alumno_add',raise_exception=True),name='dispatch')
class ConsultaUpdateView(UpdateView):
    model = Consulta
    fields = '__all__'

    def get_form(self):
        form = super(ConsultaUpdateView, self).get_form()
        form.fields['texto'].widget = forms.Textarea()
        return form
    
    def get_success_url(self):
        return reverse("consulta_lista")

class RespuestaCreateView(CreateView):
    model = Confirmacion
    fields = '__all__'

    def get_form(self):
        form = super(ConfirmacionCreateView, self).get_form()
        form.fields['consulta'].widget = forms.HiddenInput()
        form.fields['asistencia'].widget = forms.HiddenInput()
        return form

    def get_context_data(self, **kwargs):
        context = super(ConfirmacionCreateView, self).get_context_data(**kwargs)
        context['consulta'] = Consulta.objects.get(id=self.kwargs['consulta_id'])
        context['asistencia'] = Asistencia.objects.get(id=self.kwargs['asistencia_id'])
        return context
    
    def get_initial(self, *args, **kwargs):
        initial = super(ConfirmacionCreateView, self).get_initial(**kwargs)
        consulta = Consulta.objects.get(id=self.kwargs['consulta_id'])
        initial['consulta'] = consulta
        asistencia = Asistencia.objects.get(id=self.kwargs['asistencia_id'])
        initial['asistencia'] = asistencia
        return initial
    def get_success_url(self):
        return reverse('confirmacion_gracias')

@method_decorator(permission_required('gestioneide.alumno_add',raise_exception=True),name='dispatch')
class ConfirmacionListView(ListView):
    model = Confirmacion
    template_name = "consultas/confirmacion_lista.html"
   
    def get_queryset(self):
        year=Year()
        asistencias_ano = Asistencia.objects.filter(year=year.get_activo(self.request))
        return Confirmacion.objects.filter(asistencia__in=asistencias_ano).exclude(respuesta_choice=0).exclude(respuesta_choice=1).exclude(gestionada=True)

@method_decorator(permission_required('gestioneide.alumno_add',raise_exception=True),name='dispatch')
class ConfirmacionPendientesListView(ListView):
    template_name = "consultas/confirmacion_lista.html"
    def get_queryset(self):
        year=Year()
        asistencias_ano = Asistencia.objects.filter(year=year.get_activo(self.request))
        return Confirmacion.objects.filter(asistencia__in=asistencias_ano).filter(respuesta_choice=0).exclude(gestionada=True)

@method_decorator(permission_required('gestioneide.alumno_add',raise_exception=True),name='dispatch')    
class ConfirmacionPendientesExcelView(ExcelView):
    model = Confirmacion
    def get_queryset(self):
        year=Year()
        asistencias_ano = Asistencia.objects.filter(year=year.get_activo(self.request))
        return Confirmacion.objects.filter(asistencia__in=asistencias_ano).filter(respuesta_choice=0).exclude(gestionada=True)

@method_decorator(permission_required('gestioneide.alumno_add',raise_exception=True),name='dispatch')
class ConfirmacionUpdateView(UpdateView):
    model = Confirmacion
    fields = "__all__"
    #success_url = reverse('confirmacion_lista')
    def get_success_url(self):
        return reverse('confirmacion_lista')

class ConfirmacionSendView(FormView):
    form_class = ConfirmacionForm

class ConfirmacionGraciasView(TemplateView):
    template_name = 'consultas/confirmacion_gracias.html'

class ConfirmacionResponseView(CreateView):
    model = Confirmacion
    fields = "__all__"

@method_decorator(permission_required('gestioneide.alumno_add',raise_exception=True),name='dispatch')
class ConfirmacionesCrearView(ListView):
    template_name = "consultas/confirmaciones_crear.html"
    model = Confirmacion
    
    def post(self, request, *args, **kwargs):
        print "Somos post vamos a generar las confirmaciones pendiente"
        year = Year().get_activo(self.request)
        for asistencia in Asistencia.objects.filter(year=year):
            if asistencia.confirmacion_set.all().count() == 0:
                print "No tiene confirmacion"
                confirmacion = Confirmacion(asistencia=asistencia)
                confirmacion.save()
                confirmacion.send_mail()
            else:
                confirmacion = asistencia.confirmacion_set.all()[0]
                if confirmacion.respuesta_choice == 0:
                    print asistencia,"Ya tiene confirmacion, pero no ha contestado, la enviamos"
                    confirmacion.send_mail()
                else:
                    print "Ya ha contestado"
        return HttpResponseRedirect(reverse('confirmaciones_crear'))
    
    def get_queryset(self):
        year = Year().get_activo(self.request)
        return Confirmacion.objects.filter(asistencia__in=Asistencia.objects.filter(year=year))    
    
    def get_context_data(self, **kwargs):
        context = super(ConfirmacionesCrearView, self).get_context_data(**kwargs)
        year = Year().get_activo(self.request)
        context['year'] = year
        context['confirmaciones_contestadas'] = Confirmacion.objects.filter(asistencia__in=Asistencia.objects.filter(year=year)).exclude(respuesta_choice=0)
        return context

class ConfirmacionContestarView(UpdateView):
    model = Confirmacion
    fields = ['respuesta_choice','respuesta_texto']
    success_url = reverse_lazy('confirmacion_gracias')
