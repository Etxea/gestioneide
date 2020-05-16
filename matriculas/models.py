# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _

from django.db import models

SEXO = (
    (1, _('Male')),
    (2, _('Female')),
)


class MatriculaEide(models.Model):
    
    name = models.CharField(_('Nombre'),max_length=50)
    surname = models.CharField(_('Apellido(s)'),max_length=100)
    address = models.CharField(_('Dirección'),max_length=100)
    location = models.CharField(_('Localidad'),max_length=100)
    postal_code = models.DecimalField(_('Código Postal'),max_digits=6, decimal_places=0)
    sex = models.DecimalField(_('Sexo'),max_digits=1, decimal_places=0,choices=SEXO)
    birth_date = models.DateField(_('Fecha Nacm. DD-MM-AAAA'), help_text=_('Formato: DD-MM-AAAA(dia-mes-año)'))
    #dni = models.CharField(max_length=9,blank=True,help_text=_('Introduce el DNI completo con la letra sin espacios ni guiones'))
    telephone1 = models.CharField(_('Teléfono Móvil'),max_length=12)
    telephone1 = models.CharField(_('Segundo Teléfono Contacto'),max_length=12)
    email = models.EmailField()
    fecha_matricula = models.DateField(auto_now_add=True)
    pagada = models.BooleanField(_('Pagada'),default=False)
    accepta_condiciones = models.BooleanField(_('Doy mi consentimiento expreso para recibir comunicaciones en los términos anteriormente descritos.'), help_text=_('Doy mi consentimiento expreso para recibir comunicaciones en los términos anteriormente descritos.'),default=True,blank=True)
    nivel_ingles = models.CharField(_('Estudios previos de ingles eNivel'),max_length=150,default="")
    titulo_ingles = models.CharField(_('Estudios previos de ingles eNivel'),max_length=150,default="")
    clases_previas = models.CharField(_('Estudios previos de ingles eNivel'),max_length=150,default="")
    
    def send_confirmation_email(self):
        ##Para el alumno
        subject = _("Te has matriculado para un examen Cambridge en EIDE")
        
        html_content = ""
        
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
            ls = LinguaskillRegistration.objects.get(id=self.id)
            exam_date=ls.proposed_date
        except:
            exam_date=self.exam.exam_date
        subject = "Se ha confirmado el pago de la matricula para el examen %s"%self.exam
        html_content=u""""""%(self.exam)
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
    def registration_name(self):
        #return "%s - %s, %s"%(self.exam,self.surname,self.name)
	try:
	    return "%s"%(self.exam.level.schoollevel.__unicode__())
	except:
            return "%s"%(self.exam)
    def save(self, *args, **kwargs):
        ##We generate a random password
        if self.id is not None:
            if self.paid:
                self.send_paiment_confirmation_email()      
        else:
            #We set th password, not used right now
            self.password = ''.join([choice(letters) for i in xrange(6)])
            #COmprobamos si es un schoolexam
            try:
                if isinstance(self.exam.schoolexam,SchoolExam):
                    self.minor=True
                    self.eide_alumn=False
                    self.centre_name=self.exam.schoolexam.school.name
            except:
                pass
            #We send a confirmation mail to te registrant and a advise mail to the admins
            self.send_confirmation_email()
        super(Registration, self).save(*args, **kwargs)
        
    def generate_payment_url(self):
        return '/pagos/eide/%s/'%(self.id)

