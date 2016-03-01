# -*- coding: utf-8 -*-
from django.db import models
from django.db.models import Count

from django.utils.translation import gettext_lazy as _
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.models import User
from django.utils.dates import MONTHS
from django.utils.timezone import now
import datetime

DIAS_SEMANA = (
    (1, _('Lunes')),
    (2, _('Martes')),
    (3, _('Miercoles')),
    (4, _('Jueves')),
    (5, _('Viernes'))
)

TIPO_FESTIVO = (
    (1, _('Festivo')),
    (2, _('Inicio Curso')),
    (3, _('Fin Curso')),
    (4, _('Inicio vacaciones/Puente')),
    (5, _('Fin Vacaciones/Puente')),
	(6, _('Festivo oficial'))
)

DURACION = (
    (15, _('1/4 hora')),
    (30, _('1/2 hora')),
    (45, _('3/4 hora')),
    (55, _('55min')),
    (60, _('1h')),
    (90, _('1h y 1/2')),
    (120, _('2h')),
    (150, _('2h y 1/2')),
    (180, _('3h')),
    (210, _('3h y 1/2')),
    (240, _('4h')),
    (270, _('4h y 1/2'))   
)

class Aula(models.Model):
    nombre = models.CharField('Nombre',max_length=255,)
    aforo = models.DecimalField(max_digits=3, decimal_places=0)
    pdi = models.BooleanField(default=False,blank=True)
    def __unicode__(self):
         return "%s"%(self.nombre)
    def get_absolute_url(self):
        return "/aulas/editar/%i/" % self.id
    def clases_lunes(self):
        return self.clases.filter(dia_semana=1).order_by('hora_inicio')
    def clases_martes(self):
        return self.clases.filter(dia_semana=2)
    def clases_miercoles(self):
        return self.clases.filter(dia_semana=3)
    def clases_jueves(self):
        return self.clases.filter(dia_semana=4)
    def clases_viernes(self):
        return self.clases.filter(dia_semana=5)
        
class Profesor(models.Model):
#    user = models.OneToOneField(User)
    nombre = models.CharField(max_length=25,default="")
    apellido = models.CharField(max_length=50,default="")
    telefono = models.CharField(max_length=9,default="")
    email = models.EmailField(default="",blank=True,null=True)

    def __unicode__(self):
        #~ return "%s %s (%s)"%(self.user.get_short_name(),self.user.last_name,self.user.username)
        #~ return "%s, %s"%(self.apellido,self.nombre)
        return "%s"%(self.nombre)
    def get_absolute_url(self):
        return "/profesores/%s/"%self.id
    def clases_lunes(self):
        return self.clases.filter(dia_semana=1).order_by('hora_inicio')
        
    def get_horas_pendientes(self):
        pendiente_horas = 0
        pendiente_minutos = 0
        try:
            horas = self.user.asistencia_set.filter(contabilizado=False).aggregate(Sum('duracion'))
        except:
            print "No podemos agregar fecha asi que a mano"
            for p in self.user.asistencia_set.filter(contabilizado=False):
                print "Sumamos ",p.duracion
                pendiente_horas = pendiente_horas + p.duracion.hour
                pendiente_minutos = pendiente_minutos + p.duracion.minute
        print "Tenemos %s:%s"%(pendiente_horas,pendiente_minutos)
        pendiente_horas = pendiente_horas + pendiente_minutos/60
        pendiente_minutos = pendiente_minutos%60
        print "Tenemos %s:%s"%(pendiente_horas,pendiente_minutos)
        return "%s:%s"%(pendiente_horas,pendiente_minutos)

