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


from io import StringIO
from typing import Sequence
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.template.loader import render_to_string
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.views.generic import ListView, CreateView, View
from django.views.generic.detail import DetailView, SingleObjectMixin

from django.contrib.sites.models import Site

from django.conf import settings
from django.views.generic.edit import FormView, UpdateView

from sermepa.forms import SermepaPaymentForm
from sermepa.models import SermepaIdTPV

#import StringIO
#import ho.pisa as pisa
from excel_response import ExcelView
#from django_xhtml2pdf.utils import render_to_pdf_response
from cambridge.models import *
from cambridge.forms import *
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
        "Ds_Merchant_Titular": 'EIDE',
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
        #print "Tenemos la order ",order
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
    #print "Tenemos el form"
    #print form.render()
    return HttpResponse(render_to_response('cambridge/payment.html', {'form': form, 'debug': settings.DEBUG, 'registration': reg}))
    
class RegistrationCreateView(CreateView):
    model = Registration
    form_class = RegistrationForm
    template_name='cambridge/registration_form.html'
    def get_success_url(self):
        return '/cambridge/pay/%d'%self.object.id

#Matricula directa a un examen
class RegistrationExamCreateView(RegistrationCreateView):
    
    def get_form_kwargs(self):
        kwargs = super(RegistrationExamCreateView, self).get_form_kwargs()
        #recogemos y añadimos kwargs a la form
        kwargs['exam_id'] = self.kwargs['exam_id']
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super(RegistrationExamCreateView, self).get_context_data(**kwargs)
        context['exam_id'] = self.kwargs['exam_id']
        context['exam'] = Exam.objects.get(id=self.kwargs['exam_id'])
        return context
        
    def get_initial(self):
        return { 'exam': Exam.objects.get(id=self.kwargs['exam_id']) }

class RegistrationExcelView(ExcelView):
    def get_queryset(self):
        if 'exam_id' in self.kwargs:
            data = [[
            'Candidate number','First name', 'Last name',	
            'AIC required(Yes/No)','Gender','Candidate type','Preparation centre',
            'Packing code',	'Date of birth', 'Country code', 'Area code','Contact number',
            'Mobile number','Email address','ID number','Campaign code','Address line1','Address line2',
            'City','Post/Area code','Country',
            'Candidate category P1','Candidate category O1','Candidate category R1','Resit code']]

            for registration in Registration.objects.filter(paid=True, exam_id=self.kwargs['exam_id']):
                data.append([
                    '',registration.name,registration.surname,
                    '',registration.sex,'',registration.centre_name,
                    '',	registration.birth_date, 'ES', '',registration.telephone,
                    registration.telephone,registration.email,'','',registration.address,'',
                    registration.location,registration.postal_code,'Spain',
                    '','','',''
                ])
            return data
        else:
            return Registration.objects.filter(paid=True)

class RegistrationListView(ListView):
    template_name='cambridge/lista.html'
    #Limitamos a las matriculas de examenes posteriores al día de hoy y que estén pagadas
    queryset=Registration.objects.filter(exam__exam_date__gt=datetime.date.today(),paid=True).order_by('-registration_date')

class RegistrationListViewAll(ListView):
    template_name='cambridge/lista.html'
    #Limitamos a las matriculas de examenes posteriores al día de hoy y que estén pagadas
    queryset=Registration.objects.filter().order_by('-registration_date')

class RegistrationListViewExam(ListView):
    template_name='cambridge/lista.html'
    #Limitamos a las matriculas de examenes posteriores al día de hoy y que estén pagadas y del examen concreto
    def get_queryset(self):
        return Registration.objects.filter(exam=self.kwargs['exam_id'],exam__exam_date__gt=datetime.date.today(),paid=True).order_by('-registration_date')
    def get_context_data(self, **kwargs):
        context = super(RegistrationListViewExam, self).get_context_data(**kwargs)
        context['exam'] = Exam.objects.get(id=self.kwargs['exam_id'])
        return context

class ExamList(ListView):
    queryset=Exam.objects.filter(exam_date__gt=datetime.date.today())
    template_name='cambridge/exam_list.html'

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

## SCHOOLS ##
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
            #print "Comprobamos el password",school.password,kwargs['school_password']
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
    
## Venues ##
class VenueExamList(ListView):
    queryset=VenueExam.objects.filter(exam_date__gt=datetime.date.today())
    template_name='cambridge/venue_exam_list.html'

class VenueExamCreate(CreateView):
    model = VenueExam
    success_url="/cambridge/venue/exam/list/"
    template_name = "cambridge/venue_exam_form.html"
    form_class = VenueExamForm

class VenueCreate(CreateView):
    model = Venue
    success_url="/cambridge/venue/list/"
    template_name = "cambridge/venue_form.html"

