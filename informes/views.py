from django.shortcuts import render
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import HttpResponse
from gestioneide.models import *
from alumnos.views import *
from asistencias.views import *

import xlwt

class InformesHomeView(TemplateView):
    template_name="informes/home.html"
    def get_context_data(self, **kwargs):
        context = super(InformesHomeView, self).get_context_data(**kwargs)
        context['years'] = Year.objects.all()
        return context

class AlumnosErroresListView(AlumnoListView):
    #Solo listamos los activos y que estan en un grupo
    def get_queryset(self):
        return Alumno.objects.filter(activo=False).annotate(Count('asistencia')).filter(asistencia__count__gt=0)


class AlumnosBancoErroresListView(AlumnoListView):
    #Solo listamos los activos y que estan en un grupo
    def get_queryset(self):
        return Alumno.objects.filter(activo=False).filter(cuenta_bancaria="0000-0000-00-0000000000")


class AsistenciasErroresListView(AsistenciaListView):
    def get_queryset(self):
        year = Year.objects.get(activo=True)
        return Asistencia.objects.filter(year=year).filter(confirmado=False)

class AsistenciasDescuentoListView(AsistenciaListView):
    def get_queryset(self):
        year = Year.objects.get(activo=True)
        return Asistencia.objects.filter(year=year).filter(precio__isnull=False)


class GruposAlumnosListView(ListView):
    model = Grupo
    template_name = "informes/grupos_alumnos.html"
    def get_queryset(self):
        year = Year.objects.get(activo=True)
        return Grupo.objects.filter(year=year).annotate(Count('asistencia')).filter(asistencia__count__gt=0)
        
def export_grupos_xls(request):
    ano = Year.objects.get(activo=True)
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=grupos.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet("Grupos")
    
    row_num = 0
    
    columns = [
        (u"ID", 2000),
        (u"Nombre", 4000),
        (u"Curso", 6000),
        (u"Clases", 8000),
        (u"Alumno", 8000),
        (u"Confirmados", 8000),
    ]

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    for col_num in xrange(len(columns)):
        ws.write(row_num, col_num, columns[col_num][0], font_style)
        # set column width
        ws.col(col_num).width = columns[col_num][1]

    font_style = xlwt.XFStyle()
    font_style.alignment.wrap = 1
    
    for grupo in Grupo.objects.filter(year=ano):
        row_num += 1
        clases = ""
        for clase in grupo.clases.all():
            clases = clases + "%s"%clase
        row = [
            grupo.pk,
            grupo.nombre,
            grupo.curso.__unicode__(),
            clases,
            grupo.asistencia_set.all().count(),
            grupo.confirmados(),
        ]
        for col_num in xrange(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
            
    wb.save(response)
    return response



def export_alumnos_xls(request):
    
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=alumnos.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet("Alumnos")
    
    row_num = 0
    
    columns = [
        (u"ID", 2000),
        (u"Apellidos, Nombre", 6000),
        (u"Fecha Nac.", 8000),
        (u"Grupo", 8000),
    ]

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    for col_num in xrange(len(columns)):
        ws.write(row_num, col_num, columns[col_num][0], font_style)
        # set column width
        ws.col(col_num).width = columns[col_num][1]

    font_style = xlwt.XFStyle()
    font_style.alignment.wrap = 1
    
    for alumno in Alumno.objects.filter(activo=True):
        row_num += 1
        row = [
            alumno.pk,
            "%s %s, %s"%(alumno.apellido1,alumno.apellido2,alumno.nombre),
            alumno.fecha_nacimiento.isoformat(),
            alumno.asistencia_set.all()[0].grupo.nombre
        ]
        for col_num in xrange(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
            
    wb.save(response)
    return response


def export_asistencias_no_confirmadas_xls(request):
    return export_asistencias_xls(request,"noconfirmadas")

def export_asistencias_xls(request,filtro=False):
    ano = Year.objects.get(activo=True)
    response = HttpResponse(content_type='application/ms-excel')
    filename = "asistencias"
    if filtro:
        filename = filename + "_" + filtro
    
    response['Content-Disposition'] = 'attachment; filename=%s.xls'%filename
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet("Alumnos")
    
    row_num = 0
    
    columns = [
        (u"ID", 2000),
        (u"Apellidos, Nombre", 6000),
        (u"Fecha Nac.", 8000),
        (u"Grupo", 8000),
    ]

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    for col_num in xrange(len(columns)):
        ws.write(row_num, col_num, columns[col_num][0], font_style)
        # set column width
        ws.col(col_num).width = columns[col_num][1]

    font_style = xlwt.XFStyle()
    font_style.alignment.wrap = 1
    if filtro == "noconfirmadas":
        queryset = Asistencia.objects.filter(year=ano).filter(confirmado=False)
    else:
        queryset = Asistencia.objects.filter(year=ano)
    for asistencia in queryset:
        alumno = asistencia.alumno
        row_num += 1
        row = [
            alumno.pk,
            "%s %s, %s"%(alumno.apellido1,alumno.apellido2,alumno.nombre),
            alumno.fecha_nacimiento.isoformat(),
            alumno.asistencia_set.all()[0].grupo.nombre
        ]
        for col_num in xrange(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
            
    wb.save(response)
    return response


def export_telefonos_alumnos_xls(request,ano):
    
    ano = Year.objects.get(id=ano)
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=telefonos_alumnos.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet("Alumnos")
    
    row_num = 0
    
    columns = [
        (u"ID", 2000),
        (u"Apellidos, Nombre", 6000),
        (u"Telefono1", 6000),
        (u"Telefono2", 6000),
        (u"Fecha Nac.", 8000),
        (u"Grupo", 8000),
    ]

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    for col_num in xrange(len(columns)):
        ws.write(row_num, col_num, columns[col_num][0], font_style)
        # set column width
        ws.col(col_num).width = columns[col_num][1]

    font_style = xlwt.XFStyle()
    font_style.alignment.wrap = 1
    
    for asis in Asistencia.objects.filter(year=ano):
        alumno = asis.alumno
        row_num += 1
        row = [
            alumno.id,
            "%s %s, %s"%(alumno.apellido1,alumno.apellido2,alumno.nombre),
            alumno.telefono1,
            alumno.telefono2,
            alumno.fecha_nacimiento.isoformat(),
            asis.grupo.nombre
        ]
        for col_num in xrange(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
            
    wb.save(response)
    return response
