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

    def pay_code(self):
        return "eide-%s"%self.id

    def price(self):
        return settings.PRECIO_MATRICULA

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

## CAMBRIDGE ##

class Venue(models.Model):
    name = models.CharField(_('Name'),max_length=50)
    description = models.CharField(_('Description'),max_length=100,default="")
    password = models.CharField(_('Password'),max_length=50)
    def __unicode__(self):
        return self.name
    def exam_count(self):
        return self.venueexam_set.all().count()
    def registration_count(self):
        total=0
        for e in self.venueexam_set.all():
            total = total + e.registration_set.all().count()
        return total

## LINGUASKILL

class LinguaskillLevel(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    venue = models.ForeignKey(Venue)

    def __unicode__(self):
        return "[LS][%s]%s(%s)"%(self.venue,self.name,self.price)

class MatriculaLinguaskill(models.Model):
    proposed_date  = models.DateField(_('Fecha propuesta DD-MM-AAAA'), help_text=_('Formato: DD-MM-AAAA(dia-mes-año)'))
    level = models.ForeignKey(LinguaskillLevel)
    password = models.CharField(_('Password'),max_length=6,blank=True,editable=False)
    name = models.CharField(_('Nombre'),max_length=50)
    surname = models.CharField(_('Apellido(s)'),max_length=100)
    address = models.CharField(_('Dirección'),max_length=100)
    location = models.CharField(_('Localidad'),max_length=100)
    postal_code = models.DecimalField(_('Código Postal'),max_digits=6, decimal_places=0)
    sex = models.DecimalField(_('Sexo'),max_digits=1, decimal_places=0,choices=SEXO)
    birth_date = models.DateField(_('Fecha Nacm. DD-MM-AAAA'), help_text=_('Formato: DD-MM-AAAA(dia-mes-año)'))
    telephone = models.CharField(_('Teléfono'),max_length=12)
    email = models.EmailField()
    registration_date = models.DateField(auto_now_add=True)
    paid = models.BooleanField(_('Pagada'),default=False)
    accept_conditions = models.BooleanField(_('Doy mi consentimiento expreso para recibir comunicaciones en los términos anteriormente descritos.'), help_text=_('Doy mi consentimiento expreso para recibir comunicaciones en los términos anteriormente descritos.'),default=False,blank=True)

    def pay_code(self):
        return "linguaskill-%s"%self.id    
    
    def price(self):
        return self.level.price

    def send_confirmation_email(self):
        ##Para el alumno
        subject = _("Te has matriculado para un examen Cambridge en EIDE")
        
        html_content = u"""
        


<div class="well">
    Acaba de realizar una solicitud de matrícula para: <br />
    %s 
</div>
<div class="well">
    <h1>Pago de la matrícula</h1>
    La matrícula se hará efectiva una vez se haya recibido el pago. Puede hacer el pago en la siguiente dirección: <a href="http://matricula-eide.es/%s">http://matricula-eide.es/%s</a>
</div>"""%(self.exam,self.generate_payment_url(),self.generate_payment_url())
        
        message_body = html_content
        ##send_mail(subject, message_body, settings.DEFAULT_FROM_EMAIL, [self.email])
        msg = EmailMultiAlternatives(subject, message_body, settings.DEFAULT_FROM_EMAIL, [self.email])
        msg.attach_alternative(html_content, "text/html")
        ##msg.content_subtype = "html"
        #msg.send()
         
        ### Para los admins
        subject = "Hay una nueva matricula (sin pagar) para cambridge %s"%self.exam
        message_body = u"""Se ha dado de alta una nueva matricula para el examen %s. 
Los datos son del alumno son: 
    Nombre: %s
    Apellidos: %s
    Telefono: %s
    e-mail: %s
"""%(self.exam,self.name,self.surname,self.telephone,self.email)
        mail_admins(subject, message_body)
    
    def send_paiment_confirmation_email(self):
        try:
            ls = MatriculaLinguaskill.objects.get(id=self.id)
            exam_date=ls.proposed_date
        except:
            exam_date=self.exam.exam_date
        subject = "Se ha confirmado el pago de la matricula para el examen %s"%self.exam
        html_content=u"""<html><body>
        <h2>CONFIRMACIÓN DE MATRÍCULA</h2>
<p>Se ha matriculado para el examen <b> %s </b>. Tras el cierre del periodo de matriculación se le enviará el COE (Confirmation of Entry) 
con las fechas y horas del examen escrito y oral a la dirección de e-mail que ha proporcionado el candidato en la 
hoja de matrícula. Si dos semanas antes de la fecha del examen el candidato no ha recibido el COE, es su responsabilidad 
el ponerse en contacto con EIDE y solicitar el COE. EIDE no se responsabiliza del extravío o no recepción del mismo y no 
asume ninguna responsabilidad por cualquier problema derivado del desconocimiento de la fecha, horario y lugar del examen 
y se reserva el derecho de no admitir a candidatos que lleguen tarde.</p>

<p>Es responsabilidad del candidato llegar al lugar del examen con 15 minutos de antelación. Los candidatos deben traer un 
DNI o pasaporte que atestigüe su identidad en cada examen (escrito y oral).</p>
        """%(self.exam)
	#html_content= html_content+render_to_string('cambridge/legal.html')
        html_content= html_content+u"""</body></html>"""
        message_body = html_content
        ##send_mail(subject, message_body, settings.DEFAULT_FROM_EMAIL, [self.email])
        #msg = EmailMultiAlternatives(subject, message_body, settings.DEFAULT_FROM_EMAIL, [self.email])
        #msg.attach_alternative(html_content, "text/html")
        ##msg.content_subtype = "html"
        #msg.send()
        send_mail(subject, message_body, settings.DEFAULT_FROM_EMAIL,[self.email], html_message=message_body)
        
        subject = "[cambridge] Se ha confirmado el pago de una matrcicula"
        message_body = u"""Se acaba de confirmar el pago de un matricula para examen %s. \n 
Los datos son:\n
ID de la mátricula: %s \n 
Nombre: %s \n Apellidos: %s \n
Puedes ver más detalles e imprimirla en la siguente url http://matricula-eide.es/cambridge/edit/%s/
"""%(self.exam,self.id,self.name,self.surname,self.id)
        mail_admins(subject, message_body, html_message=message_body)
    
    def set_as_paid(self):
        self.paid = True
        self.save()
        self.send_paiment_confirmation_email()
        
    def __unicode__(self):
        return "%s-%s"%(self.id,self.exam)
    
    def save(self, *args, **kwargs):
        
        if self.id is not None:
            if self.paid:
                self.send_paiment_confirmation_email()      
        else:
            #We set a random password, not used right now
            self.password = ''.join([choice(letters) for i in xrange(6)])
            #We send a confirmation mail to te registrant and a advise mail to the admins
            self.send_confirmation_email()
        super(MatriculaLinguaskill, self).save(*args, **kwargs)
            
    def generate_payment_url(self):
        return '/pagos/cambridge/%s/'%(self.id)
        return '/matriculas/eide/pagar/%s/'%(self.id)
