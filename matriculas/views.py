# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.generic import TemplateView, ListView, CreateView, DeleteView, DetailView, View, UpdateView
from django.urls import reverse, reverse_lazy
from django.shortcuts import render
from django.contrib.sites.models import Site
from django.conf import settings
from django.http import Http404
from django.contrib.auth.decorators import login_required, permission_required

from sermepa.signals import payment_was_successful, payment_was_error, signature_error
from sermepa.forms import SermepaPaymentForm
from sermepa.models import SermepaIdTPV

from matriculas.models import *
from matriculas.forms import *

class MatriculaPayView(DetailView):
    #model = Matricula
    def get_object(self, queryset=None):
        if self.kwargs['type'] == "linguaskill":
            return LinguaskillRegistration.objects.get(pk=self.kwargs['pk'])
        else:
            raise Http404()
    
    context_object_name = "matricula"
    template_name = "matriculas/matricula_pagar.html"
    def get_context_data(self, **kwargs):
        context = super(MatriculaLinguaskillPayView, self).get_context_data(**kwargs)

        site = Site.objects.get_current()
        site_domain = site.domain
        merchant_parameters = {
            "Ds_Merchant_Titular": 'EIDE',
            "Ds_Merchant_MerchantData": 'linguaskill-%s'%self.object.pay_code(), # id del Pedido o Carrito, para identificarlo en el mensaje de vuelta
            "Ds_Merchant_MerchantName": settings.SERMEPA_COMERCIO,
            "Ds_Merchant_ProductDescription": 'matricula-%s'%self.object.pay_code(),
            "Ds_Merchant_Amount": int(self.object.price()*100),
            "Ds_Merchant_Terminal": settings.SERMEPA_TERMINAL,
            "Ds_Merchant_MerchantCode": settings.SERMEPA_MERCHANT_CODE,
            "Ds_Merchant_Currency": settings.SERMEPA_CURRENCY,
            "Ds_Merchant_MerchantURL":  settings.SERMEPA_URL_DATA,
            "Ds_Merchant_UrlOK": "http://%s%s" % (site_domain, reverse('matricula_linguaskill_gracias')),
            #~ "Ds_Merchant_UrlOK": "http://%s%s" % (site_domain, reverse('end')),
            "Ds_Merchant_UrlKO": "http://%s%s" % (site_domain, reverse('matricula_linguaskill_error')),
            #~ "Ds_Merchant_UrlKO": "http://%s%s" % (site_domain, reverse('end')),
            #"Ds_Merchant_Order": SermepaIdTPV.objects.new_idtpv(),
            "Ds_Merchant_TransactionType": '0',
        }
        order = SermepaIdTPV.objects.new_idtpv() #Tiene que ser un número único cada vez
        print("Tenemos la order ",order)
        merchant_parameters.update({
            "Ds_Merchant_Order": order,
            "Ds_Merchant_TransactionType": 0, #Compra puntual
        })
            
        form = SermepaPaymentForm(merchant_parameters=merchant_parameters)
        print("Tenemos el form")
        print(form.render())
        context['form'] = form
        merchant_parameters.update({"Ds_Merchant_Paymethods": 'z'})
        form_bizum = SermepaPaymentForm(merchant_parameters=merchant_parameters)
        context['form_bizum']=form_bizum
        context['precio'] = settings.PRECIO_MATRICULA
        context['debug']= settings.DEBUG

        return context

class VenueListView(ListView):
    model = Venue
    template_name = "matriculas/venue_lista.html"

class VenueCreateView(CreateView):
    model = Venue
    template_name = "matriculas/venue_nueva.html"

## EIDE

class MatriculaEideCreateView(CreateView):
    model = MatriculaEide
    template_name = "matriculas/matricula_eide_nueva.html"
    form_class = MatriculaEideForm
    
    def get_success_url(self):
        #return reverse_lazy(MatriculaEidePayView,self.object.id)
        return reverse('matricula_eide_pagar', args=[self.object.id])

class MatriculaEideUpdateView(UpdateView):
    model = MatriculaEide
    template_name = "matriculas/matricula_eide_nueva.html"
    fields = "__all__"

class MatriculaEideListView(ListView):
    model = MatriculaEide
    template_name = "matriculas/matricula_eide_lista.html"
    ordering = ['-pk']

class MatriculaEideDetailView(DetailView):
    model = MatriculaEide
    template_name = "matriculas/matricula_eide_detalle.html"

