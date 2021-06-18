# -*- coding: utf-8 -*-
from django.db import models
from gestioneide.models import DIAS_SEMANA
import calendar

class Curso(models.Model):
    year = models.ForeignKey('gestioneide.Year')
    nombre = models.CharField(max_length=50,default="")
    def __unicode__(self):
        return "%s - %s"%(self.year,self.nombre)

class Asignatura(models.Model):
    curso = models.ForeignKey('Curso', related_name='asignaturas')
    nombre = models.CharField(max_length=50, default="")
    profesor = models.ForeignKey('gestioneide.Profesor')

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
    asignatura = models.ForeignKey(Asignatura)
    alumno = models.ForeignKey('gestioneide.Alumno',related_name="asistencia_turismo")
    def __unicode__(self):
        return "%s-%s"%(self.asignatura,self.alumno)

class Clase(models.Model):
    dia_semana = models.DecimalField(max_digits=1, decimal_places=0,choices=DIAS_SEMANA)
    aula = models.ForeignKey('gestioneide.Aula',related_name='clases_turismo')
    profesor = models.ForeignKey('gestioneide.Profesor',related_name='clases_turismo')
    asignatura = models.ForeignKey(Asignatura,related_name='clases_turismo')
    hora_inicio = models.TimeField(auto_now=False, auto_now_add=False)
    hora_fin = models.TimeField(auto_now=False, auto_now_add=False)
    def __unicode__(self):
        return "%s/%s-%s"%(self.get_dia_semana_display(),self.hora_inicio,self.hora_fin)

class Presencia(models.Model):
    asistencia = models.ForeignKey('Asistencia')
    mes = models.DecimalField(max_digits=2,decimal_places=0)
    dia = models.DecimalField(max_digits=2,decimal_places=0)

class Falta(models.Model):
    asistencia = models.ForeignKey('Asistencia')
    mes = models.DecimalField(max_digits=2,decimal_places=0)
    dia = models.DecimalField(max_digits=2,decimal_places=0)

    # def save(self, *args, **kwargs):
    #     #evitamos duplicar faltas el mismo día por error
    #     if Falta.objects.filter(asistencia=self.asistencia).filter(mes=self.mes).filter(dia=self.dia).count() > 0:
    #         print "Ya tiene falta ese día! no la guardamos."
    #         return
    #     else:
    #         super(Falta, self).save(*args, **kwargs)  # Call the "real" save() method.
    #         #Si el grupo es de menores y suma cinco mandamos mail
    #         if self.asistencia.grupo.menores:
    #             print "es un grupo de menores contamos las faltas"
    #             num_faltas_mes = Falta.objects.filter(asistencia=self.asistencia).filter(mes=self.mes).count()
    #             print "tiene %s faltas"%num_faltas_mes
    #             if num_faltas_mes > 3:
    #                 print "Mandamos mail"
    #                 subject="[Gestion Alumnos]Aviso de faltas %s en el mes %s"%(self.asistencia.alumno,self.mes)
    #                 message="El alumno %s en el grupo %s a sobrepasado el ńumero de faltas con un total %s en el mes de %s"% (self.asistencia.alumno,self.asistencia.grupo,num_faltas_mes,self.mes)
    #                 print "Mandamos mail: %s \n %s"%(subject,message)
    #                 mail_admins(subject,message)

class Justificada(models.Model):
    asistencia = models.ForeignKey('Asistencia')
    mes = models.DecimalField(max_digits=2,decimal_places=0)
    dia = models.DecimalField(max_digits=2,decimal_places=0)

