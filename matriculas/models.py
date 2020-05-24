# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.core.mail import mail_admins
from anymail.message import AnymailMessage
from django.conf import settings
from django.db import models

import logging
log = logging.getLogger("django")

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
    email = models.EmailField("E-mail principal",help_text="Cuenta de correo principal, recibirá confirmación de esta matrícula")
    email2 = models.EmailField("Segundo e-mail",help_text="Otra cuenta de correo-e (opcional)",default="",blank=True)
    localidad = models.CharField(_('Localidad'),max_length=100)
    codigo_postal = models.DecimalField(_('Código Postal'),max_digits=6, decimal_places=0)
    fecha_nacimiento = models.DateField(_('Fecha Nacimiento del alumno'), 
        help_text=_('Formato: DD\MM\AAAA(día\mes\año)'))
    telefono1 = models.CharField(_('Teléfono Móvil de contacto'),max_length=12)
    telefono2 = models.CharField(_('Segundo Teléfono Contacto'),max_length=12,default='',blank=True)
    
    fecha_matricula = models.DateTimeField(auto_now_add=True)
    pagada = models.BooleanField(_('Pagada'),default=False)
    gestionada = models.BooleanField(_('Pagada'),default=False)
    
    nivel_ingles = models.CharField(_('Nivel de ingles [opcional]'),help_text="¿Conoce su nivel de ingles (A1/2,B1-1/1-2/2-1/2-2,C1)?",max_length=150,default="",blank=True)
    titulo_ingles = models.CharField(_('Títulación previa [opcional]'),help_text="¿Tiene alguna titulación de inglés? ¿Cuál? ¿Cuándo la obtuvo?",max_length=150,default="",blank=True)
    clases_previas = models.CharField(_('Estudios previos de ingles [opcional]'),help_text="¿Ha ido antes a una academia? ¿Puedes decirnos el libro que utiliza/utilizaba?",max_length=150,default="",blank=True)
    
    accepta_condiciones = models.BooleanField(_('Acepto las condiciones'),
        help_text=_('''Doy mi consentimiento expreso para recibir comunicaciones en 
        los términos anteriormente descritos.'''))

    def send_confirmation_email(self):
        ##Para el alumno
        subject = "[EIDE][Matricula] Te has matriculado en EIDE %s" %(self.get_centro_display())
        
        message_body = "Buenas,<br>Hemos recibido tu matrícula, cuando se confirme el pago recibirás un segundo e-mail.<br>Un saludo."
        
        email = AnymailMessage(
            subject=subject,
            body=message_body,
            to = [self.email],
        )
        email.content_subtype = "html"
        try:
            email.send(fail_silently=False)
        except Exception, e:
            log.error("(matriculas) Error al enviar mail",str(e))
        
         
        ### Para los admins
        subject = "[GESTIONEIDE][Matricula] Hay una nueva matricula (sin pagar) para EIDE %s"%(self.get_centro_display())
        message_body = u"""Se ha dado de alta una nueva matricula para EIDE. 
        Los datos son del alumno son: 
            Nombre: %s
            Apellidos: %s
            Telefono: %s
            e-mail: %s
        """%(self.nombre,self.apellido1,self.telefono1,self.email)
        mail_admins(subject, message_body)
    
    def send_paiment_confirmation_email(self):
        subject = "[EIDE][Matricula] Se ha confirmado el pago de la matricula para EIDE %s"%self.get_centro_display()
        html_content=u"""Hola,<br>Se ha confirmado el pago para el centro %s de EIDE.
        <br>En breve se pondrán en contacto contigo para ultimar los detalles.
        <br>Un saludo."""%(self.get_centro_display())
        message_body = html_content
        
        email = AnymailMessage(
            subject=subject,
            body=message_body,
            to = [self.email],
        )
        email.content_subtype = "html"
        try:
            email.send(fail_silently=False)
        except Exception, e:
            log.error("(matriculas) Error al enviar mail",str(e))    
        
        subject = "[GESTIONEIDE][Matricula] Se ha confirmado el pago de una matrcicula"
        message_body = u"""Se acaba de confirmar el pago de un matricula para EIDE  %s. \n 
        Los datos son:\n
        ID de la mátricula: %s \n 
        Nombre: %s \n Apellidos: %s %s\n
        Puedes ver más detalles e imprimirla en la siguente url https://gestion.eide.es/matriculas/eide/lista/
        """%(self.get_centro_display(),self.id,self.nombre,self.apellido1,self.apellido2)
        mail_admins(subject, message_body, html_message=message_body)
    
    def set_as_paid(self):
        self.pagada = True
        self.save()
        self.send_paiment_confirmation_email()
        self.generate_alumno()

    def generate_alumno(self):
        from gestioneide.models import Alumno
        a = Alumno(
            nombre = self.nombre,
            apellido1 = self.apellido1,
            apellido2 = self.apellido2,
            fecha_nacimiento = self.fecha_nacimiento,
            telefono1 = self.telefono1,
            telefono2 = self.telefono2,
            email = self.email,
            email2 = self.email2,
            direccion = self.direccion,
            ciudad = self.localidad,
            cp = self.codigo_postal,
            observaciones = "Matricula Online %s para el centro %s"%(self.id,self.get_centro_display()),
        )
        try:
            a.save()
            self.gestionada=True
            self.save()
            mail_admins(
                "[GESTIONEIDE] Alumno %s creado"%(a.id), 
                "Se ha creado el alumno %s de la matricula %s . Puedes ver los detalles en: https://gestion.eide.es%s"%(a.id,self.id,a.get_absolute_url()))
        except Exception, e:
            log.error("(matriculas) Error al generar el alumno ",str(e)) 
    def __unicode__(self):
        return "%s-%s %s,%s"%(self.id,self.apellido1,self.apellido2,self.nombre)

    def save(self, *args, **kwargs):
        ##We generate a random password
        if self.id is not None:
            if self.pagada:
                self.send_paiment_confirmation_email()      
        else:
            self.send_confirmation_email()
        super(MatriculaEide, self).save(*args, **kwargs)
        
    def generate_payment_url(self):
        return '/pagos/eide/%s/'%(self.id)

