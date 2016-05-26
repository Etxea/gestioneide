from django.shortcuts import render
import datetime
import os
import calendar

from django.conf import settings
from django.http import HttpResponse
from django.template import Context
from django.template.loader import get_template

from xhtml2pdf import pisa
from wkhtmltopdf.views import PDFTemplateView

from gestioneide.models import *

def link_callback(uri, rel):
    """
    Convert HTML URIs to absolute system paths so xhtml2pdf can access those
    resources
    """
    print "Convirtiendo...",uri,rel
    # use short variable names
    sUrl = settings.STATIC_URL      # Typically /static/
    sRoot = settings.STATIC_ROOT    # Typically /home/userX/project_static/
    mUrl = settings.MEDIA_URL       # Typically /static/media/
    mRoot = settings.MEDIA_ROOT     # Typically /home/userX/project_static/media/

    # convert URIs to absolute system paths
    if uri.startswith(mUrl):
        path = os.path.join(mRoot, uri.replace(mUrl, ""))
    elif uri.startswith(sUrl):
        path = os.path.join(sRoot, uri.replace(sUrl, ""))
    else:
        return uri  # handle absolute uri (ie: http://some.tld/foo.png)

    # make sure that file exists
    if not os.path.isfile(path):
            print "Tenemos el path que falla",path
            return path
    return path

def ImprimirGrupos(request):
    data = {}
    year = Year.objects.get(activo=True)
    grupos = Grupo.objects.filter(year=year)
    data['grupo_list'] = grupos
    data['year'] = year.__unicode__()
    template = get_template('grupos_pdf.html')
    html = template.render(Context(data))
    f = open(os.path.join(settings.MEDIA_ROOT, 'test.pdf'), "w+b")
    pisaStatus = pisa.CreatePDF(html, dest=f, link_callback=link_callback)
    f.seek(0)
    pdf = f.read()
    f.close()
    return HttpResponse(pdf, content_type='application/pdf')

#~ def ImprimirGruposAlumnos(request):
    #~ data = {}
    #~ year = Year.objects.get(activo=True)
    #~ if request.method == 'POST':
        #~ if 'listagrupos' in request.POST:
            #~ lista=request.POST.getlist('listagrupos')
            #~ print "tenemos la lista de grupos"
            #~ print lista
            #~ grupos = Grupo.objects.filter(year=year).filter(id__in=lista)
        #~ if 'grupo_id' in request.POST:
            #~ grupo_id = request.POST['grupo_id']
            #~ print "Buscamos el grupo ",grupo_id
            #~ grupos = Grupo.objects.filter(year=year).filter(id=grupo_id)
    #~ else:
        #~ grupos = Grupo.objects.filter(year=year).annotate(Count('asistencia')).filter(asistencia__count__gt=0)
#~ 
    #~ data['grupo_list'] = grupos
    #~ data['year'] = year.__unicode__()
    #~ template = get_template('grupos_alumnos_pdf.html')
    #~ html = template.render(Context(data))
    #~ f = open(os.path.join(settings.MEDIA_ROOT, 'grupos_alumnos_%s.pdf'%year), "w+b")
    #~ pisaStatus = pisa.CreatePDF(html, dest=f, link_callback=link_callback)
    #~ print "Tebenemos pisastatus",pisaStatus
    #~ f.seek(0)
    #~ pdf = f.read()
    #~ f.close()
    #~ return HttpResponse(pdf, content_type='application/pdf')


class ImprimirGruposAlumnos(PDFTemplateView):
    filename='my_pdf.pdf'
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
    def get_context_data(self, **kwargs):
        context = super(ImprimirAlumnoMatricula, self).get_context_data(**kwargs)
        alumno_id= kwargs['alumno_id']
        alumno = Alumno.objects.get(id=alumno_id)
        context['alumno'] = alumno
        return context
    
def ImprimirAlumnoOctavilla(request,alumno_id):
    data = {}
    alumno = Alumno.objects.get(id=alumno_id)
    data['alumno'] = alumno
    template = get_template('octavilla_alumno_pdf.html')
    html = template.render(Context(data))
    f = open(os.path.join(settings.MEDIA_ROOT, 'octavilla_alumno_%s.pdf'%alumno_id), "w+b")
    pisaStatus = pisa.CreatePDF(html, dest=f, link_callback=link_callback)
    f.seek(0)
    pdf = f.read()
    f.close()
    return HttpResponse(pdf, content_type='application/pdf')    
    

def ImprimirGruposPlanillaAsistencia(request,mes):
    year = Year.objects.get(activo=True)
    mes=int(mes)
    data = {}
    grupos = Grupo.objects.filter(year=year)
    data['grupo_list'] = grupos
    #FIXME esto habria que sacarlo de algun lado
    ano = year.start_year
    if mes < 8 :
        ano = ano + 1 
    data['ano'] = ano
    mes_nombre = calendar.month_name[mes]
    data['mes'] = mes
    data['mes_nombre'] = calendar.month_name[mes]

    template = get_template('grupos_planilla_asistencia_pdf.html')
    html = template.render(Context(data))
    f = open(os.path.join(settings.MEDIA_ROOT, 'test.pdf'), "w+b")
    pisaStatus = pisa.CreatePDF(html, dest=f, link_callback=link_callback)
    f.seek(0)
    pdf = f.read()
    f.close()
    return HttpResponse(pdf, content_type='application/pdf')
