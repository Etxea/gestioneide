# -*- coding: utf-8 -*-
from django.db import models
from gestioneide.models import DIAS_SEMANA
import calendar

class Curso(models.Model):
    year = models.ForeignKey('gestioneide.Year',on_delete=models.CASCADE)
    nombre = models.CharField(max_length=50,default="")
    def __unicode__(self):
        return "%s - %s"%(self.year,self.nombre)

class Asignatura(models.Model):
    curso = models.ForeignKey('Curso', related_name='asignaturas',on_delete=models.CASCADE)
    nombre = models.CharField(max_length=50, default="")
    profesor = models.ForeignKey('gestioneide.Profesor',on_delete=models.CASCADE)

    def __unicode__(self):
        return u"%s - %s"%(self.curso, self.nombre)

    def get_dias_clase_mes(self,mes):
        dias_semana_clase = []
        dias_clase = []
        for dia in self.clases_turismo.all():
            dias_semana_clase.append(dia.dia_semana)
        year = Year().get_activo()
        ano = year.start_year
        if mes < 8 :
            ano = ano + 1
        cal = calendar.Calendar()
        for semana in cal.monthdays2calendar(ano,mes):
            for dia in semana:
                #Comprobamos que ese dia de la semana haya clase y no sea 0 (es de otro mes)
                #Sumanos 1 al dia ya que empiezan desde 0 y en bbdd empezamos desde 1
                if ( dia[1]+1 in dias_semana_clase ) and ( dia[0] > 0 ):
                    fecha = "%s-%s-%s"%(ano,mes,dia[0])
                    try:
                        festivo = Festivo.objects.get(fecha=fecha,tipo=1)
                        continue
                    except:
                        dias_clase.append(dia[0])
        return dias_clase

class Asistencia(models.Model):
    asignatura = models.ForeignKey(Asignatura,on_delete=models.CASCADE)
    alumno = models.ForeignKey('gestioneide.Alumno',related_name="asistencia_turismo",on_delete=models.CASCADE)
    def __unicode__(self):
        return "%s-%s"%(self.asignatura,self.alumno)

class Clase(models.Model):
    dia_semana = models.DecimalField(max_digits=1, decimal_places=0,choices=DIAS_SEMANA)
    aula = models.ForeignKey('gestioneide.Aula',related_name='clases_turismo',on_delete=models.CASCADE)
    profesor = models.ForeignKey('gestioneide.Profesor',related_name='clases_turismo',on_delete=models.CASCADE)
    asignatura = models.ForeignKey(Asignatura,related_name='clases_turismo',on_delete=models.CASCADE)
    hora_inicio = models.TimeField(auto_now=False, auto_now_add=False)
    hora_fin = models.TimeField(auto_now=False, auto_now_add=False)
    def __unicode__(self):
        return "%s/%s-%s"%(self.get_dia_semana_display(),self.hora_inicio,self.hora_fin)

class Presencia(models.Model):
    asistencia = models.ForeignKey('Asistencia',on_delete=models.CASCADE)
    mes = models.DecimalField(max_digits=2,decimal_places=0)
    dia = models.DecimalField(max_digits=2,decimal_places=0)

class Falta(models.Model):
    asistencia = models.ForeignKey('Asistencia',on_delete=models.CASCADE)
    mes = models.DecimalField(max_digits=2,decimal_places=0)
    dia = models.DecimalField(max_digits=2,decimal_places=0)

class Justificada(models.Model):
    asistencia = models.ForeignKey('Asistencia',on_delete=models.CASCADE)
    mes = models.DecimalField(max_digits=2,decimal_places=0)
    dia = models.DecimalField(max_digits=2,decimal_places=0)