class VenueListView(ListView):
    model = Venue
    template_name = 'cambridge/venue_list.html'

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
            #~ #print "Comprobamos el password",school.password,kwargs['school_password']
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

## Prep Center

class PrepCenterHomeView(LoginRequiredMixin, DetailView):
    template_name = 'cambridge/prepcenter_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super(PrepCenterHomeView, self).get_context_data(**kwargs)
        context["exam_list"] = Exam.objects.filter(registration_end_date__gte=datetime.date.today())
        return context
    

    def get_object(self):
        return get_object_or_404(PrepCenter, pk=self.request.user.prepcenter.pk)

@method_decorator(permission_required('gestioneide.prepcenter_add',raise_exception=True),name='dispatch')
class PrepCenterCreateView(CreateView):
    model = PrepCenter
    fields = '__all__'
    success_url = reverse_lazy('cambridge_prepcenters_list')

@method_decorator(permission_required('gestioneide.prepcenter_add',raise_exception=True),name='dispatch')
class PrepCenterUpdateView(UpdateView):
    model = PrepCenter
    fields = ['name', 'description', 'telephone', 'email']
    
    def get_success_url(self) -> str:
        return reverse_lazy("prepcenter_detalle",kwargs={'pk': self.object.id})

@method_decorator(permission_required('gestioneide.prepcenter_add',raise_exception=True),name='dispatch')
class PrepCenterListView(ListView):
    model = PrepCenter

@method_decorator(permission_required('gestioneide.prepcenter_add',raise_exception=True),name='dispatch')
class PrepCenterPasswordResetView(View,SingleObjectMixin):
    model = PrepCenter
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return HttpResponseRedirect(reverse_lazy("prepcenter_detalle",kwargs={'pk': self.object.id}))
    def post(self, request, *args, **kwargs):
        # Look up the author we're interested in.
        self.object = self.get_object()
        self.object.update_user_password()
        return HttpResponseRedirect(reverse_lazy("prepcenter_detalle",kwargs={'pk': self.object.id}))

@method_decorator(permission_required('gestioneide.prepcenter_add',raise_exception=True),name='dispatch')
class PrepCenterCreateUserView(View,SingleObjectMixin):
    model = PrepCenter
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return HttpResponseRedirect(reverse_lazy("prepcenter_detalle",kwargs={'pk': self.object.id}))
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.create_user()
        return HttpResponseRedirect(reverse_lazy("prepcenter_detalle",kwargs={'pk': self.object.id}))

@method_decorator(permission_required('gestioneide.prepcenter_add',raise_exception=True),name='dispatch')
class PrepCenterDisableUserView(View,SingleObjectMixin):
    model = PrepCenter
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return HttpResponseRedirect(reverse_lazy("prepcenter_detalle",kwargs={'pk': self.object.id}))
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.user.is_active = False
        self.object.user.save()
        return HttpResponseRedirect(reverse_lazy("prepcenter_detalle",kwargs={'pk': self.object.id}))

@method_decorator(permission_required('gestioneide.prepcenter_add',raise_exception=True),name='dispatch')
class PrepCenterEnableUserView(View,SingleObjectMixin):
    model = PrepCenter
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return HttpResponseRedirect(reverse_lazy("prepcenter_detalle",kwargs={'pk': self.object.id}))
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.user.is_active = True
        self.object.user.save()
        return HttpResponseRedirect(reverse_lazy("prepcenter_detalle",kwargs={'pk': self.object.id}))

@method_decorator(permission_required('gestioneide.prepcenter_add',raise_exception=True),name='dispatch')
class PrepCenterDetailView(DetailView):
    model = PrepCenter

# @method_decorator(permission_required('gestioneide.prepcenter_add',raise_exception=True),name='dispatch')
# class PrepCenterExamCreate(CreateView):
#     model = PrepCenterExam
#     fields = '__all__'
#     def get_success_url(self) -> str:
#         return reverse_lazy("prepcenter_detalle",kwargs={'pk': self.object.center.id})

class PrepCenterRegistrationCreateView(LoginRequiredMixin,CreateView):
    model = Registration
    form_class = PrepCenterRegistrationForm
    template_name = 'cambridge/prepcenter_registration_form.html'
    
    def get_success_url(self):
        return reverse_lazy('cambridge_prepcenter_home')

    def form_valid(self, form):
        print("Somos matricula prep center")
        prepcenter = self.request.user.prepcenter
        self.object = form.save()
        pcr = PrepCenterRegistration(registration=self.object,center=prepcenter)
        pcr.save()
        return super(PrepCenterRegistrationCreateView, self).form_valid(form)

