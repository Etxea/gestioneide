# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, FormView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required
from django import forms
from django.contrib.sites.shortcuts import get_current_site

from models import Consulta, Confirmacion
from forms import *
from gestioneide.models import Asistencia,Year,Grupo,MailAlumno

class ConsultaListView(ListView):
    model = Consulta

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

class ConsultaDetailView(DetailView):
    model = Consulta

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

class ConsultaDeleteView(DeleteView):
    model = Consulta

    def get_success_url(self):
        return reverse("consulta_lista")

class ConsultaUpdateView(UpdateView):
    model = Consulta
    fields = '__all__'

    def get_form(self):
        form = super(ConsultaUpdateView, self).get_form()
        form.fields['texto'].widget = forms.Textarea()
        return form
    
    def get_success_url(self):
        return reverse("consulta_lista")

class ConfirmacionListView(ListView):
    model = Confirmacion
    template_name = ""
    def get_queryset(self):
        consulta = Consulta.objects.get(id=self.kwargs['consulta_id'])
        return Confirmacion.objects.filter(consulta=consulta)

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

class ConfirmacionSendView(FormView):
    form_class = ConfirmacionForm

class ConfirmacionGraciasView(TemplateView):
    template_name = 'confirmaciones/confirmacion_gracias.html'

class ConfirmacionResponseView(CreateView):
    model = Confirmacion
    fields = "__all__"