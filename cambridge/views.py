# -*- coding: utf-8 -*-

#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  

from django.contrib.auth.decorators import login_required, permission_required
from django.template.loader import render_to_string
from django.template import RequestContext
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.views.generic import DetailView, ListView, CreateView, UpdateView, View
from django.views.generic.edit import ModelFormMixin
from django.contrib.sites.models import Site

from django.conf import settings
from sermepa.forms import SermepaPaymentForm
from sermepa.signals import payment_was_successful, payment_was_error, signature_error
from sermepa.models import SermepaIdTPV


import StringIO
import ho.pisa as pisa
from excel_response3 import ExcelResponse
from django_xhtml2pdf.utils import render_to_pdf_response
from models import *
from forms import *
import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)

def ver(request, pk):
    registration = get_object_or_404(Registration, id=pk)
    payload = {'registration': registration}
    file_data = render_to_string('cambridge/imprimir.html', payload, RequestContext(request))
    myfile = StringIO.StringIO()
    return HttpResponse( file_data )

def imprimir(registration,request):
    payload = {}
    payload["registration"] = registration
    response_pdf = render_to_pdf_response('cambridge/matricula_imprimir.html', payload, pdfname='cambridge-%s.pdf'%registration.id)
    #response_html = render_to_response('cambridge/matricula_imprimir.html', payload)
    #return response_html
    return response_pdf

@login_required
def imprimir_cambridge(request, pk):
    logger.debug("Vamos a imprimir una matricula normal")
    registration = Registration.objects.get(id=pk)
    return imprimir(registration,request)

def RegistrationPayment(request, pk, trans_type='0'):
    site = Site.objects.get_current()
    site_domain = site.domain
    reg = Registration.objects.get(id=pk)
    amount = int(5.50 * 100) #El precio es en céntimos de euro

    merchant_parameters = {
        "Ds_Merchant_Titular": 'John Doe',
        "Ds_Merchant_MerchantData": 'cam-%s'%reg.id, # id del Pedido o Carrito, para identificarlo en el mensaje de vuelta
        "Ds_Merchant_MerchantName": settings.SERMEPA_COMERCIO,
        "Ds_Merchant_ProductDescription": 'matricula-cambridge-%s'%reg.id,
        "Ds_Merchant_Amount": int(reg.exam.level.price*100),
        "Ds_Merchant_Terminal": settings.SERMEPA_TERMINAL,
        "Ds_Merchant_MerchantCode": settings.SERMEPA_MERCHANT_CODE,
        "Ds_Merchant_Currency": settings.SERMEPA_CURRENCY,
        "Ds_Merchant_MerchantURL":  settings.SERMEPA_URL_DATA,
        "Ds_Merchant_UrlOK": "http://%s%s" % (site_domain, reverse('cambridge_gracias')),
        #~ "Ds_Merchant_UrlOK": "http://%s%s" % (site_domain, reverse('end')),
        "Ds_Merchant_UrlKO": "http://%s%s" % (site_domain, reverse('cambridge_error')),
        #~ "Ds_Merchant_UrlKO": "http://%s%s" % (site_domain, reverse('end')),
        #"Ds_Merchant_Order": SermepaIdTPV.objects.new_idtpv(),
        "Ds_Merchant_TransactionType": '0',
    }
    if trans_type == '0': #Compra puntual
        order = SermepaIdTPV.objects.new_idtpv() #Tiene que ser un número único cada vez
        print "Tenemos la order ",order
        merchant_parameters.update({
            "Ds_Merchant_Order": order,
            "Ds_Merchant_TransactionType": trans_type,
        })
    elif trans_type == 'L': #Compra recurrente por fichero. Cobro inicial
        order = SermepaIdTPV.objects.new_idtpv() #Tiene que ser un número único cada vez
        merchant_parameters.update({
            "Ds_Merchant_Order": order,
            "Ds_Merchant_TransactionType": trans_type,
        })
    elif trans_type == 'M': #Compra recurrente por fichero. Cobros sucesivos
        # order = suscripcion.idtpv #Primer idtpv, 10 dígitos
        order = ''
        merchant_parameters.update({
            "Ds_Merchant_Order": order,
            "Ds_Merchant_TransactionType": trans_type,
        })
    elif trans_type == '0': #Compra recurrente por Referencia. Cobro inicial
        order = 'REQUIRED'
        merchant_parameters.update({
            "Ds_Merchant_Order": order,
            "Ds_Merchant_TransactionType": trans_type,
        })
    elif trans_type == '0': #Compra recurrente por Referencia. Cobros sucesivos
        # order = suscripcion.idreferencia #Primer idtpv, 10 dígitos
        order = ''
        merchant_parameters.update({
            "Ds_Merchant_Order": order,
            "Ds_Merchant_TransactionType": trans_type,
        })
    elif trans_type == '3': #Devolución
        # order = suscripcion.idreferencia #Primer idtpv, 10 dígitos
        order = ''
        merchant_parameters.update({
            "Ds_Merchant_Order": order,
            "Ds_Merchant_TransactionType": trans_type,
            #"Ds_Merchant_AuthorisationCode": pedido.Ds_AuthorisationCode, #Este valor sale
            "Ds_Merchant_AuthorisationCode": '',
            # de la SermepaResponse obtenida del cobro que se quiere devolver.
        })
        
    form = SermepaPaymentForm(merchant_parameters=merchant_parameters)
    print "Tenemos el form"
    print form.render()
    return HttpResponse(render_to_response('cambridge/payment.html', {'form': form, 'debug': settings.DEBUG, 'registration': reg}))
    
    
