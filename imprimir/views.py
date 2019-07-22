from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic import ListView,TemplateView

import datetime
import os
import calendar

from django.conf import settings

from wkhtmltopdf.views import PDFTemplateView

from gestioneide.models import *

@method_decorator(permission_required('gestioneide.informes_view',raise_exception=True),name='dispatch')
class ImprimirGrupos(PDFTemplateView):
    filename='grupos.pdf'
    template_name = "grupos_pdf.html"    
    def get_context_data(self, **kwargs):
        context = super(ImprimirGrupos, self).get_context_data(**kwargs)
        year = Year().get_activo(self.request)
        context['year'] = year.__unicode__()
        context['grupo_list'] = Grupo.objects.filter(year=year).annotate(Count('asistencia')).filter(asistencia__count__gt=0)
        return context

@method_decorator(permission_required('gestioneide.informes_view',raise_exception=True),name='dispatch')
class ImprimirGruposAlumnos(PDFTemplateView):
    filename='listado_grupos_con_alumnos.pdf'
    template_name = "grupos_alumnos_pdf.html"
    def get_context_data(self, **kwargs):
        context = super(ImprimirGruposAlumnos, self).get_context_data(**kwargs)
        year = Year().get_activo(self.request)
        context['year'] = year.__unicode__()
        if 'grupo_id' in kwargs:
            context['grupo_list'] = Grupo.objects.filter(id=kwargs['grupo_id'])
        else:
            #context['grupo_list'] = Grupo.objects.filter(year=year).annotate(Count('asistencia')).filter(asistencia__count__gt=0)
            #Sacamos todos los grupos por incidencia #49
            context['grupo_list'] = Grupo.objects.filter(year=year)
        return context

@method_decorator(permission_required('gestioneide.informes_view',raise_exception=True),name='dispatch')
class ImprimirAsistenciaHorario(PDFTemplateView):
    template_name='asistencia_horario_pdf.html'
    cmd_options = {
        'margin-bottom': 10,
        'margin-top': 10,
        'margin-left': 15,
        'margin-right': 15
    }
    def get_context_data(self, **kwargs):
        context = super(ImprimirAsistenciaHorario, self).get_context_data(**kwargs)
        asistencia_id=kwargs['asistencia_id']
        asistencia = Asistencia.objects.get(id=asistencia_id)
        if not asistencia.confirmado:
            asistencia.confirmado = True
            asistencia.save()
    
        context['asistencia'] = asistencia
        year = Year().get_activo(self.request)
        context['lista_festivos'] =Festivo.objects.filter(year=year)
        return context

@method_decorator(permission_required('gestioneide.informes_view',raise_exception=True),name='dispatch')
class ImprimirAlumnoMatricula(PDFTemplateView):
    filename='matricula.pdf'
    template_name = 'matricula_alumno_pdf.html'
    cmd_options = {
        'margin-bottom': 10,
        'margin-top': 10,
        'margin-left': 15,
        'margin-right': 15
    }
    def get_context_data(self, **kwargs):
        context = super(ImprimirAlumnoMatricula, self).get_context_data(**kwargs)
        alumno_id= kwargs['alumno_id']
        alumno = Alumno.objects.get(id=alumno_id)
        context['alumno'] = alumno
        return context

@method_decorator(permission_required('gestioneide.informes_view',raise_exception=True),name='dispatch')    
class ImprimirAlumnoOctavilla(PDFTemplateView):
    filename='octavilla_alumno_pdf.pdf'
    template_name = 'octavilla_alumno_pdf.html'
    cmd_options = {"page-size": "A5","orientation": "landscape"}
    def get_context_data(self, **kwargs):
        context = super(ImprimirAlumnoOctavilla, self).get_context_data(**kwargs)
        alumno_id= kwargs['alumno_id']
        alumno = Alumno.objects.get(id=alumno_id)
        context['alumno'] = alumno
        return context

@method_decorator(permission_required('gestioneide.informes_view',raise_exception=True),name='dispatch')
class ImprimirGruposPlanillaAsistencia(PDFTemplateView):
    filename='grupos_planilla_asistencia.pdf'
    template_name = 'grupos_planilla_asistencia_pdf.html'
    cmd_options = {
#        "orientation": "landscape",
        'margin-bottom': 15,
        'margin-top': 15,
        'margin-left': 25,
        'margin-right': 25
        }
    def get_context_data(self, **kwargs):
        context = super(ImprimirGruposPlanillaAsistencia, self).get_context_data(**kwargs)
        mes= int(kwargs['mes'])
        year = Year().get_activo(self.request)
        context['year'] = year.__unicode__()
        context['grupo_list'] = Grupo.objects.filter(year=year).annotate(Count('asistencia')).filter(asistencia__count__gt=0)
        ano = year.start_year
        if mes < 8 :
            ano = ano + 1 
        context['ano'] = ano
        mes_nombre = calendar.month_name[mes]
        context['mes'] = mes
        context['mes_nombre'] = calendar.month_name[mes]
        return context

