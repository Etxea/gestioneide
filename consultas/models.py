# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.core.urlresolvers import reverse_lazy,reverse
import uuid
from datetime import datetime
from anymail.message import AnymailMessage

from gestioneide.models import Asistencia,Year,Asistencia,Grupo

import logging
log = logging.getLogger('django')
debug = log.debug


# Create your models here.

CONFIRMACION_CHOICES = (
    (1,"Sí"),
    (2,"Sí, pero deseo otro horario"),
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
    respuesta_texto = models.CharField('Si no va a asistir el curso que viene, por favor, indíquenos por favor la razón',max_length=1000,)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_respuesta = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.pk == None:
            self.password = uuid.uuid4().hex[:8].upper()
        if self.respuesta_choice != 0:
            print "A contestado"
            self.fecha_respuesta=datetime.now()
            titulo = "Confirmacion alumno %s para el año %s en el centro %s"\
                %(self.asistencia.alumno,self.asistencia.year,self.asistencia.grupo.centro)
            mensaje = """El alumno %s con ID %s a contestado: <br /> %s <br />Con las razones: <br /> %s"""%(self.asistencia.alumno,self.asistencia.alumno.id,self.get_respuesta_choice_display(),self.respuesta_texto)
            self.asistencia.grupo.centro.enviar_mail(titulo, mensaje)
            if self.respuesta_choice == 1:
                print "Ha dicho que si"
                self.asistencia.confirmado = True
                self.asistencia.save()
        super(Confirmacion, self).save(*args, **kwargs)

    def get_confirmacion_url(self):
        return "https://portal-alumno.eide.es/consultas/confirmar/%s/%s/"%(self.id,self.password)

    def send_mail(self):
        ##Para el alumno
        subject = "[EIDE][Confirmacion] Confirmación curso %s en EIDE %s" %(self.asistencia.year,self.asistencia.grupo.centro)
        
        message_body = """<html><body><p>En el enlace al final de este email puede consultar el HORARIO PROPUESTO para el curso %s.
        EN ESE MISMO ENLACE, DEBERÁ INDICARNOS HASTA EL 14 DE JUNIO SI ESTÁ DE ACUERDO CON ESE HORARIO, 
        SI PREFIERE OTRO HORARIO O SI NO VA A ASISTIR EL CURSO QUE VIENE. Para ello, tendrá que elegir 
        una de las opciones del desplegable que aparece debajo del horario. En caso de que prefiera otro 
        horario, puede ponerse en contacto con nosotros tanto por email, como por teléfono o de forma 
        presencial. </p>
        <p>
        NOTA: En previsión de las medidas marcadas por las autoridades sanitarias, las clases se han acortado 5 minutos para poder realizar las desinfecciones necesarias entre clase y clase. Asimismo, para poder realizar entradas y salidas escalonadas, es posible que los horarios de entradas y salidas sufran variaciones de entre 5 y 10 minutos. Por supuesto, se les informará de las mismas con antelación suficiente.
        </p>
        <br />
<p><a href="%s">%s</a></p>
<br />
</body></html>"""%(self.asistencia.year,self.get_confirmacion_url(),self.get_confirmacion_url())
        
        if self.asistencia.alumno.enviar_mail(subject,message_body,mensaje_html=True):
            print "mail enviado"
        else:
            print "Error enviando mail"
