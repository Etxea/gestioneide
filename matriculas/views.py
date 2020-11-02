# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.generic import TemplateView, ListView, CreateView, DeleteView, DetailView, View, UpdateView
from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import render
from django.contrib.sites.models import Site
from django.conf import settings
from django.http import Http404

from sermepa.signals import payment_was_successful, payment_was_error, signature_error
from sermepa.forms import SermepaPaymentForm
from sermepa.models import SermepaIdTPV

from models import *
from forms import *

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
            "Ds_Merchant_Titular": 'John Doe',
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
        print "Tenemos la order ",order
        merchant_parameters.update({
            "Ds_Merchant_Order": order,
            "Ds_Merchant_TransactionType": 0, #Compra puntual
        })
            
        form = SermepaPaymentForm(merchant_parameters=merchant_parameters)
        print "Tenemos el form"
        print form.render()
        context['form'] = form
        context['precio'] = settings.PRECIO_MATRICULA
        context['debug']= settings.DEBUG

        return context

class VenueListView(ListView):
    model = Venue
    template_name = "matriculas/venue_lista.html"

class VenueCreateView(CreateView):
    model = Venue
    template_name = "matriculas/venue_nueva.html"

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

class MatriculaEideDetailView(DetailView):
    model = MatriculaEide
    template_name = "matriculas/matricula_eide_detalle.html"

class MatriculaEidePayView(DetailView):
    model = MatriculaEide
    context_object_name = "matricula"
    template_name = "matriculas/matricula_eide_pagar.html"
    def get_context_data(self, **kwargs):
        context = super(MatriculaEidePayView, self).get_context_data(**kwargs)

        site = Site.objects.get_current()
        site_domain = site.domain
        merchant_parameters = {
            "Ds_Merchant_Titular": 'EIDE',
            "Ds_Merchant_MerchantData": 'eide-%s'%self.object.id, # id del Pedido o Carrito, para identificarlo en el mensaje de vuelta
            "Ds_Merchant_MerchantName": settings.SERMEPA_COMERCIO,
            "Ds_Merchant_ProductDescription": 'matricula-eide-%s'%self.object.id,
            "Ds_Merchant_Amount": int(settings.PRECIO_MATRICULA*100),
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
        print "Tenemos la order ",order
        merchant_parameters.update({
            "Ds_Merchant_Order": order,
            "Ds_Merchant_TransactionType": 0, #Compra puntual
        })
            
        form = SermepaPaymentForm(merchant_parameters=merchant_parameters)
        print "Tenemos el form"
        print form.render()
        context['form'] = form
        context['precio'] = settings.PRECIO_MATRICULA
        context['debug']= settings.DEBUG

        return context
    
class MatriculaEideGracias(TemplateView):
    template_name = "matriculas/matricula_eide_gracias.html"

class MatriculaEideError(TemplateView):
    template_name = "matriculas/matricula_eide_error.html"

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
        print "Tenemos la order ",order
        merchant_parameters.update({
            "Ds_Merchant_Order": order,
            "Ds_Merchant_TransactionType": 0, #Compra puntual
        })
            
        form = SermepaPaymentForm(merchant_parameters=merchant_parameters)
        print "Tenemos el form"
        print form.render()
        context['form'] = form
        context['precio'] = self.object.level.price
        context['debug']= settings.DEBUG

        return context