class ImprimirAlumnosCartaFaltas(ListView):
    model = Asistencia
    def get_context_data(self, **kwargs):
        context = super(ImprimirAlumnosCartaFaltas, self).get_context_data(**kwargs)
        #mes= int(kwargs['mes'])
        #year = Year().get_activo(self.request)
        return context
    def get_queryset(self):
        year = Year().get_activo(self.request)
        mes= int(self.kwargs['mes'])
        return Asistencia.objects.filter(year=year).filter(falta__mes=mes).annotate(faltas_mes=Count('falta')).filter(justificada__mes=mes).annotate(justificadas_mes=Count('justificada')).order_by('-faltas_mes')
    filename = 'alumnos_carta_faltas.pdf'
    template_name = 'Year().get_activo(self.request)'

@method_decorator(permission_required('gestioneide.informes_view',raise_exception=True),name='dispatch')
class ImprimirCartaNotasTrimestre(PDFTemplateView):
    filename='carta_notas_trimestre.pdf'
    #Para el PDF
    cmd_options = {
        'margin-bottom': 15,
        'margin-top': 15,
        'margin-left': 25,
        'margin-right': 25
    }
    def get_context_data(self, **kwargs):
        context = super(ImprimirCartaNotasTrimestre, self).get_context_data(**kwargs)
        year = Year().get_activo(self.request)
        context['year'] = year.__unicode__()
        trimestre = int(self.kwargs['trimestre'])
        context['trimestre'] = trimestre
        grupo = Grupo.objects.get(id=self.kwargs['grupo_id'])
        context['asistencia_list'] = grupo.asistencia_set.all()
        return context

    def get_template_names(self):
        return ["alumnos_carta_notas_pdf.html"]

@method_decorator(permission_required('gestioneide.informes_view',raise_exception=True),name='dispatch')
class ImprimirCartaNotasTrimestreHtml(TemplateView):
    def get_context_data(self, **kwargs):
        context = super(ImprimirCartaNotasTrimestreHtml, self).get_context_data(**kwargs)
        year = Year().get_activo(self.request)
        context['year'] = year.__unicode__()
        trimestre = int(self.kwargs['trimestre'])
        context['trimestre'] = trimestre
        grupo = Grupo.objects.get(id=self.kwargs['grupo_id'])
        context['asistencia_list'] = grupo.asistencia_set.all()
        return context

    def get_template_names(self):
        return ["alumnos_carta_notas_pdf.html"]


@method_decorator(permission_required('gestioneide.informes_view',raise_exception=True),name='dispatch')
class ImprimirCartaNotasCuatrimestre(PDFTemplateView):
    filename='carta_notas_cuatrimestre_grupo.pdf'
    template_name = "alumnos_carta_notas_cuatrimestre_pdf.html"
    cmd_options = {
        'margin-bottom': 15,
        'margin-top': 15,
        'margin-left': 25,
        'margin-right': 25
    }
    def get_context_data(self, **kwargs):
        context = super(ImprimirCartaNotasCuatrimestre, self).get_context_data(**kwargs)
        year = Year().get_activo(self.request)
        context['year'] = year.__unicode__()
        cuatrimestre = int(self.kwargs['cuatrimestre'])
        context['cuatrimestre'] = cuatrimestre
        grupo = Grupo.objects.get(id=self.kwargs['grupo_id'])
        context['asistencia_list'] = grupo.asistencia_set.all()
        return context


@method_decorator(permission_required('gestioneide.informes_view',raise_exception=True),name='dispatch')
class ImprimirCartaNotasFinal(PDFTemplateView):
    filename='carta_notas_final.pdf'
    template_name = "alumnos_carta_notas_final_pdf.html"
    cmd_options = {
        'margin-bottom': 15,
        'margin-top': 15,
        'margin-left': 25,
        'margin-right': 25
    }
    def get_context_data(self, **kwargs):
        context = super(ImprimirCartaNotasFinal, self).get_context_data(**kwargs)
        year = Year().get_activo(self.request)
        context['year'] = year.__unicode__()
        context['asistencia_list'] = Asistencia.objects.filter(year=year)
        return context
