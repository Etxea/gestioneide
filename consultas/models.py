# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.core.urlresolvers import reverse_lazy,reverse
import uuid
from datetime import datetime

from gestioneide.models import Asistencia,Year,Asistencia,Grupo

# Create your models here.

CONFIRMACION_CHOICES = (
    (1,"Sí"),
    (2,"Sí pero deseo otro horario"),
    (3,"No"),
)

class Consulta(models.Model):
    nombre = models.CharField('Nombre',max_length=255,)
    texto = models.CharField('Consulta',max_length=1500,)
    fecha_creacion = models.DateField(auto_now_add=True)
    grupo = models.ForeignKey(Grupo)
    def get_absolute_url(self):
        return reverse_lazy("consulta_editar",args=[self.id])
    
    def __unicode__(self):
         return "%s"%(self.nombre)
    
    def __str__(self):
        return self.__unicode__()
    
    class Meta:
        ordering = ["fecha_creacion"]

class Respuesta(models.Model):
    consulta = models.ForeignKey(Consulta,on_delete=models.CASCADE)
    asistencia = models.ForeignKey(Asistencia)
    respuesta_bool = models.BooleanField()
    respuesta_texto = models.CharField('Respuesta (1000carac. max.)',max_length=1000,)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

class Confirmacion(models.Model):
    asistencia = models.ForeignKey(Asistencia)
    password = models.CharField(max_length=8,default="",blank=True)
    respuesta_choice = models.DecimalField('Respuesta',max_digits=1, decimal_places=0,choices=CONFIRMACION_CHOICES,default=0)
    respuesta_texto = models.CharField('Razón (1000carac. max.)',max_length=1000,)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_respuesta = models.DateTimeField(blank=True)

    def save(self, *args, **kwargs):
        if self.pk == None:
            self.password = uuid.uuid4().hex[:8].upper()
        if self.respuesta_choice != None:
            self.fecha_respuesta=datetime.now()
        super(Confirmacion, self).save(*args, **kwargs)

    def get_confirmacion_url(self):
        return "https://portal-alumno.eide.es/consultas/confirmar/%s/%s/"%(self.id,self.password)

    def send_mail(self):
        ##Para el alumno
        subject = "[EIDE][Confirmacion] Confirmación curso %s en EIDE %s" %(self.asistencia.year,self.asistencia.get_centro_display())
        
        message_body = "Buenas,<br>Hemos recibido tu matrícula, cuando se confirme el pago recibirás un segundo e-mail.<br>Un saludo."
        
        email = AnymailMessage(
            subject=subject,
            body=message_body,
            to = [self.asistencia.alumno.email1,self.asistencia.alumno.email2],
        )
        email.content_subtype = "html"
        try:
            email.send(fail_silently=False)
        except Exception, e:
            log.error("(confirmaciones) Error al enviar mail",str(e))