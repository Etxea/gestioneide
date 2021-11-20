# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.generic import TemplateView, ListView, CreateView, DeleteView, DetailView, View, UpdateView
from django.urls import reverse, reverse_lazy
from django.shortcuts import render
from django.contrib.sites.models import Site
from django.conf import settings
from django.http import Http404
from django.contrib.auth.decorators import login_required, permission_required

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
            "Ds_Merchant_MerchantData": 'matricula-%s'%self.object.pay_code(), # id del Pedido o Carrito, para identificarlo en el mensaje de vuelta
            "Ds_Merchant_MerchantName": settings.SERMEPA_COMERCIO,
            #"Ds_Merchant_ProductDescription": 'matricula-%s'%self.object.pay_code(),
            "Ds_Merchant_ProductDescription": '%s'%(self.object.pay_code()),
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
        print("Somos MatriculaPayView y Tenemos la order ",order)
        merchant_parameters.update({
            "Ds_Merchant_Order": order,
            "Ds_Merchant_TransactionType": 0, #Compra puntual
        })
            
        form = SermepaPaymentForm(merchant_parameters=merchant_parameters)
        print("Somos MatriculaPayView y Tenemos el form")
        print(form.render())
        context['form'] = form
        merchant_parameters.update({"Ds_Merchant_Paymethods": 'z'})
        form_bizum = SermepaPaymentForm(merchant_parameters=merchant_parameters)
        context['form_bizum']=form_bizum
        context['precio'] = settings.PRECIO_MATRICULA
        context['debug']= settings.DEBUG

        return context

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
        precio_matricula = "%d"%int(float(centro.precio_matricula)*100)
        site = Site.objects.get_current()
        site_domain = site.domain
        merchant_parameters = {
            "Ds_Merchant_Titular": 'EIDE',
            "Ds_Merchant_MerchantData": 'eide-%s'%self.object.id, # id del Pedido o Carrito, para identificarlo en el mensaje de vuelta
            "Ds_Merchant_MerchantName": settings.SERMEPA_COMERCIO,
            #"Ds_Merchant_ProductDescription": 'matricula-eide-%s'%self.object.id,
            "Ds_Merchant_ProductDescription": '%s'%(self.object.pay_code()),
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
        #print("Somo MatriculaEidePayView Tenemos la order ",order)
        merchant_parameters.update({
            "Ds_Merchant_Order": order,
            "Ds_Merchant_TransactionType": 0, #Compra puntual
        })
            
        form = SermepaPaymentForm(merchant_parameters=merchant_parameters)
        #print("Somo MatriculaEidePayView Tenemos la form ",form)
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
        initial['curso'] = Curso.objects.get(id=self.kwargs.pop('curso_online_id'))
        return initial

    ##Pasamos el argumento del curso
    def get_form_kwargs(self):
        kwargs = super(MatriculaCursoDirectaCreateView, self).get_form_kwargs()
        ##Intentamos leer el curso (puede que no exista)
        try:
            kwargs['curso'] = Curso.objects.get(id=self.kwargs.pop('curso_online_id'))
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
    #def get_form(self):
    #    self.form_class = MatriculaLinguaskillForm
    #    form = super(MatriculaLinguaskillCreateView, self).get_form(self.form_class)
    #    form.fields['level'].queryset = LinguaskillLevel.objects.filter(venue=Venue.objects.filter(name=venue_name))
    #    return form

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
            "Ds_Merchant_Titular": 'EIDE',
            "Ds_Merchant_MerchantData": 'ls-%s'%self.object.id, # id del Pedido o Carrito, para identificarlo en el mensaje de vuelta
            "Ds_Merchant_MerchantName": settings.SERMEPA_COMERCIO,
            "Ds_Merchant_ProductDescription": '%s'%(self.object.pay_code()),
            "Ds_Merchant_Amount": int(self.object.level.price*100),
            "Ds_Merchant_Terminal": settings.SERMEPA_TERMINAL,
            "Ds_Merchant_MerchantCode": settings.SERMEPA_MERCHANT_CODE,
            "Ds_Merchant_Currency": settings.SERMEPA_CURRENCY,
            "Ds_Merchant_MerchantURL":  settings.SERMEPA_URL_DATA,
            "Ds_Merchant_UrlOK": "http://%s%s" % (site_domain, reverse('matricula_linguaskill_gracias')),        
            "Ds_Merchant_UrlKO": "http://%s%s" % (site_domain, reverse('matricula_linguaskill_error')),
            "Ds_Merchant_Order": SermepaIdTPV.objects.new_idtpv(),
            "Ds_Merchant_TransactionType": '0',
        }
                    
        form = SermepaPaymentForm(merchant_parameters=merchant_parameters)
        print("Tenemos el form")
        print(form.render())
        context['form'] = form
        merchant_parameters.update({"Ds_Merchant_Paymethods": 'z'})
        #form_bizum = SermepaPaymentForm(merchant_parameters=merchant_parameters)
        #context['form_bizum']=form_bizum
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
    

