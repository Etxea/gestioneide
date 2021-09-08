from __future__ import unicode_literals

from django.db import models

from django.contrib.auth.models import User

class Mensaje(models.Model):
    creador = models.ForeignKey(User,related_name="creador_mensaje",on_delete=models.CASCADE)
    destinatario = models.ForeignKey(User,on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    titulo = models.CharField(max_length=125)
    texto = models.TextField()
    leido = models.BooleanField(default=False)
    todos = models.BooleanField(default=False)

class Comentario(models.Model):
    mensaje = models.ForeignKey(Mensaje,on_delete=models.CASCADE)
    creador = models.ForeignKey(User,related_name="creador_comentario",on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    texto = models.TextField()
    leido = models.BooleanField()