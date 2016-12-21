# -*- coding: utf-8 -*-
from django.db import models
from django.db.models import Count

from django.utils.translation import gettext_lazy as _
from django.core.urlresolvers import reverse_lazy
from django.utils.text import slugify
from django.contrib.auth.models import User, Group
from django.utils.dates import MONTHS
from django.utils.timezone import now
from django.db.models import Q
from django.conf import settings
if "mailer" in settings.INSTALLED_APPS:
    from mailer import send_mail, mail_admins
else:
    from django.core.mail import send_mail, mail_admins

import datetime
import calendar

from utils import *

DIAS_SEMANA = (
    (1, _('Lunes')),
    (2, _('Martes')),
    (3, _('Miercoles')),
    (4, _('Jueves')),
    (5, _('Viernes'))
)
TIPO_EVALUACION = (
    (1, _('Trimestral')),
    (2, _('Elementary/Prei Intermediate')),
    (3, _('Intermediate')),
    (4, _('Upper/[Pre]First/Advance/Proficiency')),
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

class Year(models.Model):
    start_year = models.DecimalField(max_digits=4,decimal_places=0,default=2015)
    name = models.CharField(max_length=8,default="201X-1X")
    activo = models.BooleanField(default=1)
    def __unicode__(self):
        return "%s"%self.name

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
                            hora_inicio__lte=fecha_consulta,hora_fin__gt=fecha_consulta,grupo__in=grupos)
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
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)
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

    def update_user_password(self):
        password = User.objects.make_random_password()
        self.user.set_password(password)
        self.user.save()
        mensaje = u"""Buenas %s,
Te acabamos de crear un usuario para el nuevo sistema de
gestión de alumnos de EIDE. Los datos de acceso son:
https://gestion.eide.es
usuario: %s
contraseña: %s
Guarda en lugar seguro estos datos por favor."""%(self.nombre,self.user.username,password)
        print self.nombre,self.user.username,password
        #self.user.email_user("Alta en gestion de alumnos EIDE",mensaje)

    def create_user(self):
        try:
            pg = Group.objects.get(name="profesores")            
        except:
            pg = Group(name="profesores")
            pg.save()
        if self.user == None:
            try:
                u = User.objects.get(username=slugify(self.nombre))
                self.user=u
                u.groups.add(pg)
                u.save()
                self.save()
            except:
                password = User.objects.make_random_password()
                print "No hay usuario generamos uno para ",self.nombre,"con el pass ",password
                username = slugify(self.nombre)
                u = User(username=username,email=self.email)
                u.save()
                u.set_password(password)
                u.groups.add(pg)
                u.save()
                mensaje = u"""Buenas %s,
                Te acabamos de crear un usuario para el nuevo sistema de
                gestión de alumnos de EIDE. Los datos de acceso son:
                https://gestion.eide.es
                usuario: %s
                contraseña: %s
                Guarda en lugar seguro estos datos por favor.
                """%(self.nombre,username,password)
                u.email_user("Alta en gestion de alumnos EIDE",mensaje)
                self.user=u
                self.save()

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
    cuenta_bancaria = models.CharField(max_length=23,default="")
    direccion = models.CharField(max_length=250,default="",blank=True,null=True)
    ciudad = models.CharField(max_length=25,default="Santurtzi",blank=True,null=True)
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

