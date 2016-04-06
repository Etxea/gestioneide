from django.shortcuts import render
import datetime
import os
import calendar

from django.conf import settings
from django.http import HttpResponse
from django.template import Context
from django.template.loader import get_template

from xhtml2pdf import pisa

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
            raise Exception(
                'media URI must start with %s or %s' % (sUrl, mUrl)
            )
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

def ImprimirAlumnoMatricula(request,alumno_id):
    data = {}
    alumno = Alumno.objects.get(id=alumno_id)
    data['alumno'] = alumno
    template = get_template('matricula_alumno_pdf.html')
    html = template.render(Context(data))
    f = open(os.path.join(settings.MEDIA_ROOT, 'matricula_alumno_%s.pdf'%alumno_id), "w+b")
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
