# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required

from django.core.validators import validate_email

import xlwt
from wkhtmltopdf.views import PDFTemplateView

from gestioneide.models import *
from gestioneide.utils import validar_ccc
from alumnos.views import *
from asistencias.views import *

@method_decorator(permission_required('gestioneide.informes_view',raise_exception=True),name='dispatch')
class InformesHomeView(TemplateView):
    template_name="informes/home.html"
    def get_context_data(self, **kwargs):
        context = super(InformesHomeView, self).get_context_data(**kwargs)
        context['years'] = Year.objects.all().order_by('-id')
        return context

@method_decorator(permission_required('gestioneide.informes_view',raise_exception=True),name='dispatch')
class ProfesoresClasesView(PDFTemplateView):
    filename='profesores_clases.pdf'
    template_name = "informes/listado_profesores_clases.html"
    def get_context_data(self, **kwargs):
        context = super(ProfesoresClasesView, self).get_context_data(**kwargs)
        context["profesores_list"]=Profesor.objects.all()
        return context

@method_decorator(permission_required('gestioneide.informes_view',raise_exception=True),name='dispatch')
class AulasClasesView(PDFTemplateView):
    filename='aulas_clases.pdf'
    template_name = "informes/listado_aulas_clases.html"
    def get_context_data(self, **kwargs):
        context = super(AulasClasesView, self).get_context_data(**kwargs)
        context["aulas_list"]=Aula.objects.all()
        return context
        
@method_decorator(permission_required('gestioneide.informes_view',raise_exception=True),name='dispatch')
class AlumnosErroresListView(AlumnoListView):
    #Solo listamos los activos y que estan en un grupo
    def get_queryset(self):
        return Alumno.objects.filter(activo=False).annotate(Count('asistencia')).filter(asistencia__count__gt=0)

#FIXME este permiso deberia ser mas especifico porque hay datos sensibles
@method_decorator(permission_required('gestioneide.informes_view',raise_exception=True),name='dispatch')
class AlumnosBancoErroresListView(TemplateView):
    template_name="informes/alumnos_cuenta_mal.html"
    def get_context_data(self, **kwargs):
        context = super(AlumnosBancoErroresListView, self).get_context_data(**kwargs)
        lista_alumnos = []
        year = Year().get_activo(self.request)
        for asistencia in Asistencia.objects.filter(year=year).filter(metalico=False):
            if not validar_ccc(asistencia.alumno.cuenta_bancaria):
                lista_alumnos.append(asistencia.alumno)
        context['alumnos_list'] = lista_alumnos
        return context

@method_decorator(permission_required('gestioneide.informes_view',raise_exception=True),name='dispatch')
class AlumnosMailErroresListView(TemplateView):
    template_name="informes/alumnos_mail_mal.html"
    def get_context_data(self, **kwargs):
        context = super(AlumnosMailErroresListView, self).get_context_data(**kwargs)
        lista_alumnos = []
        year = Year().get_activo(self.request)
        for asistencia in Asistencia.objects.filter(year=year).filter(metalico=False):
            try:
                validate_email(asistencia.alumno.email)
            except:
                lista_alumnos.append(asistencia.alumno)
        context['alumnos_list'] = lista_alumnos
        return context


@method_decorator(permission_required('gestioneide.informes_view',raise_exception=True),name='dispatch')
class AsistenciasErroresListView(AsistenciaListView):
    def get_queryset(self):
        year = Year().get_activo(self.request)
        return Asistencia.objects.filter(year=year).filter(confirmado=False)

@method_decorator(permission_required('gestioneide.informes_view',raise_exception=True),name='dispatch')
class AsistenciasDescuentoListView(AsistenciaListView):
    def get_queryset(self):
        year = Year().get_activo(self.request)
        return Asistencia.objects.filter(year=year).filter(precio__isnull=False)

@method_decorator(permission_required('gestioneide.informes_view',raise_exception=True),name='dispatch')
class AsistenciasMetalicoListView(AsistenciaListView):
    def get_queryset(self):
        year = Year().get_activo(self.request)
        return Asistencia.objects.filter(year=year).filter(metalico=True)

@method_decorator(permission_required('gestioneide.informes_view',raise_exception=True),name='dispatch')
class GruposAlumnosListView(ListView):
    model = Grupo
    template_name = "informes/grupos_alumnos.html"
    def get_queryset(self):
        year = Year().get_activo(self.request)
        return Grupo.objects.filter(year=year).annotate(Count('asistencia')).filter(asistencia__count__gt=0)

@permission_required('gestioneide.informes_view',raise_exception=True)
def export_grupos_xls(request):
    ano = Year().get_activo(self.request)
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