class Anotacion(models.Model):
    alumno = models.ForeignKey('Alumno')
    fecha = models.DateField(auto_now_add=True)
    creador = models.ForeignKey(User)#, editable=False)
    texto = models.CharField(max_length=500,default="")
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
    libros = models.ManyToManyField('Libro',blank=True)
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
    def get_profesores(self):
        profesores = []
        for clase in self.clases.all():
            profesor = clase.profesor
            if profesor in profesores:
                continue
            else:
                profesores.append(profesor)
        texto = ""
        for profesor in profesores:
            texto = "%s / %s"%(texto,profesor)
        return texto
    def get_precio(self):
        if self.precio:
            return self.precio
        else:
            return self.curso.precio
    def next_by_nombre(self,cuatrimestre=False):
        year = Year.objects.get(activo=True)
        if cuatrimestre:
            filtro = Grupo.objects.filter(year=year).annotate(Count('asistencia')).filter(asistencia__count__gt=0).order_by('nombre')
        else:
            filtro = Grupo.objects.filter(year=year).annotate(Count('asistencia')).filter(asistencia__count__gt=0).order_by('nombre')
        posicion = int(filtro.filter(nombre__lt = self.nombre).count())
        total = len(filtro)
        print "Somo el %s de %s"%(posicion,total)
        if posicion == total:
            return self.id
        else:
            return filtro[posicion+1].id

    def next_by_nombre_quatrimestre(self):
        self.next_by_nombre(cuatrimestre=True)

    def prev_by_nombre(self,cuatrimestre=False):
        year = Year.objects.get(activo=True)
        if cuatrimestre:
            filtro = Grupo.objects.filter(year=year).annotate(Count('asistencia')).filter(
                asistencia__count__gt=0).order_by('nombre')
        else:
            filtro = Grupo.objects.filter(year=year).annotate(Count('asistencia')).filter(
                asistencia__count__gt=0).order_by('nombre')

        posicion = filtro.filter(nombre__lt = self.nombre).count()
        total = len(filtro)
        print "Somo el %s de %s"%(posicion,total)
        if posicion == 0:
            return self.id
        else:
            return Grupo.objects.filter(year=year).annotate(Count('asistencia')).filter(asistencia__count__gt=0).order_by('nombre')[posicion-1].id

    def prev_by_nombre_quatrimestre(self):
        self.prev_by_nombre(cuatrimestre=True)
    def __unicode__(self):
        return "%s"%(self.nombre)
    def get_absolute_url(self):
        return reverse_lazy("grupo_detalle",args=[self.id])
        
    def get_dias_clase_mes(self,mes):
        dias_semana_clase = []
        dias_clase = []
        for dia in self.clases.all():
            dias_semana_clase.append(dia.dia_semana)
        print dias_semana_clase
        year = Year.objects.get(activo=True)
        ano = year.start_year
        if mes < 8 :
            ano = ano + 1 
        cal = calendar.Calendar()
        for semana in cal.monthdays2calendar(ano,mes):
            for dia in semana:
                #COmprobamos que ese dia de la semana haya clase y no sea 0 (es de otro mes)
                #Sumanos 1 al dia ya que empiezan desde 0 y en bbd empezamos desde 1
                if ( dia[1]+1 in dias_semana_clase ) and ( dia[0] > 0 ):
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

class Asistencia(models.Model):
    year = models.ForeignKey('Year')
    grupo = models.ForeignKey('Grupo',limit_choices_to=Q(year=Year.objects.get(activo=True))) #Comentar el limit choices para un primer import
    alumno = models.ForeignKey('Alumno')
    confirmado = models.BooleanField(default=False)
    factura = models.BooleanField(default=False)
    metalico = models.BooleanField(default=False)
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

    def faltas_trimestre(self,trimestre):
        meses = []
        if trimestre==1:
           meses = [9,8,10,11,12]
        elif trimestre==2:
           meses = [1,2,3]
        elif trimestre==2:
           meses = [4,5,6]
        #return self.falta_set.filter(mes__in=meses).count()
        faltas = Falta.objects.filter(asistencia=self).filter(mes__in=meses).count()
        return faltas

    def justificadas_trimestre(self,trimestre):
        meses = []
        if trimestre==1:
           meses = [9,8,10,11,12]
        elif trimestre==2:
           meses = [1,2,3]
        elif trimestre==2:
           meses = [4,5,6]
        return self.justificada_set.filter(mes__in=meses).count()

    def get_nota_trimestre(self,trimestre):
        nota = "0"
        notaquery = self.notatrimestral_set.filter(trimestre=trimestre)
        if notaquery.count() > 0:
            nota = notaquery[0].nota
        return nota

    def get_observaciones_trimestre(self,trimestre):
        observaciones = ""
        notaquery = self.notatrimestral_set.filter(trimestre=trimestre)
        if notaquery.count() > 0:
            observaciones = notaquery[0].observaciones
        return observaciones

    def nota_trimestre(self,trimestre):
        nota = self.get_nota_trimestre(trimestre)
        observaciones = self.get_observaciones_trimestre(trimestre)
        return nota,observaciones

    def nota_quatrimestre(self,quatrimestre):
        nota = "0"
        observaciones = "No presentado"
        notaquery = self.notaquatrimestral_set.filter(quatrimestre=quatrimestre)
        if notaquery.count() > 0:
            nota = notaquery[0].nota
            observaciones = notaquery[0].observaciones
        return nota,observaciones

    def __unicode__(self):
        return "%s"%(self.alumno.id)