class Alumno(models.Model):
    nombre = models.CharField(max_length=25,default="")
    apellido1 = models.CharField(max_length=100,default="")
    apellido2 = models.CharField(max_length=100,default="",blank=True,null=True)
    fecha_nacimiento = models.DateField(default=datetime.date.today,blank=True)
    telefono1 = models.CharField(max_length=9,default="")
    telefono2 = models.CharField(max_length=9,default="",blank=True,null=True)
    email = models.EmailField(default="",blank=True,null=True)
    cuenta_bancaria = models.CharField(max_length=25,default="")
    localidad = models.CharField(max_length=25,default="")
    cp = models.CharField(max_length=5,default="48980")
    dni = models.CharField(max_length=9,default="",blank=True,null=True)
    activo = models.BooleanField(default=True)
    def __unicode__(self):
    #    return "%s %s (%s)"%(self.user.get_short_name(),self.user.last_name,self.user.username)
        return "(%s) %s %s,%s"%(self.id,self.apellido1,self.apellido2,self.nombre)

    def get_absolute_url(self):
        return "/alumnos/%s/"%self.id
    def validate_cuenta_bancaria(self):
        return True
    def grupos(self):
        ret = ""
        for asis in self.asistencia_set.all():
            ret = ret + " %s"%asis.grupo.nombre
        return ret

class Historia(models.Model):
    alumno = models.ForeignKey('Alumno')
    fecha = models.DateField(auto_now_add=True)
    tipo = models.CharField(max_length=25,default="")
    anotacion = models.CharField(max_length=25,default="")

class Libro(models.Model):
    titulo = models.CharField(max_length=50,default="")
    autor = models.CharField(max_length=25,default="",blank=True)
    isbn = models.CharField(max_length=40,default="")
    editorial = models.CharField(max_length=40,default="")
    def __unicode__(self):
        return "%s - %s"%(self.titulo,self.editorial)
    def get_absolute_url(self):
        return reverse_lazy("curso_libro_detalle",args=[self.id])

class Curso(models.Model):
    nombre = models.CharField(max_length=25,default="")
    precio = models.FloatField(default=100)
    ##No obligatorios
    examen = models.CharField(max_length=25,default="",blank=True,null=True)
    nivel = models.CharField(max_length=25,default="",blank=True,null=True)
    libros = models.ManyToManyField('Libro')
    nota_aprobado = models.FloatField(default=50)
    solo_examen_final = models.BooleanField(default=False)
    def get_absolute_url(self):
        return reverse_lazy("curso_editar",args=[self.id])
    def __unicode__(self):
         return "%s"%(self.nombre)

class Grupo(models.Model):
    nombre = models.CharField(max_length=25,default="")
    curso = models.ForeignKey('Curso')
    precio  = models.DecimalField(max_digits=3,decimal_places=0,default=0)
    num_max = models.DecimalField(max_digits=2,decimal_places=0,default=14) #El tamano default no es lo mejor que este aqui, pero bueno
    menores = models.BooleanField(default=False)
    class Meta:
        ordering = ["nombre"]
    def get_absolute_url(self):
        return reverse_lazy("grupo_detalle",args=[self.id]) 
    def confirmados(self):
        return self.asistencia_set.filter(confirmado=True).count()
    def sin_confirmar(self):
        return self.asistencia_set.filter(confirmado=False).count()
    def lista_clases(self):
        ret = ""
        for clase in self.clases.all():
            ret = ret + " " + clase.__unicode__()
        return ret
    def get_precio(self):
        if self.precio:
            return self.precio
        else:
            return self.curso.precio
    def next_by_nombre(self):
        posicion = int(Grupo.objects.annotate(Count('asistencia')).filter(asistencia__count__gt=0).order_by('nombre').filter(nombre__lt = self.nombre).count())
        total = len(Grupo.objects.annotate(Count('asistencia')).filter(asistencia__count__gt=0))
        print "Somo el %s de %s"%(posicion,total)
        if posicion == total:
            return self.id
        else:
            return Grupo.objects.annotate(Count('asistencia')).filter(asistencia__count__gt=0).order_by('nombre')[posicion+1].id
            
    def prev_by_nombre(self):
        posicion = Grupo.objects.annotate(Count('asistencia')).filter(asistencia__count__gt=0).order_by('nombre').filter(nombre__lt = self.nombre).count()
        total = len(Grupo.objects.annotate(Count('asistencia')).filter(asistencia__count__gt=0))
        print "Somo el %s de %s"%(posicion,total)
        if posicion == 0:
            return self.id
        else:
            return Grupo.objects.annotate(Count('asistencia')).filter(asistencia__count__gt=0).order_by('nombre')[posicion-1].id
            
    def __unicode__(self):
        return "%s"%(self.nombre)
    def get_absolute_url(self):
        return reverse_lazy("grupo_detalle",args=[self.id])
        