class RegistrationCreateView(CreateView):
    model = Registration
    form_class = RegistrationForm
    template_name='cambridge/registration_form.html'
    def get_success_url(self):
        return '/cambridge/pay/%d'%self.object.id
    
@login_required 
def RegistrationExcelView(request):
    objs = Registration.objects.filter(paid=True)
    return ExcelResponse(objs)

class RegistrationListView(ListView):
    template_name='cambridge/lista.html'
    #Limitamos a las matriculas de examenes posteriores al día de hoy y que estén pagadas
    queryset=Registration.objects.filter(exam__exam_date__gt=datetime.date.today(),paid=True).order_by('-registration_date')

class RegistrationListViewAll(ListView):
    template_name='cambridge/lista.html'
    #Limitamos a las matriculas de examenes posteriores al día de hoy y que estén pagadas
    queryset=Registration.objects.filter().order_by('-registration_date')

class ExamList(ListView):
    queryset=Exam.objects.filter(exam_date__gt=datetime.date.today())
    template_name='cambridge/exam_list.html'

class SchoolCreateView(CreateView):
    model = School
    fields = "__all__"
    success_url="/cambridge/schools/list/"

class SchoolExamList(ListView):
    queryset=SchoolExam.objects.filter(exam_date__gt=datetime.date.today())
    template_name='cambridge/school_exam_list.html'
    def get_context_data(self, **kwargs):
        context = super(SchoolExamList, self).get_context_data(**kwargs)
        context['schools'] = School.objects.all()
        return context

class SchoolListView(ListView):
    model = School

class SchoolExamCreate(CreateView):
    model = SchoolExam
    success_url="/cambridge/schools/exam/list/"
    template_name = "cambridge/school_exam_form.html"
    form_class = SchoolExamForm
    #Limitamos los niveles a los que tiene el colegio
    def get_form_kwargs(self):
        kwargs = super(SchoolExamCreate, self).get_form_kwargs()
        #recogemos y añadimos kwargs a la form
        kwargs['school_name'] = self.kwargs['school_name']
        return kwargs
    #Añadimos el school_name al contexto
    def get_context_data(self, **kwargs):
        context = super(SchoolExamCreate, self).get_context_data(**kwargs)
        context['school_name'] = self.kwargs['school_name']
        context['school'] = School.objects.get(name=self.kwargs['school_name'])
        return context
    def get_initial(self):
        return { 'school': School.objects.get(name=self.kwargs['school_name']) }

class SchoolRegistrationListView(ListView):
    template_name='cambridge/school_registration_list.html'
    #Limitamos a las matriculas de examenes posteriores al día de hoy y que estén pagadas y sean de la escuela
    queryset=Registration.objects.filter(exam__exam_date__gt=datetime.date.today(),exam__in=SchoolExam.objects.all(),paid=True)

class SchoolRegistrationCreateView(RegistrationCreateView):
    form_class = SchoolRegistrationForm
    template_name='cambridge/school_registration_form.html'
    def get(self, request, *args, **kwargs):
        #Comprobamos el password
        if 'school_password' in kwargs:
            school = School.objects.get(name=kwargs['school_name'])
            print "Comprobamos el password",school.password,kwargs['school_password']
            if school.password == kwargs['school_password']:
                return super(SchoolRegistrationCreateView, self).get(request, *args, **kwargs)
            else:
                return redirect('/cambridge/')
        else:
            return redirect('/cambridge/')
    def get_form_kwargs(self):
        kwargs = super(SchoolRegistrationCreateView, self).get_form_kwargs()
        #recogemos y añadimos kwargs a la form
        kwargs['school_name'] = self.kwargs['school_name']
        return kwargs
    #Añadimos el school_name al contexto
    def get_context_data(self, **kwargs):
        context = super(SchoolRegistrationCreateView, self).get_context_data(**kwargs)
        context['school_name'] = self.kwargs['school_name']
        context['school'] = School.objects.get(name=self.kwargs['school_name'])
        return context


