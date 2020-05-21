# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.core.mail import EmailMultiAlternatives, mail_admins
from django.conf import settings
from django.db import models

SEXO = (
    (1, _('Male')),
    (2, _('Female')),
)

CENTROS = (
    (1,"Santurce"),
    (2,"Kabiezes"),
    (3,"Sestao"),
)

class MatriculaEide(models.Model):
    centro = models.DecimalField(_('Centro'),max_digits=1, decimal_places=0,choices=CENTROS)
    nombre = models.CharField(_('Nombre'),max_length=50)
    apellido1 = models.CharField(_('Primer Apellido'),max_length=100)
    apellido2 = models.CharField(_('Segundo Apellido'),max_length=100,default='',blank=True)
    direccion = models.CharField(_('Dirección'),max_length=100)
    email = models.EmailField("Dirección de correo-e")
    email2 = models.EmailField("Segundo e-mail",help_text="Otra cuenta de correo-e (opcional)",default="",blank=True)
    localidad = models.CharField(_('Localidad'),max_length=100)
    codigo_postal = models.DecimalField(_('Código Postal'),max_digits=6, decimal_places=0)
    fecha_nacimiento = models.DateField(_('Fecha Nacimiento del alumno'), 
        help_text=_('Formato: DD-MM-AAAA(dia-mes-año)'))
    telefono1 = models.CharField(_('Teléfono Móvil de contacto'),max_length=12)
    telefono2 = models.CharField(_('Segundo Teléfono Contacto'),max_length=12,default='',blank=True)
    
    fecha_matricula = models.DateTimeField(auto_now_add=True)
    pagada = models.BooleanField(_('Pagada'),default=False)
    gestionada = models.BooleanField(_('Pagada'),default=False)
    
    nivel_ingles = models.CharField(_('Estudios previos de ingles'),help_text="¿Ha ido antes a una academia? ¿Puedes decirnos el libro que utiliza/utilizaba?",max_length=150,default="",blank=True)
    titulo_ingles = models.CharField(_('Títulación previa'),help_text="¿Tiene alguna titulación de inglés? ¿Cuál? ¿Cuándo la obtuvo?",max_length=150,default="",blank=True)
    clases_previas = models.CharField(_('Estudios previos de ingles'),max_length=150,default="",blank=True)
    
    accepta_condiciones = models.BooleanField(_('Acepto las condiciones'),
        help_text=_('''Doy mi consentimiento expreso para recibir comunicaciones en 
        los términos anteriormente descritos.'''))

    def send_confirmation_email(self):
        ##Para el alumno
        subject = _("Te has matriculadoen EIDE")
        
        html_content = ""
        
        message_body = html_content
        ##send_mail(subject, message_body, settings.DEFAULT_FROM_EMAIL, [self.email])
        msg = EmailMultiAlternatives(subject, message_body, settings.DEFAULT_FROM_EMAIL, [self.email])
        msg.attach_alternative(html_content, "text/html")
        ##msg.content_subtype = "html"
        #msg.send()
         
        ### Para los admins
        subject = "Hay una nueva matricula (sin pagar) para EIDE"
        message_body = u"""Se ha dado de alta una nueva matricula para EIDE. 
Los datos son del alumno son: 
    Nombre: %s
    Apellidos: %s
    Telefono: %s
    e-mail: %s
"""%(self.nombre,self.apellido1,self.telefono1,self.email)
        mail_admins(subject, message_body)
    def send_paiment_confirmation_email(self):
        subject = "Se ha confirmado el pago de la matricula para EIDE %s"%self.centro
        html_content=u""""""%(self.exam)
        message_body = html_content
        ##send_mail(subject, message_body, settings.DEFAULT_FROM_EMAIL, [self.email])
        #msg = EmailMultiAlternatives(subject, message_body, settings.DEFAULT_FROM_EMAIL, [self.email])
        #msg.attach_alternative(html_content, "text/html")
        ##msg.content_subtype = "html"
        #msg.send()
        send_mail(subject, message_body, settings.DEFAULT_FROM_EMAIL,[self.email], html_message=message_body)
        
        subject = "[EIDE] Se ha confirmado el pago de una matrcicula"
        message_body = u"""Se acaba de confirmar el pago de un matricula para EIDE  %s. \n 
Los datos son:\n
ID de la mátricula: %s \n 
Nombre: %s \n Apellidos: %s %s\n
Puedes ver más detalles e imprimirla en la siguente url https://gestion.eide.es/matriculas/eide/
"""%(self.centro,self.id,self.nombre,self.apellido1,self.apellido2)
        mail_admins(subject, message_body, html_message=message_body)
    
    def set_as_paid(self):
        self.paid = True
        self.save()
        self.send_paiment_confirmation_email()
        
    def __unicode__(self):
        return "%s-%s %s,%s"%(self.id,self.apellido1,self.apellido2,self.nombre)

    def save(self, *args, **kwargs):
        ##We generate a random password
        if self.id is not None:
            if self.paid:
                self.send_paiment_confirmation_email()      
        else:
            pass
            #We send a confirmation mail to te registrant and a advise mail to the admins
            self.send_confirmation_email()
        super(MatriculaEide, self).save(*args, **kwargs)
        
    def generate_payment_url(self):
        return '/pagos/eide/%s/'%(self.id)

