# -*- coding: utf-8 -*-
from django.db import models
from django.db.models import Count

from django.utils.translation import gettext_lazy as _
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.models import User
from django.utils.dates import MONTHS
from django.utils.timezone import now

import datetime
import calendar

DIAS_SEMANA = (
    (1, _('Lunes')),
    (2, _('Martes')),
    (3, _('Miercoles')),
    (4, _('Jueves')),
    (5, _('Viernes'))
)
TIPO_EVALUACION = (
    (1, _('Otro')),
    (2, _('elementary_intermediate')),
    (3, _('upper_proficiency')),
)

TIPO_FESTIVO = (
    (1, _('Festivo')),
    (2, _('Inicio Curso')),
    (3, _('Fin Curso')),
    (4, _('Inicio vacaciones/Puente')),
    (5, _('Fin Vacaciones/Puente')),
    (6, _('Festivo oficial')),
    (7, _('Inicio trimestre')),
    (8, _('Fin trimestre'))
    
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
    def programacion_semana(self):
        tabla_clases = []
        for hora in range(8,22):
            grupos = Grupo.objects.filter(year=Year.objects.get(activo=True))
            for cuarto in [0,30]:
                fecha_consulta = datetime.time(hora,cuarto)
                programacion_hora = ["%02d:%02d"%(hora,cuarto)]
                for dia in range(1,6):
                    print dia
                    clase = Clase.objects.filter(dia_semana=dia,aula=self,\
                            hora_inicio__lt=fecha_consulta,hora_fin__gte=fecha_consulta,grupo__in=grupos)
                    if clase.count() == 1:
                        clase = clase[0]
                        #print "Anadimos la clase es: %s" % clase
                        programacion_hora.append("%s-%s"%(clase.grupo,clase.profesor))
                    elif clase.count() > 1:
                        programacion_hora.append("SOLAPE: %s vs %s"%\
                                (clase[0].grupo,clase[1].grupo))
                    else:
                        programacion_hora.append("")
                tabla_clases.append(programacion_hora)
        return tabla_clases

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

    def programacion_semana(self):
        tabla_clases = []
        for hora in range(8,22):
            #print "Vamos con la hora %s"%hora
            grupos = Grupo.objects.filter(year=Year.objects.get(activo=True))
            for cuarto in [0,30]:
                fecha_consulta = datetime.time(hora,cuarto)
                #print "Vamos con la fecha de consulta %s"%(fecha_consulta)
                programacion_hora = ["%02d:%02d"%(hora,cuarto)]
                for dia in range(1,6):
                    print dia
                    clase = Clase.objects.filter(dia_semana=dia,profesor=self,\
                            hora_inicio__lt=fecha_consulta,hora_fin__gte=fecha_consulta,grupo__in=grupos)
                    if clase.count() == 1:
                        clase = clase[0]
                        #print "Anadimos la clase es: %s" % clase
                        programacion_hora.append("%s-%s"%(clase.grupo,clase.aula))
                    elif clase.count() > 1:
                        programacion_hora.append("SOLAPE: %s vs %s"%\
                                (clase[0].grupo,clase[1].grupo))
                    else:
                        programacion_hora.append("")
                tabla_clases.append(programacion_hora)
        #~ print "Clases"
        #~ print tabla_clases
        return tabla_clases
        #~ return claseTable(clases)
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
    fecha_creacion = models.DateField(default=datetime.date.today)
    telefono1 = models.CharField(max_length=9,default="")
    telefono2 = models.CharField(max_length=9,default="",blank=True,null=True)
    email = models.EmailField(default="",blank=True,null=True)
    cuenta_bancaria = models.CharField(max_length=25,default="")
    direccion = models.CharField(max_length=250,default="",blank=True,null=True)
    ciudad = models.CharField(max_length=25,default="Santurtzi")
    cp = models.CharField(max_length=5,default="48980")
    dni = models.CharField(max_length=9,default="",blank=True,null=True)
    activo = models.BooleanField(default=True)
    observaciones = models.CharField(max_length=500,blank=True,null=True,default="")
    #Hacemos un overrido de save para añadir entradas al historico
    def save(self, *args, **kw):
        if self.pk is not None:
            orig = Alumno.objects.get(pk=self.pk)
            if orig.activo == False and self.activo == True:
                hist = Historia(alumno=self,tipo="alta",anotacion="Recuperamos alumno")
                hist.save()
            else:
                hist = Historia(alumno=self,tipo="modificación",anotacion="Datos editados")
                hist.save()
        super(Alumno, self).save(*args, **kw)
    def __unicode__(self):
    #    return "%s %s (%s)"%(self.user.get_short_name(),self.user.last_name,self.user.username)
        return "%s %s %s,%s"%(self.id,self.apellido1,self.apellido2,self.nombre)

    def get_absolute_url(self):
        return reverse_lazy("alumno_detalle",args=[self.id])
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
    class Meta:
        ordering = ['-fecha']

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
    tipo_evaluacion = models.DecimalField(max_digits=1, decimal_places=0,choices=TIPO_EVALUACION)
    ##No obligatorios
    examen = models.CharField(max_length=25,default="",blank=True,null=True)
    nivel = models.CharField(max_length=25,default="",blank=True,null=True)
    libros = models.ManyToManyField('Libro',null=True,blank=True)
    nota_aprobado = models.FloatField(default=50)
    solo_examen_final = models.BooleanField(default=False)
    def get_absolute_url(self):
        return reverse_lazy("curso_editar",args=[self.id])
    def __unicode__(self):
         return "%s"%(self.nombre)
    class Meta:
        ordering = ["nombre"]

class Grupo(models.Model):
    year = models.ForeignKey('Year')
    nombre = models.CharField(max_length=25,default="")
    curso = models.ForeignKey('Curso')
    precio  = models.DecimalField(max_digits=3,decimal_places=0,default=0)
    num_max = models.DecimalField(max_digits=2,decimal_places=0,default=14) #El tamano default no es lo mejor que este aqui, pero bueno
    menores = models.BooleanField(default=False)
    class Meta:
        ordering = ["nombre"]
    def ver_precio(self):
        if self.precio:
            return self.precio
        else:
            return self.curso.precio
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
        year = Year.objects.get(activo=True)
        posicion = int(Grupo.objects.filter(year=year).annotate(Count('asistencia')).filter(asistencia__count__gt=0).order_by('nombre').filter(nombre__lt = self.nombre).count())
        total = len(Grupo.objects.filter(year=year).annotate(Count('asistencia')).filter(asistencia__count__gt=0))
        print "Somo el %s de %s"%(posicion,total)
        if posicion == total:
            return self.id
        else:
            return Grupo.objects.filter(year=year).annotate(Count('asistencia')).filter(asistencia__count__gt=0).order_by('nombre')[posicion+1].id
            
    def prev_by_nombre(self):
        year = Year.objects.get(activo=True)
        posicion = Grupo.objects.filter(year=year).annotate(Count('asistencia')).filter(asistencia__count__gt=0).order_by('nombre').filter(nombre__lt = self.nombre).count()
        total = len(Grupo.objects.filter(year=year).annotate(Count('asistencia')).filter(asistencia__count__gt=0))
        print "Somo el %s de %s"%(posicion,total)
        if posicion == 0:
            return self.id
        else:
            return Grupo.objects.filter(year=year).annotate(Count('asistencia')).filter(asistencia__count__gt=0).order_by('nombre')[posicion-1].id
            
    def __unicode__(self):
        return "%s"%(self.nombre)
    def get_absolute_url(self):
        return reverse_lazy("grupo_detalle",args=[self.id])
        
    def get_dias_clase_mes(self,mes):
        dias_semana_clase = []
        dias_clase = []
        for dia in self.clases.all():
            dias_semana_clase.append(dia.dia_semana)
        
        year = Year.objects.get(activo=True)
        ano = year.start_year
        if mes < 8 :
            ano = ano + 1 
        cal = calendar.Calendar()
        for semana in cal.monthdays2calendar(ano,mes):
            for dia in semana:
                #COmprobamos que ese dia de la semana haya clase y no sea 0 (es de otro mes)
                if ( dia[1] in dias_semana_clase ) and ( dia[0] > 0 ):
                    fecha = "%s-%s-%s"%(ano,mes,dia[0])
                    try:
                        festivo = Festivo.objects.get(fecha=fecha)
                        continue
                    except:
                        dias_clase.append(dia[0])
        return dias_clase
        
class Clase(models.Model):
    dia_semana = models.DecimalField(max_digits=1, decimal_places=0,choices=DIAS_SEMANA)
    aula = models.ForeignKey(Aula,related_name='clases')
    profesor = models.ForeignKey(Profesor,related_name='clases')
    grupo = models.ForeignKey(Grupo,related_name='clases')
    hora_inicio = models.TimeField(auto_now=False, auto_now_add=False)
    hora_fin = models.TimeField(auto_now=False, auto_now_add=False)
    def __unicode__(self):
        return "%s/%s-%s/%s"%(self.get_dia_semana_display(),self.hora_inicio,self.hora_fin,self.profesor)
        
class Year(models.Model):
    start_year = models.DecimalField(max_digits=4,decimal_places=0,default=2015)
    name = models.CharField(max_length=8,default="201X-1X")
    activo = models.BooleanField(default=1)
    def __unicode__(self):
        return "%s"%self.name
from django.db.models import Q    
class Asistencia(models.Model):
    year = models.ForeignKey('Year')
    grupo = models.ForeignKey('Grupo',limit_choices_to=Q(year=Year.objects.get(activo=True)))
    alumno = models.ForeignKey('Alumno')
    confirmado = models.BooleanField(default=False)
    factura = models.BooleanField(default=False)
    metalico = models.BooleanField(default=True)
    precio = models.FloatField(null=True,blank=True)
    #~ notas = MultipleJoin('Notas')
    #~ faltas = MultipleJoin('Notas')
    def ver_precio(self):
        if self.precio:
            return self.precio
        else:
            return self.grupo.ver_precio()
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

    control = models.DecimalField(max_digits=3,decimal_places=0,default=0)
    control_np = models.BooleanField(default=False)
    control_na = models.BooleanField(default=False)
    
    grammar = models.DecimalField(max_digits=3,decimal_places=0,default=0)
    grammar_np = models.BooleanField(default=False)
    grammar_na = models.BooleanField(default=False)
    
    reading = models.DecimalField(max_digits=3,decimal_places=0,default=0)
    reading_np = models.BooleanField(default=False)
    reading_na = models.BooleanField(default=False)
    
    writing = models.DecimalField(max_digits=3,decimal_places=0,default=0)
    writing_np = models.BooleanField(default=False)
    writing_na = models.BooleanField(default=False)
    
    useofenglish = models.DecimalField(max_digits=3,decimal_places=0,default=0)
    useofenglish_np = models.BooleanField(default=False)
    useofenglish_na = models.BooleanField(default=False)

    listenning = models.DecimalField(max_digits=3,decimal_places=0,default=0)
    listenning_np = models.BooleanField(default=False)
    listenning_na = models.BooleanField(default=False)

    speaking = models.DecimalField(max_digits=3,decimal_places=0,default=0)
    speaking_np = models.BooleanField(default=False)
    speaking_na = models.BooleanField(default=False)

    comportamiento = models.CharField(max_length=2,default="B")
    comportamiento_np = models.BooleanField(default=False)
    comportamiento_na = models.BooleanField(default=False)

    
class Falta(models.Model):
    asistencia = models.ForeignKey('Asistencia')
    mes = models.DecimalField(max_digits=1,decimal_places=0)
    justificadas = models.DecimalField(max_digits=3,decimal_places=0,default="0")
    faltas = models.DecimalField(max_digits=3,decimal_places=0,default="0")

class Recibo(models.Model):
    year = models.ForeignKey('Year')
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
    year = models.ForeignKey('Year')
    fecha = models.DateField()
    anotacion = models.CharField(max_length=50,default="")
    tipo = models.DecimalField(max_digits=1, decimal_places=0,choices=TIPO_FESTIVO)
    class Meta:
        ordering = ['fecha']