class MatriculaEidePayView(DetailView):
    model = MatriculaEide
    context_object_name = "matricula"
    template_name = "matriculas/matricula_eide_pagar.html"
    def get_context_data(self, **kwargs):
        context = super(MatriculaEidePayView, self).get_context_data(**kwargs)
        centro = Centro.objects.get(id=self.object.centro)
        precio_matricula = "%d"%centro.precio_matricula*100
        site = Site.objects.get_current()
        site_domain = site.domain
        merchant_parameters = {
            "Ds_Merchant_Titular": 'EIDE',
            "Ds_Merchant_MerchantData": 'eide-%s'%self.object.id, # id del Pedido o Carrito, para identificarlo en el mensaje de vuelta
            "Ds_Merchant_MerchantName": settings.SERMEPA_COMERCIO,
            "Ds_Merchant_ProductDescription": 'matricula-eide-%s'%self.object.id,
            "Ds_Merchant_Amount": precio_matricula,
            "Ds_Merchant_Terminal": settings.SERMEPA_TERMINAL,
            "Ds_Merchant_MerchantCode": settings.SERMEPA_MERCHANT_CODE,
            "Ds_Merchant_Currency": settings.SERMEPA_CURRENCY,
            "Ds_Merchant_MerchantURL":  settings.SERMEPA_URL_DATA,
            "Ds_Merchant_UrlOK": "http://%s%s" % (site_domain, reverse('matricula_eide_gracias')),
            #~ "Ds_Merchant_UrlOK": "http://%s%s" % (site_domain, reverse('end')),
            "Ds_Merchant_UrlKO": "http://%s%s" % (site_domain, reverse('matricula_eide_error')),
            #~ "Ds_Merchant_UrlKO": "http://%s%s" % (site_domain, reverse('end')),
            #"Ds_Merchant_Order": SermepaIdTPV.objects.new_idtpv(),
            "Ds_Merchant_TransactionType": '0',
        }
        order = SermepaIdTPV.objects.new_idtpv() #Tiene que ser un número único cada vez
        print("Tenemos la order ",order)
        merchant_parameters.update({
            "Ds_Merchant_Order": order,
            "Ds_Merchant_TransactionType": 0, #Compra puntual
        })
            
        form = SermepaPaymentForm(merchant_parameters=merchant_parameters)
        print("Tenemos el form")
        print(form.render())
        context['form'] = form
        merchant_parameters.update({"Ds_Merchant_Paymethods": 'z'})
        form_bizum = SermepaPaymentForm(merchant_parameters=merchant_parameters)
        context['form_bizum']=form_bizum
        context['precio'] = settings.PRECIO_MATRICULA
        context['debug']= settings.DEBUG

        return context
    
class MatriculaEideGracias(TemplateView):
    template_name = "matriculas/matricula_eide_gracias.html"

class MatriculaEideError(TemplateView):
    template_name = "matriculas/matricula_eide_error.html"

## CURSOS

class CursoListView(ListView):
    model = Curso
    template_name = "matriculas/curso_curso_lista.html"
    
class CursoListViewPublica(ListView):
    model = Curso
    queryset = Curso.objects.filter(activo=True)
    template_name = "matriculas/curso_curso_lista_publica.html"

class CursoCreateView(CreateView):
    model = Curso
    template_name = "matriculas/curso_curso_nuevo.html"
    fields = "__all__"
    success_url = reverse_lazy('curso_online_lista')

class MatriculaCursoListView(ListView):
    model = MatriculaCurso
    template_name = "matriculas/matricula_curso_lista.html"
    ordering = ['-pk']

class MatriculaCursoCreateView(CreateView):
    model = MatriculaCurso
    template_name = "matriculas/matricula_curso_nueva.html"
    form_class = MatriculaCursoForm
    
    def get_success_url(self):
        #return reverse_lazy(MatriculaLinguaskillPayView,self.object.id)
        return reverse('matricula_curso_online_pagar', args=[self.object.id])
    
class MatriculaCursoDirectaCreateView(CreateView):
    model = MatriculaCurso
    template_name = "matriculas/matricula_curso_nueva.html"
    form_class = MatriculaCursoForm
    
    def get_success_url(self):
        #return reverse_lazy(MatriculaLinguaskillPayView,self.object.id)
        return reverse('matricula_curso_online_pagar', args=[self.object.id])
    
    def get_context_data(self, **kwargs):
        context = super(MatriculaCursoDirectaCreateView, self).get_context_data(**kwargs)
        try:
            context['curso'] = context['form'].initial['curso']
        except:
            print("No hay curso")
            pass
        return context
    
    def get_initial(self, *args, **kwargs):
        initial = super(MatriculaCursoDirectaCreateView, self).get_initial(**kwargs)
        initial['curso'] = Curso.objects.get(id=self.kwargs.pop('curso_id'))
        return initial

    ##Pasamos el argumento del curso
    def get_form_kwargs(self):
        kwargs = super(MatriculaCursoDirectaCreateView, self).get_form_kwargs()
        ##Intentamos leer el curso (puede que no exista)
        try:
            kwargs['curso'] = Curso.objects.get(id=self.kwargs.pop('curso_id'))
        except:
            kwargs['curso'] = None
        return kwargs

