# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.core.urlresolvers import reverse_lazy,reverse

from gestioneide.models import Asistencia,Year,Asistencia,Grupo

# Create your models here.

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

class Confirmacion(models.Model):
    consulta = models.ForeignKey(Consulta)
    asistencia = models.ForeignKey(Asistencia)
    respuesta_bool = models.BooleanField()
    respuesta_texto = models.CharField('Respuesta (1000carac. max.)',max_length=1000,)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