class IndexExamList(ListView):
    model=Exam
    template_name='cambridge/index.html'
    def get_context_data(self, **kwargs):
        context = super(IndexExamList, self).get_context_data(**kwargs)
        context.update({
        'examenes_pb' : Exam.objects.filter(registration_end_date__gte=datetime.date.today()).filter(exam_type=1).filter(schoolexam__isnull=True),
        'examenes_cb' : Exam.objects.filter(registration_end_date__gte=datetime.date.today()).filter(exam_type=2).filter(schoolexam__isnull=True),
        'examenes_fs_pb' : Exam.objects.filter(registration_end_date__gte=datetime.date.today()).filter(exam_type=3).filter(schoolexam__isnull=True),
        'examenes_fs_cb' : Exam.objects.filter(registration_end_date__gte=datetime.date.today()).filter(exam_type=4).filter(schoolexam__isnull=True)
        })
        return context
             
        #return render_to_response('cambridge/index.html',{'examenes_pb': examenes_pb, 'examenes_cb': examenes_cb,'examenes_fs': examenes_fs})
    
##Venues
class VenueExamList(ListView):
    queryset=VenueExam.objects.filter(exam_date__gt=datetime.date.today())
    template_name='cambridge/venue_exam_list.html'

class VenueExamCreate(CreateView):
    model = VenueExam
    success_url="/cambridge/venue/exam/list/"
    template_name = "cambridge/venue_exam_form.html"
    form_class = VenueExamForm

class VenueListView(ListView):
	model = Venue

class VenueRegistrationListView(ListView):
    template_name='cambridge/venue_registration_list.html'
    #Limitamos a las matriculas de examenes posteriores al día de hoy y que estén pagadas y sean de la escuela
    queryset=Registration.objects.filter(exam__exam_date__gt=datetime.date.today(),exam__in=VenueExam.objects.all(),paid=True)

class VenueRegistrationCreateView(RegistrationCreateView):
    form_class = VenueRegistrationForm
    template_name='cambridge/venue_registration_form.html'
    #~ def get(self, request, *args, **kwargs):
        #~ #Comprobamos el password
        #~ if 'school_password' in kwargs:
            #~ school = School.objects.get(name=kwargs['school_name'])
            #~ print "Comprobamos el password",school.password,kwargs['school_password']
            #~ if school.password == kwargs['school_password']:
                #~ return super(SchoolRegistrationCreateView, self).get(request, *args, **kwargs)
            #~ else:
                #~ return redirect('/cambridge/')
        #~ else:
            #~ return redirect('/cambridge/')
    def get_form_kwargs(self):
        kwargs = super(VenueRegistrationCreateView, self).get_form_kwargs()
        #recogemos y añadimos kwargs a la form
        kwargs['venue_name'] = self.kwargs['venue_name']
        return kwargs
    #Añadimos el school_name al contexto
    def get_context_data(self, **kwargs):
        context = super(VenueRegistrationCreateView, self).get_context_data(**kwargs)
        context['venue_name'] = self.kwargs['venue_name']
        context['venue'] = Venue.objects.get(name=self.kwargs['venue_name'])
        return context

class LinguaskillRegistrationCreateView(RegistrationCreateView):
    model = LinguaskillRegistration
    form_class = LinguaskillRegistrationForm
    template_name='cambridge/linguaskill_registration_form.html'
    
    #def get_form_kwargs(self):
    #    kwargs = super(VenueRegistrationCreateView, self).get_form_kwargs()
    #    #recogemos y añadimos kwargs a la form
    #    kwargs['venue_name'] = self.kwargs['venue_name']
    #    return kwargs
    #Añadimos el school_name al contexto
    #def get_context_data(self, **kwargs):
    #    context = super(VenueRegistrationCreateView, self).get_context_data(**kwargs)
    #    context['venue_name'] = self.kwargs['venue_name']
    #    context['venue'] = Venue.objects.get(name=self.kwargs['venue_name'])
    #    return context
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.postal_code = '48980'
        self.object.sex = 0
        self.object.save()
        return super(LinguaskillRegistrationCreateView, self).form_valid(form)
        #return HttpResponseRedirect(self.get_success_url())

class LinguaskillRegistrationListView(ListView):
    template_name='cambridge/linguaskill_registration_list.html'
    #Limitamos a las matriculas de examenes linguaskill y que estén pagadas 
    queryset=Registration.objects.filter(exam__exam_type=5,paid=True)
