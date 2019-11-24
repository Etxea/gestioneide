from __future__ import unicode_literals

from django.db import models

from django.contrib.auth.models import User

class Mensaje(models.Model):
    creador = models.ForeignKey(User,related_name="creador_mensaje")
    destinatario = models.ForeignKey(User)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    titulo = models.CharField(max_length=125)
    texto = models.TextField()
    leido = models.BooleanField(default=False)
    todos = models.BooleanField(default=False)

class Comentario(models.Model):
    mensaje = models.ForeignKey(Mensaje)
    creador = models.ForeignKey(User,related_name="creador_comentario")
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    texto = models.TextField()
    leido = models.BooleanField()