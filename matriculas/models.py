# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.core.mail import mail_admins
from anymail.message import AnymailMessage
from django.conf import settings
from django.db import models
import logging
from django.core.urlresolvers import reverse_lazy

log = logging.getLogger("django")

from gestioneide.models import Alumno, Centro

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
    alumno_id = models.DecimalField(max_digits=6, decimal_places=0,blank=True,default=0)
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
    gestionada = models.BooleanField(_('Gestionada'),default=False)
    
    nivel_ingles = models.CharField(_('Nivel de ingles [opcional]'),help_text="¿Conoce su nivel de ingles (A1/2,B1-1/1-2/2-1/2-2,C1)?",max_length=150,default="",blank=True)
    titulo_ingles = models.CharField(_('Títulación previa [opcional]'),help_text="¿Tiene alguna titulación de inglés? ¿Cuál? ¿Cuándo la obtuvo?",max_length=150,default="",blank=True)
    clases_previas = models.CharField(_('Estudios previos de inglés [opcional]'),help_text="¿Ha ido antes a una academia? ¿Puede decirnos el libro que utiliza/utilizaba?",max_length=150,default="",blank=True)
    
    accepta_condiciones_imagen = models.BooleanField(_('Acepto las condiciones'),
        help_text=_('''Doy mi consentimiento expreso para que mi imagen pueda ser utilizada en la página 
        Web o en redes sociales del centro así como en todo el material publicitario que pueda utilizar, 
        en los términos anteriormente descritos'''))

    accepta_condiciones_comunicacion = models.BooleanField(_('Acepto las condiciones'),
        help_text=_('''Doy mi consentimiento expreso para recibir comunicaciones en los términos anteriormente descritos.'''))

    def send_confirmation_email(self):
        ##Para el alumno
        subject = "[EIDE][Matricula] Te has matriculado en EIDE %s" %(self.get_centro_display())
        
        message_body = """Hemos recibido su matrícula, muchas gracias. En cuanto realice el pago recibirá otro mail de confirmación. <br>
        Un saludo. <br>
        Secretaría."""
        
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
        html_content=u"""Se ha confirmado el pago de la matrícula, muchas gracias. En breve nos pondremos en contacto con usted para darle más instrucciones e indicarle cómo realizar la prueba de nivel, en caso de que sea necesario
        <br>Un saludo.
        <br>Secretaría."""
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

        subject = "[GESTIONEIDE][Matricula] Se ha confirmado el pago de una matrcicula"
        message_body = u"""Se acaba de confirmar el pago de un matricula para EIDE  %s. \n 
        Los datos son:\n
        ID de la mátricula: %s \n 
        Nombre: %s \n Apellidos: %s %s\n
        Puedes ver más detalles e imprimirla en la siguente url https://gestion.eide.es/matriculas/eide/lista/
        """%(self.get_centro_display(),self.id,self.nombre,self.apellido1,self.apellido2)

        centro = Centro.objects.get(id=self.centro)
        email_secretaria = AnymailMessage(
            subject=subject,
            body=message_body,
            to = [centro.email],
        )
        email.content_subtype = "html"
        try:
            email.send(fail_silently=False)
        except Exception, e:
            log.error("(matriculas) Error al enviar mail",str(e))
    
    def set_as_paid(self):
        self.pagada = True
        self.save()
        self.send_paiment_confirmation_email()
        self.generate_alumno()

    def generate_alumno(self):
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
            self.alumno_id = a.id
            #self.gestionada=True
            self.save()
            texto = """Se ha creado el alumno %s de la matricula %s . <br />
                Puedes ver los detalles del alumno en: https://gestion.eide.es%s <br />
                Puedes ver los detalles de la matricula en : https://gestion.eide.es%s
                """%(a.id,self.id,a.get_absolute_url(),self.get_absolute_url())
            mail_admins("[GESTIONEIDE] Alumno %s creado via m"%(a.id), texto )
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
        return '/matriculas/eide/pagar/%s/'%(self.id)

    def get_absolute_url(self):
        return reverse_lazy('matricula_eide_editar', kwargs={'pk': self.pk })