class Clase(models.Model):
    dia_semana = models.DecimalField(max_digits=1, decimal_places=0,choices=DIAS_SEMANA)
    aula = models.ForeignKey(Aula,related_name='clases')
    profesor = models.ForeignKey(Profesor,related_name='clases')
    grupo = models.ForeignKey(Grupo,related_name='clases')
    hora_inicio = models.TimeField(auto_now=False, auto_now_add=False)
    hora_fin = models.TimeField(auto_now=False, auto_now_add=False)
    def __unicode__(self):
        return "%s/%s-%s/%s"%(self.get_dia_semana_display(),self.hora_inicio,self.hora_fin,self.profesor)

class Ano(models.Model):
    ano = models.CharField(max_length=8,default="20XX-XX")
    activo = models.BooleanField(default=1)
    def __unicode__(self):
        return "%s"%self.ano

class Asistencia(models.Model):
    ano = models.ForeignKey('Ano')
    grupo = models.ForeignKey('Grupo')
    alumno = models.ForeignKey('Alumno')
    confirmado = models.BooleanField(default=False)
    factura = models.BooleanField(default=False)
    metalico = models.BooleanField(default=True)
    precio = models.FloatField(default=100)
    #~ notas = MultipleJoin('Notas')
    #~ faltas = MultipleJoin('Notas')
    def siguiente_asistencia_grupo(self):
        #Deberiamos sacar la lista de asistencia s dle grupo ordenadas por id, calcula nuestra posición y devolver el id de la siguiente
        count = 0
        for asistencia in self.grupo.asistencia_set.all():
            count =+ 1
            if asistencia == self:
                return  self.grupo.asistencia_set.all()[count].id
    def anterior_asistencia_grupo(self):
        return 0
    def __unicode__(self):
        return "%s"%(self.alumno.id)

class Nota(models.Model):
    asistencia = models.ForeignKey('Asistencia')
    trimestre = models.DecimalField(max_digits=1,decimal_places=0)
    grama = models.DecimalField(max_digits=3,decimal_places=0,default=0)
    grama_baremo = models.DecimalField(max_digits=3,decimal_places=0,default=0)
    expresion = models.DecimalField(max_digits=3,decimal_places=0,default=0)
    expresion_baremo = models.DecimalField(max_digits=3,decimal_places=0,default=0)
    lectura = models.DecimalField(max_digits=3,decimal_places=0,default=0)
    lectura_baremo = models.DecimalField(max_digits=3,decimal_places=0,default=0)
    
class Falta(models.Model):
    asistencia = models.ForeignKey('Asistencia')
    mes = models.DecimalField(max_digits=1,decimal_places=0)
    justificadas = models.DecimalField(max_digits=3,decimal_places=0,default="0")
    faltas = models.DecimalField(max_digits=3,decimal_places=0,default="0")

class Recibo(models.Model):
    fecha_creacion = models.DateField(auto_now_add=True)
    mes = models.DecimalField(max_digits=1,decimal_places=0,choices=MONTHS.items())
    medio_mes = models.BooleanField(default=False)
    grupos = models.ManyToManyField(Grupo)
    def get_absolute_url(self):
        return reverse_lazy("recibo_detalle",args=[self.id])
    def get_total_alumnos(self):
        return self.grupos.all().aggregate(Count('asistencia'))
    def csb19(self):
		return "000000000000000000000000"

class Festivo(models.Model):
    fecha = models.DateField()
    anotacion = models.CharField(max_length=25,default="")
    tipo = models.DecimalField(max_digits=1, decimal_places=0,choices=TIPO_FESTIVO)