class MatriculaCursoGracias(TemplateView):
    template_name = "matriculas/matricula_curso_gracias.html"

class MatriculaCursoError(TemplateView):
    template_name = "matriculas/matricula_curso_error.html"

class MatriculaCursoPayView(DetailView):
    model = MatriculaCurso
    context_object_name = "matricula"
    template_name = "matriculas/matricula_curso_pagar.html"
    def get_context_data(self, **kwargs):
        context = super(MatriculaCursoPayView, self).get_context_data(**kwargs)

        site = Site.objects.get_current()
        site_domain = site.domain
        merchant_parameters = {
            "Ds_Merchant_Titular": 'EIDE',
            "Ds_Merchant_MerchantData": 'curso-%s'%self.object.id, # id del Pedido o Carrito, para identificarlo en el mensaje de vuelta
            "Ds_Merchant_MerchantName": settings.SERMEPA_COMERCIO,
            #"Ds_Merchant_ProductDescription": '%s'%(self.object.pay_code()),
            "Ds_Merchant_ProductDescription": 'matricula-curso-%s'%(self.object.pay_code()),
            "Ds_Merchant_Amount": int(self.object.curso.price*100),
            "Ds_Merchant_Terminal": settings.SERMEPA_TERMINAL,
            "Ds_Merchant_MerchantCode": settings.SERMEPA_MERCHANT_CODE,
            "Ds_Merchant_Currency": settings.SERMEPA_CURRENCY,
            "Ds_Merchant_MerchantURL":  settings.SERMEPA_URL_DATA,
            "Ds_Merchant_UrlOK": "http://%s%s" % (site_domain, reverse('matricula_curso_online_gracias')),
            #~ "Ds_Merchant_UrlOK": "http://%s%s" % (site_domain, reverse('end')),
            "Ds_Merchant_UrlKO": "http://%s%s" % (site_domain, reverse('matricula_curso_online_error')),
            #~ "Ds_Merchant_UrlKO": "http://%s%s" % (site_domain, reverse('end')),
            #"Ds_Merchant_Order": SermepaIdTPV.objects.new_idtpv(),
            "Ds_Merchant_TransactionType": '0',
        }
        order = SermepaIdTPV.objects.new_idtpv() #Tiene que ser un número único cada vez
        
        merchant_parameters.update({
            "Ds_Merchant_Order": order,
            "Ds_Merchant_TransactionType": 0, #Compra puntual
        })
            
        form = SermepaPaymentForm(merchant_parameters=merchant_parameters)
        context['form'] = form
        context['merchant_parameters'] = merchant_parameters
        merchant_parameters.update({"Ds_Merchant_Paymethods": 'z'})
        form_bizum = SermepaPaymentForm(merchant_parameters=merchant_parameters)
        context['form_bizum']=form_bizum
        context['precio'] = self.object.curso.price
        context['debug']= settings.DEBUG

        return context

class MatriculaCursoDetailView(DetailView):
    model = MatriculaCurso
    template_name = "matriculas/matricula_curso_detalle.html"

class MatriculaCursoUpdateView(UpdateView):
    model = MatriculaCurso
    template_name = "matriculas/matricula_curso_nueva.html"
    success_url = reverse_lazy('matricula_curso_online_lista')
    fields = "__all__"

## LINGUASKILL
class MatriculaLinguaskillCreateView(CreateView):
    model = MatriculaLinguaskill
    template_name = "matriculas/matricula_linguaskill_nueva.html"
    form_class = MatriculaLinguaskillForm
    
    def get_success_url(self):
        #return reverse_lazy(MatriculaLinguaskillPayView,self.object.id)
        return reverse('matricula_linguaskill_pagar', args=[self.object.id])
    
    ##Pasamos el argumento de la venue
    def get_form_kwargs(self):
        kwargs = super(MatriculaLinguaskillCreateView, self).get_form_kwargs()
        kwargs['venue'] = self.kwargs.pop('venue')
        return kwargs

