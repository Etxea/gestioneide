# -*- coding: utf-8 -*-

from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render_to_response, redirect

from django.views.generic.detail import DetailView

from django.contrib.sites.models import Site

from forms import *
from models import Pago
from sermepa.forms import SermepaPaymentForm
from sermepa.models import SermepaIdTPV

import logging
log = logging.getLogger("MatriculaEIDE")

class pagos_lista(ListView):
    model = Pago
    template_name="pagosonline/pago_list.html"
    
class crear_pago_manual(CreateView):
    #model = Pago
    form_class = PagoForm
    template_name="pagosonline/pago_manual_crear.html"

class editar_pago_manual(UpdateView):
    model = Pago
    #form_class = PagoForm
    template_name="pago_manual_editar.html"
    fields = '__all__'

class borrar_pago_manual(DeleteView):
    model = Pago
    success_url ="/pagos/lista"
    #form_class = PagoForm
    template_name="pago_manual_borrar.html"

def pagar_manual(request,pago_id):
    site = Site.objects.get_current()
    site_domain = site.domain
    pago = Pago.objects.get(id=pago_id)
    merchant_parameters = {
        "Ds_Merchant_Titular": 'John Doe',
        "Ds_Merchant_MerchantData": 'man-%s' % pago.id,   # id del Pedido o Carrito, para identificarlo en el mensaje de vuelta
        "Ds_Merchant_MerchantName": settings.SERMEPA_COMERCIO,
        "Ds_Merchant_ProductDescription": 'eide-onlinepayment-%s' % pago.id,
        "Ds_Merchant_Amount": int(pago.importe * 100),
        "Ds_Merchant_Terminal": settings.SERMEPA_TERMINAL,
        "Ds_Merchant_MerchantCode": settings.SERMEPA_MERCHANT_CODE,
        "Ds_Merchant_Currency": settings.SERMEPA_CURRENCY,
        "Ds_Merchant_MerchantURL": settings.SERMEPA_URL_DATA,
        "Ds_Merchant_UrlOK": "http://%s%s" % (site_domain, reverse('pago_ok')),
        "Ds_Merchant_UrlKO": "http://%s%s" % (site_domain, reverse('pago_ko')),
        # "Ds_Merchant_Order": SermepaIdTPV.objects.new_idtpv(),
        "Ds_Merchant_TransactionType": '0',
    }

    order = SermepaIdTPV.objects.new_idtpv()  # Tiene que ser un número único cada vez
    print "Tenemos la order ", order
    merchant_parameters.update({
        "Ds_Merchant_Order": order,
        "Ds_Merchant_TransactionType": '0',
    })

    form = SermepaPaymentForm(merchant_parameters=merchant_parameters)
    print "Tenemos el form"
    print form.render()
    return render_to_response('pagosonline/pago_manual_pagar.html', context={'form': form, 'debug': settings.DEBUG, 'pago': pago})

class PagoManual(DetailView):
    template_name = "pagosonline/pago_manual_pagar.html"
    model = Pago

    def get_context_data(self, **kwargs):
        context = super(PagoManual, self).get_context_data(**kwargs)
        context['pago']=self.object
        site = Site.objects.get_current()
        site_domain = site.domain
        pago = self.object
        merchant_parameters = {
            "Ds_Merchant_Titular": 'John Doe',
            "Ds_Merchant_MerchantData": 'man-%s' % pago.id,   # id del Pedido o Carrito, para identificarlo en el mensaje de vuelta
            "Ds_Merchant_MerchantName": settings.SERMEPA_COMERCIO,
            "Ds_Merchant_ProductDescription": 'eide-onlinepayment-%s' % pago.id,
            "Ds_Merchant_Amount": int(pago.importe * 100),
            "Ds_Merchant_Terminal": settings.SERMEPA_TERMINAL,
            "Ds_Merchant_MerchantCode": settings.SERMEPA_MERCHANT_CODE,
            "Ds_Merchant_Currency": settings.SERMEPA_CURRENCY,
            "Ds_Merchant_MerchantURL": settings.SERMEPA_URL_DATA,
            "Ds_Merchant_UrlOK": "http://%s%s" % (site_domain, reverse('pago_ok')),
            "Ds_Merchant_UrlKO": "http://%s%s" % (site_domain, reverse('pago_ko')),
            # "Ds_Merchant_Order": SermepaIdTPV.objects.new_idtpv(),
            "Ds_Merchant_TransactionType": '0',
        }

        order = SermepaIdTPV.objects.new_idtpv()  # Tiene que ser un número único cada vez
        print "Tenemos la order ", order
        merchant_parameters.update({
            "Ds_Merchant_Order": order,
            "Ds_Merchant_TransactionType": '0',
        })

        form = SermepaPaymentForm(merchant_parameters=merchant_parameters)
        print "Tenemos el form"
        print form.render()
        context['form']=form
        return context



def make_payment(request, reference, order_id):
    """ Recibimos un texto de referencia, el ID de la orden y una cantidad en euros (sin decimales)"""
    return direct_to_template(request,
        template= "pagosonline/pago.html",
        extra_context={"payament_info": payament_info(reference, order_id)})

@csrf_exempt
def confirm_payment(request):
    ## FIXME habría que poner algun filtro a la confirmación del pago.
    log.debug("Recibimos una confirmación de pago")
    log.debug(request.POST)
    try:
        #Leemos el bumero de operación donde tenemo s la referencia a la matricula
        log.debug("Vamos a leer el Num_operacion para ver que vamos a confirmar")
        reference = request.POST["Num_operacion"]
        log.debug("tenemos la referencia: %s"%reference)
        registration_type = reference.split('-')[0]
        registration_id = reference.split('-')[1]
        log.debug( "tenemos una matricula de %s con el id %s"%(registration_type, registration_id))
        r = None
        #Buscamos la matricula
        if registration_type=="cambridge":
            log.debug("Es cambridge la buscamos en BBDD")
            r = Registration.objects.get(id=registration_id)
        elif registration_type=="manual":
            log.debug("Vamos a confirmar un pago manual. Lo buscamos en BBDD...")
            r = Pago.objects.get(id=registration_id)
            log.debug("Hemos encontrado el pago manual %s"%r.id)
        else:
            log.debug( "No sabemos que tipo de matricula es!" )
        #Comprobamos si tenemos una matricula
        if r:
            log.debug( "Tenemos la matricula/pago, vamos a marcalo como pagado")
            r.set_as_paid()
            log.debug( "Mostramos al TPV la pagina de pago OK")
            return direct_to_template(request,template="pago_confirmar.html")
        else:
            return direct_to_template(request,template="pago_noconfirmar.html")
    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        log.debug("No hemos sido capaces de validar el pago de la matricula ha fallado el try con la excepcion: %s %s %s"%(exc_type,exc_value,exc_traceback))
        log.debug(exc_type)
        log.debug(exc_value)
        log.debug(exc_traceback)
        return direct_to_template(request,template="pago_noconfirmar.html")