@permission_required('gestioneide.informes_view',raise_exception=True)
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
    
    year = Year().get_activo(request)
    for asistencia in Asistencia.objects.filter(year=year):
        alumno = asistencia.alumno
        row_num += 1
        row = [
            alumno.pk,
            "%s %s, %s"%(alumno.apellido1,alumno.apellido2,alumno.nombre),
            alumno.fecha_nacimiento.isoformat(),
            "%s (%s)"%(asistencia.grupo.nombre,year)
        ]
        for col_num in xrange(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
            
    wb.save(response)
    return response

@permission_required('gestioneide.informes_view',raise_exception=True)
def export_asistencias_no_confirmadas_xls(request):
    return export_asistencias_xls(request,"noconfirmadas")

@permission_required('gestioneide.informes_view',raise_exception=True)
def export_asistencias_xls(request,filtro=False):
    ano = Year().get_activo(request)
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
        (u"Telefono1", 6000),
        (u"Telefono2", 6000),
        (u"Mail", 6000),
        (u"Mail2", 6000),
        (u"Dirección", 6000),
        (u"Localidad", 6000),
        (u"CP", 2000),

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
            alumno.asistencia_set.all()[0].grupo.nombre,
            alumno.telefono1,
            alumno.telefono2,
            alumno.email,
            alumno.email2,
            alumno.direccion,
            alumno.ciudad,
            alumno.cp
        ]
        for col_num in xrange(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
            
    wb.save(response)
    return response

@permission_required('gestioneide.informes_view',raise_exception=True)
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
        (u"Mail", 6000),
        (u"Mail2", 6000),
        (u"Fecha Nac.", 4000),
        (u"Año Nac.", 3000),
        (u"Grupo", 8000),
        (u"Dirección", 12000),
        (u"CP", 6000),
        (u"Ciudad", 8000)
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
            alumno.email,
            alumno.email2,
            alumno.fecha_nacimiento.isoformat(),
            alumno.fecha_nacimiento.isocalendar()[0],
            asis.grupo.nombre,
            asis.alumno.direccion,
            asis.alumno.cp,
            asis.alumno.ciudad,
        ]
        for col_num in xrange(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
            
    wb.save(response)
    return response

@permission_required('gestioneide.informes_view',raise_exception=True)
def export_alumnos_mail_errores_xls(request):
    ano = Year().get_activo(request)
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=mails_alumnos.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet("Alumnos")
    
    row_num = 0
    
    columns = [
        (u"ID", 2000),
        (u"Apellidos, Nombre", 6000),
        (u"Mail", 6000),
        (u"Mail2", 6000),
        (u"Telefono1", 6000),
        (u"Telefono2", 6000),
        (u"Fecha Nac.", 2000),
        (u"Año Nac.", 2000),
        (u"Grupo", 8000),
        (u"Dirección", 12000),
        (u"CP", 6000),
        (u"Ciudad", 8000)
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
        try:
            validate_email(asis.alumno.email)
        except:
            alumno = asis.alumno
            row_num += 1
            row = [
                alumno.id,
                "%s %s, %s"%(alumno.apellido1,alumno.apellido2,alumno.nombre),
                alumno.email,
                alumno.email2,
                alumno.telefono1,
                alumno.telefono2,
                alumno.fecha_nacimiento.isoformat(),
                alumno.fecha_nacimiento.isocalendar()[0],
                asis.grupo.nombre,
                asis.alumno.direccion,
                asis.alumno.cp,
                asis.alumno.ciudad,
            ]
            for col_num in xrange(len(row)):
                ws.write(row_num, col_num, row[col_num], font_style)
            
    wb.save(response)
    return response

@permission_required('gestioneide.informes_view',raise_exception=True)
def export_notas_trimestre_xls(request,trimestre):
    
    ano = Year().get_activo(request)
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=notas_trimestre.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet("Notas")
    
    row_num = 0
    
    columns = [
        (u"ID", 2000),
        (u"Apellidos",6000),
        (u"Nombre", 4000),
        (u"Direccion", 8000),
        (u"CP", 2000),
        (u"Ciudad", 4000),
        (u"Grupo", 8000),
        (u"Nota", 2000),
        (u"NP", 1000),
        (u"Faltas", 2000),
        (u"Justificadas", 2000),
        (u"Observaciones", 8000),
    ]

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    for col_num in xrange(len(columns)):
        ws.write(row_num, col_num, columns[col_num][0], font_style)
        # set column width
        ws.col(col_num).width = columns[col_num][1]

    font_style = xlwt.XFStyle()
    font_style.alignment.wrap = 1
    import random 
    for asis in Asistencia.objects.filter(year=ano):
        alumno = asis.alumno
        nota,observaciones,np = asis.nota_trimestre(trimestre)
        row_num += 1
        row = [
            alumno.id,
            "%s %s"%(alumno.apellido1,alumno.apellido2),
            alumno.nombre,
            u"%s"%alumno.direccion,
            alumno.cp,
            u"%s"%alumno.ciudad,
            asis.grupo.nombre,
	        nota,
            np,
            "%d"%asis.faltas_trimestre(trimestre),
            "%d"%asis.justificadas_trimestre(trimestre),
            #random.randint(1, 10),
            #random.randint(1, 10),
            observaciones
        ]
        for col_num in xrange(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
            
    wb.save(response)
    return response

@permission_required('gestioneide.informes_view', raise_exception=True)
def export_notas_cuatrimestre_xls(request, ano):
    ano = Year().get_activo(request)
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=notas_%s_cuatrimestre.xls'%(ano)
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet("Notas %s Cuatrimestre"%(ano))

    row_num = 0

    columns = [
        (u"ID", 2000),
        (u"Apellidos", 6000),
        (u"Nombre", 4000),
        (u"Direccion", 8000),
        (u"CP", 2000),
        (u"Ciudad", 4000),
        (u"Grupo", 8000),
        (u"T1. Nota", 2000),
        (u"T1. Observaciones", 2000),
        (u"T1. Faltas", 2000),
        (u"T1. Justificadas", 2000),
        (u"T2. Nota", 2000),
        (u"T2. Observaciones", 2000),
        (u"T2. Faltas", 2000),
        (u"T2. Justificadas", 2000),
        (u"T3. Nota", 2000),
        (u"T3. Observaciones", 2000),
        (u"T3. Faltas", 2000),
        (u"T3. Justificadas", 2000),
        (u"Q1. Grammar", 2000),
        (u"Q1. Reading", 2000),
        (u"Q1. Writing", 2000),
        (u"Q1. Read./Wri.", 2000),
        (u"Q1. Use of english", 2000),
        (u"Q1. listening", 2000),
        (u"Q1. Speaking", 2000),
        (u"Q1. Media", 2000),
        (u"Q1. Observaciones", 8000),
        (u"Q2. Grammar", 2000),
        (u"Q2. Reading", 2000),
        (u"Q2. Writing", 2000),
        (u"Q2. Read./Wri.", 2000),
        (u"Q2. Use of english", 2000),
        (u"Q2. listening", 2000),
        (u"Q2. Speaking", 2000),
        (u"Q2. Media", 2000),
        (u"Q2. Observaciones", 8000),
        (u"Q3. Grammar", 2000),
        (u"Q3. Reading", 2000),
        (u"Q3. Writing", 2000),
        (u"Q3. Read./Wri.", 2000),
        (u"Q3. Use of english", 2000),
        (u"Q3. listening", 2000),
        (u"Q3. Speaking", 2000),
        (u"Q3. Media", 2000),
        (u"Q3. Observaciones", 8000),
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
        row_num += 1
        row = [
            asis.alumno.id,
            "%s %s" % (asis.alumno.apellido1, asis.alumno.apellido2),
            asis.alumno.nombre,
            u"%s" % asis.alumno.direccion,
            asis.alumno.cp,
            u"%s" % asis.alumno.ciudad,
            asis.grupo.nombre
        ]
        meses_trimestre = { 1: [9,10,11,12], 2: [1,2,3], 3: [4,5,6]}
        for trimestre in 1, 2, 3:
            resultados = asis.notatrimestral_set.filter(trimestre=trimestre)
            if len(resultados) > 0:
                for nota in resultados:
                    row.append(nota.nota)
                    row.append(nota.observaciones)
                    faltas = 0
                    justificadas = 0
                    for mes in meses_trimestre[trimestre]:
                        faltas =+ Falta.objects.filter(asistencia=asis,mes=mes).count()
                        justificadas =+ Justificada.objects.filter(asistencia=asis,mes=mes).count()
                    row.append(faltas)
                    row.append(justificadas)
            else:
                row.append("")
                row.append("")
                row.append("")
                row.append("")

        for cuatrimestre in 1,2,3:
            for nota in asis.notacuatrimestral_set.filter(cuatrimestre=cuatrimestre):
                row.append(nota.grammar)
                row.append(nota.reading)
                row.append(nota.writing)
                row.append(nota.reading_writing)
                row.append(nota.useofenglish)
                row.append(nota.listening)
                row.append(nota.speaking)
                row.append(nota.media())
                row.append(nota.observaciones)
                
        for col_num in xrange(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response

#~ @permission_required('gestioneide.informes_view',raise_exception=True)
class NotasTrimestralesAnoListView(ListView):
    model = NotaTrimestral
    template_name = "informes/informes_notas_ano.html"
    context_object_name = 'notas_list'
    def get_queryset(self):
        year = Year.objects.get(start_year=self.kwargs['ano'])
        asistencias = Asistencia.objects.filter(year=year)
        return NotaTrimestral.objects.filter(asistencia__in=asistencias,trimestre=3).order_by('asistencia__alumno__apellido1','asistencia__alumno__apellido1','asistencia__alumno__nombre')
    def get_context_data(self, **kwargs):
        context = super(NotasTrimestralesAnoListView, self).get_context_data(**kwargs)
        context['year'] = Year.objects.get(start_year=self.kwargs['ano'])
        return context

#~ @permission_required('gestioneide.informes_view',raise_exception=True)
class NotasTrimestralesLegacyListView(ListView):
    model = Nota
    template_name = "informes/informes_notas_trimestre_legacy.html"
    context_object_name = 'notas_list'
    paginate_by = 100
    def get_queryset(self):
        year = Year.objects.get(start_year=self.kwargs['ano'])
        asistencias = Asistencia.objects.filter(year=year)
        return Nota.objects.filter(asistencia__in=asistencias,trimestre=self.kwargs['trimestre']).order_by('asistencia__alumno__apellido1','asistencia__alumno__apellido1','asistencia__alumno__nombre')
    def get_context_data(self, **kwargs):
        context = super(NotasTrimestralesLegacyListView, self).get_context_data(**kwargs)
        context['year'] = Year.objects.get(start_year=self.kwargs['ano'])
        return context

class NotasCuatrimestralesAnoListView(ListView):
    model = NotaCuatrimestral
    template_name = "informes/informes_notas_cuatrimestrales_ano.html"
    context_object_name = 'notas_list'

    def get_queryset(self):
        year = Year.objects.get(start_year=self.kwargs['ano'])
        asistencias = Asistencia.objects.filter(year=year)
        return NotaCuatrimestral.objects.filter(asistencia__in=asistencias).order_by(
            'asistencia__alumno__apellido1', 'asistencia__alumno__apellido1', 'asistencia__alumno__nombre')

    def get_context_data(self, **kwargs):
        context = super(NotasCuatrimestralesAnoListView, self).get_context_data(**kwargs)
        context['year'] = Year.objects.get(start_year=self.kwargs['ano'])
        return context

class NotasFinalesAnoListView(ListView):
    model = Asistencia
    template_name = "informes/informes_notas_finales_ano.html"
    context_object_name = 'asistencia_list'
    def get_queryset(self):
        year = Year.objects.get(start_year=self.kwargs['ano'])
        asistencias = Asistencia.objects.filter(year=year,borrada=False).order_by('alumno__apellido1','alumno__apellido2','alumno__nombre')
        return asistencias
    def get_context_data(self, **kwargs):
        context = super(NotasFinalesAnoListView, self).get_context_data(**kwargs)
        context['year'] = Year.objects.get(start_year=self.kwargs['ano'])
        return context

@permission_required('gestioneide.informes_view',raise_exception=True)
def export_notas_finales_xls(request,ano):
    year = Year.objects.get(start_year=ano)
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=notas_finales.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet("Notas %s"%year)
    
    row_num = 0
    
    columns = [
        (u"ID", 2000),
        (u"Apellidos",6000),
        (u"Nombre", 4000),
        (u"Grupo", 8000),
        (u"Tipo", 2000),
        (u"Nota", 2000),
        (u"Faltas", 2000),
        (u"Justificadas", 2000),
    ]

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    for col_num in xrange(len(columns)):
        ws.write(row_num, col_num, columns[col_num][0], font_style)
        # set column width
        ws.col(col_num).width = columns[col_num][1]

    font_style = xlwt.XFStyle()
    font_style.alignment.wrap = 1
    import random 
    for asis in Asistencia.objects.filter(year=year,borrada=False).order_by('alumno__apellido1','alumno__apellido2','alumno__nombre'):
        alumno = asis.alumno
        nota_final = asis.nota_final()
        row_num += 1
        row = [
            alumno.id,
            "%s %s"%(alumno.apellido1,alumno.apellido2),
            alumno.nombre,
            asis.grupo.nombre,
            nota_final["tipo"],
	    nota_final["media"],
            nota_final["faltas"],
            nota_final["justificadas"],
        ]
        for col_num in xrange(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
            
    wb.save(response)
    return response