class MatriculaLinguaskillListView(ListView):
    model = MatriculaLinguaskill
    template_name = "matriculas/matricula_linguaskill_lista.html"
    ordering = ['-registration_date']

class MatriculaLinguaskillGracias(TemplateView):
    template_name = "matriculas/matricula_linguaskill_gracias.html"

class MatriculaLinguaskillError(TemplateView):
    template_name = "matriculas/matricula_linguaskill_error.html"

class MatriculaLinguaskillPayView(DetailView):
    model = MatriculaLinguaskill
    context_object_name = "matricula"
    template_name = "matriculas/matricula_eide_pagar.html"
    def get_context_data(self, **kwargs):
        context = super(MatriculaLinguaskillPayView, self).get_context_data(**kwargs)

        site = Site.objects.get_current()
        site_domain = site.domain
        merchant_parameters = {
            "Ds_Merchant_Titular": 'EIDE Lingua Skill',
            "Ds_Merchant_MerchantData": 'ls-%s'%self.object.id, # id del Pedido o Carrito, para identificarlo en el mensaje de vuelta
            "Ds_Merchant_MerchantName": settings.SERMEPA_COMERCIO,
            "Ds_Merchant_ProductDescription": '%s'%(self.object.pay_code()),
            "Ds_Merchant_Amount": int(self.object.level.price*100),
            "Ds_Merchant_Terminal": settings.SERMEPA_TERMINAL,
            "Ds_Merchant_MerchantCode": settings.SERMEPA_MERCHANT_CODE,
            "Ds_Merchant_Currency": settings.SERMEPA_CURRENCY,
            "Ds_Merchant_MerchantURL":  settings.SERMEPA_URL_DATA,
            "Ds_Merchant_UrlOK": "http://%s%s" % (site_domain, reverse('matricula_eide_gracias')),
            #~ "Ds_Merchant_UrlOK": "http://%s%s" % (site_domain, reverse('end')),
            "Ds_Merchant_UrlKO": "http://%s%s" % (site_domain, reverse('matricula_eide_error')),
            #~ "Ds_Merchant_UrlKO": "http://%s%s" % (site_domain, reverse('end')),
            #"Ds_Merchant_Order": SermepaIdTPV.objects.new_idtpv(),
            "Ds_Merchant_TransactionType": '0',
        }
        order = SermepaIdTPV.objects.new_idtpv() #Tiene que ser un número único cada vez
        print("Tenemos la order ",order)
        merchant_parameters.update({
            "Ds_Merchant_Order": order,
            "Ds_Merchant_TransactionType": 0, #Compra puntual
        })
            
        form = SermepaPaymentForm(merchant_parameters=merchant_parameters)
        print("Tenemos el form")
        print(form.render())
        context['form'] = form
        merchant_parameters.update({"Ds_Merchant_Paymethods": 'z'})
        form_bizum = SermepaPaymentForm(merchant_parameters=merchant_parameters)
        context['form_bizum']=form_bizum
        context['precio'] = self.object.level.price
        context['debug']= settings.DEBUG

        return context

class MatriculaLinguaskillUpdateView(UpdateView):

    model = MatriculaLinguaskill
    template_name = "matriculas/matricula_linguaskill_nueva.html"
    fields = "__all__"   
    success_url = reverse_lazy('matricula_linguaskill_lista')

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
        logger.debug("Tenemos la order ",order)
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
    logger.debug("Tenemos el form")
    logger.debug(form.render())
    merchant_parameters.update({"Ds_Merchant_Paymethods": 'z'})
    form_bizum = SermepaPaymentForm(merchant_parameters=merchant_parameters)
    return HttpResponse(render_to_response('cambridge/payment.html', {'form': form, 'form_bizum': form_bizum, 'debug': settings.DEBUG, 'registration': reg}))
    
    
class RegistrationCreateView(CreateView):
    model = Registration
    form_class = RegistrationForm
    template_name='cambridge/registration_form.html'
    def get_success_url(self):
        return '/cambridge/pay/%d'%self.object.id

class RegistrationExamCreateView(CreateView):
    model = Registration
    form_class = RegistrationForm
    template_name='cambridge/registration_form.html'
    def get_success_url(self):
        return '/cambridge/pay/%d'%self.object.id
    def get_initial(self):
        # Get the initial dictionary from the superclass method
        initial = super(RegistrationExamCreateView, self).get_initial()
        # Copy the dictionary so we don't accidentally change a mutable dict
        initial = initial.copy()
        initial['exam'] = self.request.GET["exam_id"]
        # etc...
        return initial

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


