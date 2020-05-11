# -*- coding: utf-8 -*-

from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
import hashlib
import datetime
#from django.utils.text import slugify
from django.template.defaultfilters import slugify
from cambridge.models import Registration
from django.core.mail import send_mail, mail_admins

import logging
from django.core.urlresolvers import reverse

log = logging.getLogger("MatriculaEIDE")

class Pago(models.Model):
    importe = models.DecimalField(max_digits=6, decimal_places=2)
    descripcion = models.CharField(_('Concepto'),max_length=250,blank=True)
    fecha_creacion = models.DateField(auto_now_add=True)
    fecha_pago = models.DateField(null=True,blank=True)
    def get_absolute_url(self):
        return reverse('pagosonline_manual_pagar', kwargs={'pk': self.id})
    def set_as_paid(self):
        log.debug("Vamos a marcar como pagado el pago: %s con la descripcion %s"%(self.id,self.descripcion))
        self.fecha_pago = datetime.date.today()
        log.debug("Mandamos un mail de confirmacion")
        self.send_paiment_confirmation_email()
        log.debug("Guardamos...")
        self.save()
        return True
    def send_paiment_confirmation_email(self):
        subject = "[PagosOnline] Se ha confirmado un pago manual online"
        message_body = u"""Se acaba de confirmar un pago online creado manualmente. Los datos son: \n
        \tid: %s. \n 
        \tfecha creacion: %s. \n 
        \tdescripcion: %s. \n 
        \timporte: %s. \n 
"""%(self.id,self.fecha_creacion,self.descripcion,self.importe)
        mail_admins(subject, message_body)


class payament_info:
    """El objecto donde guardamos la infor para pasarla a la vista"""
    #Estas variables las leemos de la conf
    action_url=""
    MerchantID = ""
    AcquirerBIN = ""
    TerminalID = ""
    url_ok = ""
    url_nok = ""    
    clave = ""
    #Estas no cambian entre instalaciones
    cifrado="SHA1"
    tipo_moneda="978"
    exponente="2"
    pago_soportado="SSL"
    #Estas las generamos
    amount = ""
    order_id = ""
    firma = ""
    
    def __init__(self, reference, order_id):
        if reference=="cambridge":
            r = Registration.objects.get(id=order_id)
            #La cantidad la multiplicamos por 100 para tener los 2 decimales en un numero entero
            self.amount = int(float(r.exam.level.price)*100)
            self.amount_text = "%s"%(float(r.exam.level.price))
            #generamos el order_i con la referencia, subreferencia y el ID del la matricula para luego saber cual es
            self.order_id = "%s-%s-%s"%(reference,order_id,slugify(r.registration_name()))
        elif reference == "manual":
            p = Pago.objects.get(id=order_id)
            self.amount = int(float(p.importe)*100)
            self.amount_text = "%s €"%p.importe
            self.order_id = "manual-%s"%order_id
        #Leemos de los settings
        self.MerchantID = settings.PAYMENT_INFO["MerchantID"]
        self.AcquirerBIN=settings.PAYMENT_INFO["AcquirerBIN"]
        self.TerminalID=settings.PAYMENT_INFO["TerminalID"]
        self.clave=settings.PAYMENT_INFO["clave"]
        self.action_url=settings.PAYMENT_INFO["action_url"]
        self.url_ok=settings.PAYMENT_INFO["url_ok"]
        self.url_nok=settings.PAYMENT_INFO["url_nok"]
        #calculamos el SHA1 de la operación
        texto = self.clave + self.MerchantID + self.AcquirerBIN + self.TerminalID + \
            self.order_id + str(self.amount) + self.tipo_moneda + self.exponente + \
            self.cifrado + self.url_ok + self.url_nok;        
        clave_sha1 = hashlib.sha1()
        clave_sha1.update(str(texto))
        self.firma = clave_sha1.hexdigest()

