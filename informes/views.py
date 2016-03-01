from django.shortcuts import render
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import HttpResponse
from gestioneide.models import Alumno

# Create your views here.


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