class Nota(models.Model):
    asistencia = models.ForeignKey('Asistencia')
    trimestre = models.DecimalField(max_digits=1,decimal_places=0)
    fecha_creacion = models.DateField(auto_now_add=True)

    control = models.DecimalField(max_digits=3,decimal_places=0,default=0)
    control_np = models.BooleanField("NP",default=False)
    control_na = models.BooleanField(default=False)
    
    grammar = models.DecimalField(max_digits=3,decimal_places=0,default=0)
    grammar_np = models.BooleanField("NP",default=False)
    grammar_na = models.BooleanField(default=False)
    
    reading = models.DecimalField(max_digits=3,decimal_places=0,default=0)
    reading_np = models.BooleanField("NP",default=False)
    reading_na = models.BooleanField(default=False)
    
    writing = models.DecimalField(max_digits=3,decimal_places=0,default=0)
    writing_np = models.BooleanField("NP",default=False)
    writing_na = models.BooleanField(default=False)
    
    useofenglish = models.DecimalField(max_digits=3,decimal_places=0,default=0)
    useofenglish_np = models.BooleanField("NP",default=False)
    useofenglish_na = models.BooleanField(default=False)

    listenning = models.DecimalField(max_digits=3,decimal_places=0,default=0)
    listenning_np = models.BooleanField("NP",default=False)
    listenning_na = models.BooleanField(default=False)

    speaking = models.DecimalField(max_digits=3,decimal_places=0,default=0)
    speaking_np = models.BooleanField("NP",default=False)
    speaking_na = models.BooleanField(default=False)

    comportamiento = models.CharField(max_length=2,default="B")
    comportamiento_np = models.BooleanField("NP",default=False)
    comportamiento_na = models.BooleanField(default=False)
    def ver_legacy_faltas(self):
        try:
            return self.asistencia.legacyfalta_set.all()[0].__unicode__()
        except:
            return "-/-"
    def media(self):
        print self.asistencia.grupo.curso.tipo_evaluacion
        if self.asistencia.grupo.curso.tipo_evaluacion == 2: #"elementary_intermediate":
            lista_materias = ['reading', 'grammar', 'writing', 'speaking', 'listenning']

        elif self.asistencia.grupo.curso.tipo_evaluacion == 3: #"upper_proficiency":
            lista_materias = ['reading', 'useofenglish', 'writing', 'speaking', 'listenning']

        else:
            lista_materias = ['grammar']
        lista_notas = []
        print lista_materias,self.grammar
        for materia in lista_materias:
            # ~ print "miramos si %s tiene na"%materia,getattr(n,"%s_na"%materia)
            nota_temp = getattr(self, materia)
            print "hemos leido",nota_temp
            lista_notas.append(nota_temp)
                # ~ print "Lista", lista_notas
        total = float(0)
        for nota in lista_notas:
            total = total + float(nota)
        numero = float(len(lista_notas))
        media = (total / numero)
        print "Total, numero notas, media", total, numero, media
        return media

        #nota_final = nota_media(lista_notas)


class NotaCuatrimestral(models.Model):
    asistencia = models.ForeignKey('Asistencia')
    cuatrimestre = models.DecimalField(max_digits=1, decimal_places=0)
    fecha_creacion = models.DateField(auto_now_add=True)

    grammar = models.DecimalField(max_digits=3, decimal_places=0, default=0)
    grammar_np = models.BooleanField("NP", default=False)

    reading = models.DecimalField(max_digits=3, decimal_places=0, default=0)
    reading_np = models.BooleanField("NP", default=False)

    writing = models.DecimalField(max_digits=3, decimal_places=0, default=0)
    writing_np = models.BooleanField("NP", default=False)

    reading_writing = models.DecimalField(max_digits=3, decimal_places=0, default=0)
    reading_writing_np = models.BooleanField("NP", default=False)

    useofenglish = models.DecimalField(max_digits=3, decimal_places=0, default=0)
    useofenglish_np = models.BooleanField("NP", default=False)

    listenning = models.DecimalField(max_digits=3, decimal_places=0, default=0)
    listenning_np = models.BooleanField("NP", default=False)

    speaking = models.DecimalField(max_digits=3, decimal_places=0, default=0)
    speaking_np = models.BooleanField("NP", default=False)


    def media(self):
        print self.asistencia.grupo.curso.tipo_evaluacion
        if self.asistencia.grupo.curso.tipo_evaluacion == 2:  # "elementary_intermediate":
            lista_materias = ['reading', 'grammar', 'writing', 'speaking', 'listenning']

        elif self.asistencia.grupo.curso.tipo_evaluacion == 3:  # "upper_proficiency":
            lista_materias = ['reading', 'useofenglish', 'writing', 'speaking', 'listenning']

        else:
            lista_materias = ['grammar']
        lista_notas = []
        print lista_materias, self.grammar
        for materia in lista_materias:
            # ~ print "miramos si %s tiene na"%materia,getattr(n,"%s_na"%materia)
            nota_temp = getattr(self, materia)
            print "hemos leido", nota_temp
            lista_notas.append(nota_temp)
            # ~ print "Lista", lista_notas
        total = float(0)
        for nota in lista_notas:
            total = total + float(nota)
        numero = float(len(lista_notas))
        media = (total / numero)
        print "Total, numero notas, media", total, numero, media
        return media

        # nota_final = nota_media(lista_notas)

