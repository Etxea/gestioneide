from django.shortcuts import render
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import HttpResponse
from gestioneide.models import *
from alumnos.views import *
from asistencias.views import *

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

class AsistenciasErroresListView(AsistenciaListView):
    def get_queryset(self):
        year = Year.objects.get(activo=True)
        return Asistencia.objects.filter(year=year).filter(confirmado=False)

class GruposAlumnosListView(ListView):
    model = Grupo
    template_name = "informes/grupos_alumnos.html"
    def get_queryset(self):
        year = Year.objects.get(activo=True)
        return Grupo.objects.filter(year=year).annotate(Count('asistencia')).filter(asistencia__count__gt=0)
        

def export_alumnos_xls(request):
    import xlwt
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

def export_telefonos_alumnos_xls(request,ano):
    import xlwt
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
