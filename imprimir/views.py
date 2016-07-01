from django.shortcuts import render
import datetime
import os
import calendar

from django.conf import settings

from wkhtmltopdf.views import PDFTemplateView

from gestioneide.models import *

class ImprimirGrupos(PDFTemplateView):
    filename='grupos.pdf'
    template_name = "grupos_pdf.html"    
    def get_context_data(self, **kwargs):
        context = super(ImprimirGrupos, self).get_context_data(**kwargs)
        year = Year.objects.get(activo=True)
        context['year'] = year.__unicode__()
        context['grupo_list'] = Grupo.objects.filter(year=year).annotate(Count('asistencia')).filter(asistencia__count__gt=0)
        return context

class ImprimirGruposAlumnos(PDFTemplateView):
    filename='listado_grupos_con_alumnos.pdf'
    template_name = "grupos_alumnos_pdf.html"
    def get_context_data(self, **kwargs):
        context = super(ImprimirGruposAlumnos, self).get_context_data(**kwargs)
        year = Year.objects.get(activo=True)
        context['year'] = year.__unicode__()
        if 'grupo_id' in kwargs:
            context['grupo_list'] = Grupo.objects.filter(id=kwargs['grupo_id'])
        else:
            context['grupo_list'] = Grupo.objects.filter(year=year).annotate(Count('asistencia')).filter(asistencia__count__gt=0)
        return context

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
            print "Confirmamos la asistencia"
            asistencia.confirmado = True
            asistencia.save()
    
        context['asistencia'] = asistencia
        year = Year.objects.get(activo=True)
        context['lista_festivos'] =Festivo.objects.filter(year=year)
        return context

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

class ImprimirGruposPlanillaAsistencia(PDFTemplateView):
    filename='grupos_planilla_asistencia.pdf'
    template_name = 'grupos_planilla_asistencia_pdf.html'
    cmd_options = {
        "orientation": "landscape",
        'margin-bottom': 10,
        'margin-top': 10,
        'margin-left': 15,
        'margin-right': 15
        }
    def get_context_data(self, **kwargs):
        context = super(ImprimirGruposPlanillaAsistencia, self).get_context_data(**kwargs)
        mes= int(kwargs['mes'])
        year = Year.objects.get(activo=True)
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