class NotaTrimestral(models.Model):
    asistencia = models.ForeignKey('Asistencia')
    trimestre = models.DecimalField(max_digits=1,decimal_places=0)
    fecha_creacion = models.DateField(auto_now_add=True)
    nota = models.DecimalField(max_digits=3,decimal_places=0,default=0)
    observaciones = models.CharField(max_length=500,blank=True,null=True,default="")

class Falta(models.Model):
    asistencia = models.ForeignKey('Asistencia')
    mes = models.DecimalField(max_digits=2,decimal_places=0)
    dia = models.DecimalField(max_digits=2,decimal_places=0)

    def save(self, *args, **kwargs):
        #evitamos duplicar faltas el mismo día por error
        if Falta.objects.filter(asistencia=self.asistencia).filter(mes=self.mes).filter(dia=self.dia).count() > 0:
            print "Ya tiene falta ese día! no la guardamos."
            return
        else:
            super(Falta, self).save(*args, **kwargs)  # Call the "real" save() method.
            #Si el grupo es de menores y suma cinco mandamos mail
            if self.asistencia.grupo.menores:
                print "es un grupo de menores contamos las faltas"
                num_faltas_mes = Falta.objects.filter(asistencia=self.asistencia).filter(mes=self.mes).count()
                print "tiene %s faltas"%num_faltas_mes
                if num_faltas_mes > 3:
                    print "Mandamos mail"
                    subject="[Gestion Alumnos]Aviso de faltas %s en el mes %s"%(self.asistencia.alumno,self.mes)
                    message="El alumno %s en el grupo %s a sobrepasado el ńumero de faltas con un total %s en el mes de %s"% (self.asistencia.alumno,self.asistencia.grupo,num_faltas_mes,self.mes)
                    print "Mandamos mail: %s \n %s"%(subject,message)
                    mail_admins(subject,message)

class Justificada(models.Model):
    asistencia = models.ForeignKey('Asistencia')
    mes = models.DecimalField(max_digits=2,decimal_places=0)
    dia = models.DecimalField(max_digits=2,decimal_places=0)

class LegacyFalta(models.Model):
    asistencia = models.ForeignKey('Asistencia')
    faltas = models.DecimalField(max_digits=3,decimal_places=0)
    justificadas = models.DecimalField(max_digits=3,decimal_places=0)
    def __unicode__(self):
        return "%s/%s"%(self.faltas,self.justificadas)
    
class Presencia(models.Model):
    asistencia = models.ForeignKey('Asistencia')
    mes = models.DecimalField(max_digits=2,decimal_places=0)
    dia = models.DecimalField(max_digits=2,decimal_places=0)

