from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View, ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import SingleObjectMixin
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from gestioneide.models import *
from forms import *

import xlwt

@method_decorator(permission_required('gestioneide.recibo_view',raise_exception=True),name='dispatch')
class ReciboListView(ListView):
    model = Recibo
    ordering = "-fecha_creacion"
    template_name = "recibos_list.html"

@method_decorator(permission_required('gestioneide.recibo_add',raise_exception=True),name='dispatch')
class ReciboCreateView(CreateView):
    model = Recibo
    template_name = "recibo_create.html"
    form_class = ReciboCreateForm
    def get_initial(self):
        year = Year().get_activo(self.request)
        return { 'year': year }


@method_decorator(permission_required('gestioneide.recibo_add',raise_exception=True),name='dispatch')
class ReciboUpdateView(UpdateView):
    model = Recibo
    template_name = "recibo_update.html"
    form_class = ReciboUpdateForm
    def get_initial(self):
        year = Year().get_activo(self.request)
        return { 'year': year }

@method_decorator(permission_required('gestioneide.recibo_view',raise_exception=True),name='dispatch')
class ReciboDetailView(DetailView):
    model = Recibo
    template_name = "recibo_detail.html"

@method_decorator(permission_required('gestioneide.recibo_view',raise_exception=True),name='dispatch')
class ReciboInformeView(DetailView):
    model = Recibo
    template_name = "recibo_informe.html"

#@method_decorator(permission_required('gestioneide.recibo_view',raise_exception=True),name='dispatch')
def ReciboInformeExcelView(request,pk):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=recibos_alumnos.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet("Alumnos")
    
    row_num = 0
    
    columns = [
        (u"Numero", 2000),
        (u"Apellidos, Nombre", 8000),
        (u"Cuenta", 6000),
        (u"Precio", 3000),
        (u"Grupo", 8000),
        (u"Tipo Cobro", 5000)
    ]

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    for col_num in xrange(len(columns)):
        ws.write(row_num, col_num, columns[col_num][0], font_style)
        # set column width
        ws.col(col_num).width = columns[col_num][1]

    font_style = xlwt.XFStyle()
    font_style.alignment.wrap = 1
    recibo = Recibo.objects.get(id=pk)
    print "tenemos el recibo",recibo.get_alumnos_metalico()
    for asistencia in recibo.get_alumnos():
        tipo="recibo"
        if asistencia.metalico:
            tipo = "metalico"
        elif asistencia.factura:
            tipo="factura"
        if recibo.medio_mes:
            precio = float(asistencia.ver_precio()) / 2 
        else:
            precio = asistencia.ver_precio()
        alumno = asistencia.alumno
        row_num += 1
        row = [
            alumno.id,
            "%s %s, %s"%(alumno.apellido1,alumno.apellido2,alumno.nombre),
            alumno.cuenta_bancaria,
            precio,
            asistencia.grupo.nombre,
            tipo
        ]
        for col_num in xrange(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
    
    wb.save(response)
    return response

@method_decorator(permission_required('gestioneide.recibo_view',raise_exception=True),name='dispatch')
class ReciboFicheroView(View,SingleObjectMixin):
    model = Recibo
    template_name = "recibo_fichero.html"
    def get(self, request, *args, **kwargs):
        fichero = self.get_object().csb19()
        response = HttpResponse(content_type='text/txt')
        response['Content-Disposition'] = 'attachment; filename="csb19.txt"'
        response.write(fichero)
        return response

@method_decorator(permission_required('gestioneide.recibo_delete',raise_exception=True),name='dispatch')
class ReciboDeleteView(DeleteView):
    model = Recibo