# Matricula directa a un examen
class PrepCenterRegistrationExamCreateView(LoginRequiredMixin, FormView):
    model = Registration
    #form_class = PrepCenterRegistrationForm
    template_name = 'cambridge/prepcenter_registration_form.html'

    def get_success_url(self):
        return reverse_lazy('cambridge_prepcenter_home')

    def get_context_data(self, **kwargs):
        context = super(PrepCenterRegistrationExamCreateView, self).get_context_data(**kwargs)
        context['directo'] = True
        exam = Exam.objects.get(pk=self.kwargs['exam_id'])
        prepcenter = self.request.user.prepcenter
        context['exam'] = exam
        context['center'] = prepcenter
        
        # Rellenamsos los datos iniciales, idealmente el range debería ser del tamaño de extra_forms
        initial = []
        for i in range(0,2):
            initial.append({'exam': exam, 'prepcenter': prepcenter.pk})
        
        #Si es POST rellenamos con los datos
        if self.request.method == 'POST':
            formset = PrepCenterRegistrationFormSet(self.request.POST, initial=initial)
        else:
            formset = PrepCenterRegistrationFormSet(initial=initial)

        context['formset'] = formset 
        context.pop('form')
        #print(formset.management_form)
        return context

    def get_form(self, form_class=None):
        if self.request.method == 'POST':
            formset = PrepCenterRegistrationFormSet(self.request.POST)
        else:
            formset = PrepCenterRegistrationFormSet()
        return formset

    def form_valid(self, formset):
        prepcenter = self.request.user.prepcenter    
        for form in formset:
            self.object = form.save()
            # Generemos una matricula de prepcenter asociando la matricula y el centro        
            print("Generemos una matricula de prepcenter asociando la matricula y el centro",self.object,prepcenter)
            pcr = PrepCenterRegistration(registration=self.object,center=prepcenter)
            pcr.save()
        return super(PrepCenterRegistrationExamCreateView, self).form_valid(formset)        
    
    def form_invalid(self, formset):
        print("El formset no es válido")
        print(formset)
        print(formset.errors)
        return super(PrepCenterRegistrationExamCreateView, self).form_invalid(formset)


class PrepCenterRegistrationsPayView(LoginRequiredMixin,DetailView):
    model = PrepCenter
    context_object_name = "prepcenter"
    template_name = "cambridge/prepcenter_registrations_pay.html"

    def get_object(self):
        return get_object_or_404(PrepCenter, pk=self.request.user.prepcenter.pk)

    def get_context_data(self, **kwargs):
        context = super(PrepCenterRegistrationsPayView, self).get_context_data(**kwargs)
        #Fecha control para luego marcar como pagadas las matriculas anteriores a esta fecha
        now = datetime.datetime.now()
        fecha_control = "%s-%s-%s-%s-%s"%(now.year,now.month,now.day,now.hour,now.minute)
        context['fecha_control']=fecha_control
        # print("Fecha control:",fecha_control)
        #Calculamos el importe total de todas las matriculas sin pagar de este centro
        precio = 0
        lista_matriculas = self.object.registration_set.filter(registration__paid = 0)
        context['lista_matriculas'] = lista_matriculas
        for pcr in lista_matriculas:
            precio =+ pcr.registration.exam.level.price 
        context['precio'] = precio
        site = Site.objects.get_current()
        site_domain = site.domain
        merchant_parameters = {
            "Ds_Merchant_Titular": 'EIDE',
            "Ds_Merchant_MerchantData": 'prepcenter-%s-%s'%(self.object.pk,fecha_control), # id del Pedido o Carrito, para identificarlo en el mensaje de vuelta
            "Ds_Merchant_MerchantName": settings.SERMEPA_COMERCIO,
            "Ds_Merchant_ProductDescription": 'prepcenter-%s-%s'%(self.object.pk,fecha_control),
            "Ds_Merchant_Amount": int(precio*100),
            "Ds_Merchant_Terminal": settings.SERMEPA_TERMINAL,
            "Ds_Merchant_MerchantCode": settings.SERMEPA_MERCHANT_CODE,
            "Ds_Merchant_Currency": settings.SERMEPA_CURRENCY,
            "Ds_Merchant_MerchantURL":  settings.SERMEPA_URL_DATA,
            "Ds_Merchant_UrlOK": "http://%s%s" % (site_domain, reverse('cambridge_prepcenter_home')),        
            "Ds_Merchant_UrlKO": "http://%s%s" % (site_domain, reverse('cambridge_prepcenter_home')),
            "Ds_Merchant_Order": SermepaIdTPV.objects.new_idtpv(),
            "Ds_Merchant_TransactionType": '0',
        }
                    
        form = SermepaPaymentForm(merchant_parameters=merchant_parameters)
        # print("Tenemos el form")
        # print(form.render())
        context['form'] = form
        merchant_parameters.update({"Ds_Merchant_Paymethods": 'z'})
        form_bizum = SermepaPaymentForm(merchant_parameters=merchant_parameters)
        context['form_bizum']=form_bizum
        context['debug']= settings.DEBUG

        return context