class Recibo(models.Model):
    year = models.ForeignKey('Year')
    fecha_creacion = models.DateField(auto_now_add=True)
    mes = models.DecimalField(max_digits=2,decimal_places=0,choices=MONTHS.items())
    medio_mes = models.BooleanField(default=False)
    grupos_sueltos = models.BooleanField(default=False)
    grupos = models.ManyToManyField(Grupo,blank=True,limit_choices_to=Q(year=Year.objects.get(activo=True)))
    fichero_csb19 = models.TextField(default="",blank=True)
    importe_total = models.FloatField(default=0,blank=True)
    recibos_generados = models.DecimalField(max_digits=4,decimal_places=0,default=0,blank=True)
    metalicos = models.DecimalField(max_digits=4,decimal_places=0,default=0,blank=True)
    errores = models.TextField(default="",blank=True)
    def get_absolute_url(self):
        return reverse_lazy("recibo_detalle",args=[self.id])
    def get_total_alumnos(self):
        if self.grupos_sueltos:
            return self.grupos.all().aggregate(Count('asistencia'))['asistencia__count']
        else:
            return Grupo.objects.filter(year=Year.objects.get(activo=True)).aggregate(Count('asistencia'))['asistencia__count']
    def get_grupos(self):
        if self.grupos_sueltos:
            lista = self.grupos.all()
        else:
            lista = Grupo.objects.filter(year=Year.objects.get(activo=True))
        return lista
    
    def get_alumnos(self):
        return Asistencia.objects.filter(grupo__in=self.get_grupos()).order_by('alumno__cuenta_bancaria')
    
    def get_alumnos_recibo(self):
        return Asistencia.objects.filter(grupo__in=self.get_grupos()).filter(metalico=False).order_by('alumno__cuenta_bancaria')
        
    def get_alumnos_metalico(self):
        return Asistencia.objects.filter(grupo__in=self.get_grupos()).filter(metalico=True)
        
    def get_alumnos_factura(self):
        return Asistencia.objects.filter(grupo__in=self.get_grupos()).filter(factura=True)
        
    def csb19(self):
        fichero_csb19=""
        hoy=datetime.date.today()
        fecha_confeccion=self.fecha_creacion.strftime('%d%m%y')
        fecha_cargo=hoy.strftime('%d%m%y')
        importe_recibos=0
        numero_recibos=0
        
        #~ logging.debug( "Vamos a facturar el día %s en concepto de %s"%(fecha_cargo,fecha_confeccion) )
        #Vamos con la cabecera del presentador
        fichero_csb19=csb19_crear_presentador(fecha_confeccion)
        #Vamos con la cabecera del ordenante
        fichero_csb19=csb19_crear_ordenante(fichero_csb19,fecha_confeccion,fecha_cargo)
        # Ahora los cargos
        lista_grupos = self.get_grupos()
        for grupo in lista_grupos:
            for asistencia in grupo.asistencia_set.all():
                print "Generamos cobro para la asistencia",asistencia
                if asistencia.metalico:
                    print "Paga en metalico"
                    self.metalicos=+1
                else:
                    fichero_csb19,importe_recibos,numero_recibos,error = csb19_crear_individual(fichero_csb19,importe_recibos,numero_recibos,asistencia,self.mes,self.medio_mes)
                    self.importe_total=+importe_recibos
                    self.recibos_generados=+numero_recibos
                    if len(error) > 0:
                        self.errores=self.errores+"<br />"+error

        print "Hemos creado %s recibos que sumanan un total de %s €"%(self.recibos_generados,self.importe_total)
        self.save()
        fichero_csb19 = csb19_crear_totales(fichero_csb19,numero_recibos,importe_recibos)
        return fichero_csb19

class Festivo(models.Model):
    year = models.ForeignKey('Year')
    fecha = models.DateField()
    anotacion = models.CharField(max_length=50,default="")
    tipo = models.DecimalField(max_digits=1, decimal_places=0,choices=TIPO_FESTIVO)
    class Meta:
        ordering = ['fecha']

class TurismoCurso(models.Model):
    year = models.ForeignKey('Year')
    nombre = models.CharField(max_length=50,default="")
    def __unicode__(self):
        return "%s - %s"%(self.year,self.nombre)

class TurismoAsignatura(models.Model):
    curso = models.ForeignKey('TurismoCurso',related_name='asignaturas')
    nombre = models.CharField(max_length=50,default="")
    profesor = models.ForeignKey('Profesor')
    def __unicode__(self):
        return "%s - %s"%(self.curso,self.nombre)

class TurismoAsistencia(models.Model):
    asignatura = models.ForeignKey('TurismoAsignatura')
    alumno = models.ForeignKey('Alumno')
    def __unicode__(self):
        return "%s-%s"%(self.asignatura,self.alumno)

class TurismoClase(models.Model):
    dia_semana = models.DecimalField(max_digits=1, decimal_places=0,choices=DIAS_SEMANA)
    aula = models.ForeignKey(Aula,related_name='clases_turismo')
    profesor = models.ForeignKey(Profesor,related_name='clases_turismo')
    asignatura = models.ForeignKey(TurismoAsignatura,related_name='clases_turismo')
    hora_inicio = models.TimeField(auto_now=False, auto_now_add=False)
    hora_fin = models.TimeField(auto_now=False, auto_now_add=False)
    def __unicode__(self):
        return "%s/%s-%s"%(self.get_dia_semana_display(),self.hora_inicio,self.hora_fin)


