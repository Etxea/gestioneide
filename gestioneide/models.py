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
from anymail.message import AnymailMessage
from django.template.loader import render_to_string

import logging
logger = logging.getLogger('gestioneide.debug')
debug = logger.debug

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
    (2, _('Elementary/Pre Intermediate')),
    (3, _('Intermediate')),
    (4, _('Upper/[Pre]First/Advance/Proficiency')),
    (5, _('Kids')),
)

RESULTADOS_CAMBRIDGE = (
    (1,_('A: Sobresaliente')),
    (2,_('B: Notable')),
    (3,_('C: Aprobado')),
    (4,_('D: Suspendido')),
)

NIVELES_CAMBRIDGE = (
    (1,_('KET')),
    (2,_('PET')),
    (3,_('FCE')),
    (4,_('CAE')),
    (5,_('CPE')),
)

LISTA_MATERIAS_TIPO_EVALUACION = {
    2: ['reading_writing','speaking','listening' ],
    3: ['reading','writing','speaking','listening'],
    4: ['reading','writing','speaking','listening','useofenglish'],
    5: ['']
}

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
    (270, _('4h y 1/2'))   )

NOTAS_KIDS = (
    (0,_('No Aplica')),
    (1,_('Mejorable')),
    (2,_('Satisfactorio')),
    (3,_('Muy Satisfactorio'))
)

COMPORTAMIENTO_KIDS = (
    (0,_('Malo')),
    (1,_('Regular')),
    (2,_('Bueno')),
    (3,_('Excelente'))
)

class Year(models.Model):
    start_year = models.DecimalField(max_digits=4,decimal_places=0,default=2015)
    name = models.CharField(max_length=8,default="201X-1X")
    activo = models.BooleanField(default=1)

    def __unicode__(self):
        return "%s"%self.name
    
    def __str__(self):
        return self.__unicode__()

    def get_activo_global(self):
        return Year.objects.get(activo=True)

    def get_activo(self, request=None):
        if request:
            try:
                perfil = Perfil.objects.get(user=request.user)
                return perfil.ano_activo
            except Exception as e:
                #print e
                return Year.objects.get(activo=True)
        else:
            return Year.objects.get(activo=True)

class CuentaBancaria(models.Model):
    nombre = models.CharField('Nombre',max_length=50)
    banco = models.DecimalField(max_digits=4, decimal_places=0,default=2095)
    oficina = models.DecimalField(max_digits=4, decimal_places=0,default="0553")
    dc = models.DecimalField(max_digits=2, decimal_places=0,default=00)
    cuenta= models.DecimalField(max_digits=10, decimal_places=0,default=0000000000)

    def __unicode__(self):
        return "%s"%self.nombre

    def get_oficina(self):
        return str(csb19_ajustar(self.oficina,4))

    def get_banco(self):
        return str(csb19_ajustar(self.banco,4))

    def get_dc(self):
        return str(csb19_ajustar(self.dc,2))

    def get_cuenta(self):
        return str(csb19_ajustar(self.cuenta,10))

class Empresa(models.Model):
    nombre = models.CharField('Nombre',max_length=255)
    telefono = models.CharField(max_length=12,default="")
    email = models.EmailField(default="",blank=True,null=True)
    direccion = models.CharField(max_length=250,default="",blank=True,null=True)
    razon_social= models.CharField('Razón Social',max_length=255,default="ESCUELAS INTERNACIONALES E.I.D.E.  S.L.")
    cif = models.CharField(max_length=9,default='B12345678')
    csb19_suffijo = models.DecimalField(max_digits=3, decimal_places=0, default=000)
    cuenta_bancaria = models.ForeignKey(CuentaBancaria,blank=True,null=True)

    def get_sufijo(self):
        return str(csb19_ajustar(self.csb19_suffijo,3))

    def __unicode__(self):
        return "%s"%self.nombre

class Centro(models.Model):
    empresa = models.ForeignKey(Empresa,blank=True,null=True)
    nombre = models.CharField('Nombre',max_length=255)
    telefono = models.CharField(max_length=12, default="")
    email = models.EmailField(default="", blank=True, null=True)
    direccion = models.CharField(max_length=250, default="", blank=True, null=True)

    def __unicode__(self):
        return "%s"%self.nombre
    
class Aula(models.Model):
    centro = models.ForeignKey(Centro,blank=True,null=True)
    nombre = models.CharField('Nombre',max_length=255,)
    aforo = models.DecimalField(max_digits=3, decimal_places=0)
    pdi = models.BooleanField(default=False,blank=True)
    def __unicode__(self):
         return "%s"%(self.nombre)
    def __str__(self):
        return self.__unicode__()     
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
            grupos = Grupo.objects.filter(year=Year().get_activo())
            for cuarto in [0,30]:
                fecha_consulta = datetime.time(hora,cuarto)
                programacion_hora = ["%02d:%02d"%(hora,cuarto)]
                for dia in range(1,6):
                    print(dia)
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
    telefono = models.CharField(max_length=12,default="")
    email = models.EmailField(default="",blank=True,null=True)

    def __unicode__(self):
        return "%s"%(self.nombre)

    def __str__(self):
        return self.__unicode__()

    def get_absolute_url(self):
        return "/profesores/%s/"%self.id

    def update_user_password(self):
        password = User.objects.make_random_password()
        self.user.set_password(password)
        self.user.save()
        mensaje = u"""Acabamos de crear o modificar la contraseña para el sistema de
        gestión de alumnos de EIDE. 

        Los datos de acceso son:
        https://gestion.eide.es
        usuario: %s
        contraseña: %s
        Guarda en lugar seguro estos datos por favor."""%(self.user.username,password)
        print(self.nombre,self.user.username,password)

        self.user.email_user("Cambio contraseña en gestion de alumnos EIDE",mensaje)
        #send_mail(u"Cambio contraseña en gestion de alumnos EIDE",mensaje,settings.DEFAULT_FROM_EMAIL,['eide@eide.es','moebius1984@gmail.com'])

    def create_user(self):
        try:
            pg = Group.objects.get(name="profesores")            
        except:
            pg = Group(name="profesores")
            pg.save()
        if self.user == None:
            password = User.objects.make_random_password()  # type: unicode
            nombreusuario = slugify("%s%s" % (self.nombre,self.apellido)).replace('-', '')
            print("No hay usuario asociado para ", nombreusuario, "con el pass ", password)
            if len(User.objects.filter(username=nombreusuario))>0:
                print("Pero ya existe el usuario %s y lo asociamos"%nombreusuario)
                self.user = User.objects.get(username=nombreusuario)
                self.save()
                return
            try:
                u = User(username=nombreusuario,email=self.email)
                u.save()
            except Exception as e:
                print("No hemos podido crearlo")
                print(e)
                return
            u.set_password(password)
            u.groups.add(pg)
            u.save()
            mensaje = u"""Acabamos de crear un usuario para el nuevo sistema de
            gestión de alumnos de EIDE. Los datos de acceso son:
            https://gestion.eide.es/
            usuario: %s
            contraseña: %s
            Guarda en lugar seguro estos datos por favor.
            """%(nombreusuario,password)
            self.user=u
            self.save()
            u.email_user("Alta en gestion de alumnos EIDE",mensaje)
            send_mail(u"Alta en gestion de alumnos EIDE",mensaje,settings.DEFAULT_FROM_EMAIL,['eide@eide.es','moebius1984@gmail.com'])
        else:
            print('El profesor %s Ya tiene un usuario %s'%(self,self.user))

    def grupos(self):
        return Grupo.objects.filter(clases__in=Clase.objects.filter(profesor=self))

    def programacion_semana(self):
        tabla_clases = []
        for hora in range(8,22):
            #print "Vamos con la hora %s"%hora
            grupos = Grupo.objects.filter(year=Year().get_activo())
            for cuarto in [0,30]:
                fecha_consulta = datetime.time(hora,cuarto)
                #print "Vamos con la fecha de consulta %s"%(fecha_consulta)
                programacion_hora = ["%02d:%02d"%(hora,cuarto)]
                for dia in range(1,6):
                    print(dia)
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
            print("No podemos agregar fecha asi que a mano")
            for p in self.user.asistencia_set.filter(contabilizado=False):
                print("Sumamos ",p.duracion)
                pendiente_horas = pendiente_horas + p.duracion.hour
                pendiente_minutos = pendiente_minutos + p.duracion.minute
        print("Tenemos %s:%s"%(pendiente_horas,pendiente_minutos))
        pendiente_horas = pendiente_horas + pendiente_minutos/60
        pendiente_minutos = pendiente_minutos%60
        print("Tenemos %s:%s"%(pendiente_horas,pendiente_minutos))
        return "%s:%s"%(pendiente_horas,pendiente_minutos)

class Alumno(models.Model):
    nombre = models.CharField(max_length=25,default="")
    apellido1 = models.CharField(max_length=100,default="")
    apellido2 = models.CharField(max_length=100,default="",blank=True,null=True)
    fecha_nacimiento = models.DateField(default=datetime.date.today,blank=True)
    fecha_creacion = models.DateField(default=datetime.date.today)
    telefono1 = models.CharField(max_length=12,default="")
    telefono2 = models.CharField(max_length=12,default="",blank=True,null=True)
    email = models.EmailField(default="",blank=True,null=True)
    email2 = models.EmailField(default="",blank=True,null=True)
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
    
    def __str__(self):
        return self.__unicode__()

    def __unicode__(self):
    #    return "%s %s (%s)"%(self.user.get_short_name(),self.user.last_name,self.user.username)
        return "%s %s %s,%s"%(self.id,self.apellido1,self.apellido2,self.nombre)

    def asistencia_todas(self):
        return Asistencia.all_objects.filter(alumno=self)
    
    def get_absolute_url(self):
        return reverse_lazy("alumno_detalle",args=[self.id])
    
    def validate_cuenta_bancaria(self):
        return True
    
    def grupos(self):
        ret = ""
        for asis in self.asistencia_set.all():
            ret = ret + " %s"%asis.grupo.nombre
        return ret
    
    def enviar_mail_sendinblue(self,titulo,mensaje): 
        try:
            send_mail(titulo, mensaje,
            settings.DEFAULT_FROM_EMAIL, [self.email,self.email2])
            return True
        except:
            return False
    
    def enviar_mail(self,titulo,mensaje,mensaje_html=False,adjunto=None,from_email=None):
        if self.email2:
            mails_destino = [ self.email , self.email2 ]
        else:
            mails_destino = [ self.email ]
        email = AnymailMessage(
            subject=titulo,
            body=mensaje,
            to = mails_destino,
        )
        if from_email is not None:
            email.from_email = from_email
        
        if mensaje_html:
            #email.attach_alternative(html_content, "text/html")
            email.content_subtype = "html"

        if adjunto:
            email.attach("adjunto.pdf",adjunto,"application/pdf")
        try:
            email.send(fail_silently=False)
            
            status = email.anymail_status  # available after sending
            
            #print status.message_id  # e.g., '<12345.67890@example.com>'
            #print status.message_id
            #print status.recipients
            print status.esp_response
            return True
        except Exception, e:
            print("Error al enviar mail",str(e))
            return False

    def enviar_mails_pendientes(self):
        for mail in self.mailalumno_set.filter(enviado=False):
            mail.enviado = mail.alumno.enviar_mail(titulo=mail.titulo,mensaje=mail.mensaje)
            mail.save()
    
    def enviar_sms(self):
        
        return True

class Historia(models.Model):
    alumno = models.ForeignKey('Alumno')
    fecha = models.DateTimeField(auto_now_add=True)
    tipo = models.CharField(max_length=25,default="")
    anotacion = models.CharField(max_length=150,default="")
    class Meta:
        ordering = ['-fecha']

class Anotacion(models.Model):
    alumno = models.ForeignKey('Alumno')
    fecha = models.DateField(auto_now_add=True)
    creador = models.ForeignKey(User)#, editable=False)
    texto = models.CharField(max_length=500,default="")
    class Meta:
        ordering = ['-fecha']

class MailAlumno(models.Model):
    alumno = models.ForeignKey('Alumno')
    enviado = models.BooleanField(default=False)
    fecha = models.DateField(auto_now_add=True)
    creador = models.ForeignKey(User)#, editable=False)
    titulo = models.CharField(max_length=100,default="") 
    mensaje = models.CharField(max_length=500,default="")
    mensaje_html = models.CharField(max_length=500,default="")
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
    def __str__(self):
        return self.__unicode__()
    class Meta:
        ordering = ["nombre"]

class Grupo(models.Model):
    year = models.ForeignKey('Year')
    centro = models.ForeignKey(Centro,default=1,blank=True,null=True)
    nombre = models.CharField(max_length=25,default="")
    curso = models.ForeignKey('Curso')
    precio  = models.DecimalField(max_digits=3,decimal_places=0,default=0)
    num_max = models.DecimalField(max_digits=2,decimal_places=0,default=14) #El tamano default no es lo mejor que este aqui, pero bueno
    menores = models.BooleanField(default=False)
    
    class Meta:
        ordering = ["nombre"]
        permissions = [
            ("send_email_grupo", "Send e-mail to group students"),
            ("view_data_grupo", "View group data"),
        ]
    
    def ver_precio(self):
        if self.precio:
            return self.precio
        else:
            return self.curso.precio
    
    def get_absolute_url(self):
        return reverse_lazy("grupo_detalle",args=[self.id]) 
    
    def confirmados(self):
        return self.asistencia_set.filter(confirmado=True).filter(borrada=False).count()
    
    def sin_confirmar(self):
        return self.asistencia_set.filter(confirmado=False).filter(borrada=False).count()
    
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
        year = Year().get_activo()
        if cuatrimestre:
            filtro = Grupo.objects.filter(year=year).annotate(Count('asistencia')).filter(asistencia__count__gt=0).order_by('nombre')
        else:
            filtro = Grupo.objects.filter(year=year).annotate(Count('asistencia')).filter(asistencia__count__gt=0).order_by('nombre')
        posicion = int(filtro.filter(nombre__lt = self.nombre).count())
        total = len(filtro)
        print("Somo el %s de %s"%(posicion,total))
        if posicion == total:
            return self.id
        else:
            return filtro[posicion+1].id

    def next_by_nombre_quatrimestre(self):
        self.next_by_nombre(cuatrimestre=True)

    def prev_by_nombre(self,cuatrimestre=False):
        year = Year().get_activo()
        if cuatrimestre:
            filtro = Grupo.objects.filter(year=year).annotate(Count('asistencia')).filter(
                asistencia__count__gt=0).order_by('nombre')
        else:
            filtro = Grupo.objects.filter(year=year).annotate(Count('asistencia')).filter(
                asistencia__count__gt=0).order_by('nombre')

        posicion=0
        posicion = filtro.filter(nombre__lt = self.nombre).count()
        total = len(filtro)
        print("Somo el %s de %s"%(posicion,total))
        if posicion == 0:
            return self.id
        else:
            if cuatrimestre:
                #return Grupo.objects.filter(year=year).annotate(Count('asistencia')).filter(asistencia__count__gt=0).order_by('nombre')[posicion-1].id
                return 0
            else:
                return Grupo.objects.filter(year=year).annotate(Count('asistencia')).filter(asistencia__count__gt=0).order_by('nombre')[posicion-1].id

    def envio_notas_email(self, tipo, trimestre ):
        #print "Se van a enviar las notas de tipo %s y del cua/trimestre %s"%(tipo,trimestre)
        for asistencia in self.asistencia_set.all():
            if tipo == "trimestre":
                #print "Enviamos la del trimestre %s"%trimestre
                nota_model = NotaTrimestral.objects.get(asistencia=asistencia,trimestre=trimestre)
                nota_model.enviar_mail()
            elif tipo == "cuatrimestre":
                nota_model = NotaCuatrimestral.objects.get(asistencia=asistencia,cuatrimestre=trimestre)
                #print nota_model
                #print "Enviamos la del cuatrimestre %s "%trimestre
                nota_model.enviar_mail()
            else:
                print "tipo desconocido. No hacemos nada"
                break
            
    def prev_by_nombre_quatrimestre(self):
        self.prev_by_nombre(cuatrimestre=True)
    
    def __unicode__(self):
        return "%s - %s"%(self.nombre,self.year)
    
    def get_absolute_url(self):
        return reverse_lazy("grupo_detalle",args=[self.id])
        
    def get_dias_clase_mes(self,mes):
        dias_semana_clase = []
        dias_clase = []
        for dia in self.clases.all():
            dias_semana_clase.append(dia.dia_semana)
        print(dias_semana_clase)
        year = Year().get_activo()
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

    def __str__(self):
        return self.__unicode__()

class AnotacionGrupo(models.Model):
    grupo = models.ForeignKey('Grupo')
    fecha = models.DateField(auto_now_add=True)
    creador = models.ForeignKey(User)
    texto = models.CharField(max_length=1000,default="")
    class Meta:
        ordering = ['-fecha']

class Clase(models.Model):
    dia_semana = models.DecimalField(max_digits=1, decimal_places=0,choices=DIAS_SEMANA)
    aula = models.ForeignKey(Aula,related_name='clases')
    profesor = models.ForeignKey(Profesor,related_name='clases')
    grupo = models.ForeignKey(Grupo,related_name='clases')
    hora_inicio = models.TimeField(auto_now=False, auto_now_add=False)
    hora_fin = models.TimeField(auto_now=False, auto_now_add=False)
    video_url = models.URLField(max_length=200,blank=True)
    def __unicode__(self):
        return "%s/%s-%s/%s"%(self.get_dia_semana_display(),self.hora_inicio,self.hora_fin,self.profesor)

class AsistenciaManager(models.Manager):
    def get_queryset(self):
        return super(AsistenciaManager, self).get_queryset().filter(borrada=False)

class Asistencia(models.Model):
    year = models.ForeignKey('Year')
    #El limit debería tener en cuenta el ano del perfil del usuario, pero como no tenemos request no se puede hacer aquí, habrá que pasarlo al FORM
    grupo = models.ForeignKey('Grupo')#,limit_choices_to=Q(year=Year().get_activo())) #Comentar el limit choices para un primer import
    alumno = models.ForeignKey('Alumno')
    confirmado = models.BooleanField(default=False)
    factura = models.BooleanField(default=False)
    metalico = models.BooleanField(default=False)
    precio = models.FloatField(null=True,blank=True)
    borrada = models.BooleanField(default=False)
    objects = AsistenciaManager()
    all_objects = models.Manager() # The default manager.

    def __unicode__(self):
        return u"(%s) %s -> %s"%(self.year,self.alumno,self.grupo)

    def __str__(self):
        return self.__unicode__()    

    #Override del save para anotar en la historia los cambios
    def save(self, *args, **kwargs):
        # Guardamos en la historia
        if self.pk is None:
            active_year = Year().get_activo()
            try:
                debug("Tenemos el año %s"%(self.year))
                self.year = active_year
            except:
                self.year = active_year
            hist = Historia(alumno=self.alumno, tipo="altagrupo",
                            anotacion="Alta en el grupo")
            hist.save()
        elif self.borrada is True:
            hist = Historia(alumno=self.alumno, tipo="bajagrupo",
                            anotacion="Baja del grupo %s ano %s" % (self.grupo.nombre,self.year))
            hist.save()
        else:
            hist = Historia(alumno=self.alumno, tipo="cambiogrupo",
                            anotacion="Editados datos de la asistencia")
            hist.save()
        super(Asistencia, self).save(*args, **kwargs)

    #Override del metodo delete para hacer borrado lógico
    def delete(self, *args, **kwargs):
        self.borrada = True
        self.save()

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
        trimestre = int(trimestre)
        meses = []
        if trimestre==1:
           meses = [9,8,10,11,12]
        elif trimestre==2:
           meses = [1,2,3]
        elif trimestre==2:
           meses = [4,5,6]
        return Falta.objects.filter(asistencia=self).filter(mes__in=meses).count()

    def faltas_finales(self):
        return Falta.objects.filter(asistencia=self).count()

    def justificadas_trimestre(self,trimestre):
        trimestre = int(trimestre)
        meses = []
        if trimestre==1:
           meses = [9,8,10,11,12]
        elif trimestre==2:
           meses = [1,2,3]
        elif trimestre==2:
           meses = [4,5,6]
        return self.justificada_set.filter(mes__in=meses).count()

    def justificadas_finales(self):
        return Justificada.objects.filter(asistencia=self).count()

    def get_nota_trimestre(self,trimestre):
        nota = "-"
        notaquery = self.notatrimestral_set.filter(trimestre=trimestre)
        if notaquery.count() > 0:
            if notaquery[0].np == True:
                nota = "NP"
            else:
                nota = notaquery[0].nota
        return nota
    def get_nota_trimestre_obj(self,trimestre):
        nota = None
        notaquery = self.notatrimestral_set.filter(trimestre=trimestre)
        if notaquery.count() > 0:
            nota = notaquery[0]
        return nota

    def get_np_trimestre(self,trimestre):
        nota = "0"
        notaquery = self.notatrimestral_set.filter(trimestre=trimestre)
        if notaquery.count() > 0:
            np = notaquery[0].np
        else:
            np = False
        return np

    def get_observaciones_trimestre(self,trimestre):
        observaciones = ""
        notaquery = self.notatrimestral_set.filter(trimestre=trimestre)
        if notaquery.count() > 0:
            observaciones = notaquery[0].observaciones
        return observaciones

    def get_aspectos_mejorar_trimestre(self,trimestre):                                                              
        observaciones = ""
        notaquery = self.notatrimestral_set.filter(trimestre=trimestre)
        if notaquery.count() > 0:
            observaciones = notaquery[0].aspectos_mejorar
        return observaciones

    def get_temas_repasar_trimestre(self,trimestre):                                                              
        observaciones = ""
        notaquery = self.notatrimestral_set.filter(trimestre=trimestre)
        if notaquery.count() > 0:
            observaciones = notaquery[0].temas_repasar
        return observaciones

    def get_observaciones_cuatrimestre(self,cuatrimestre):
        observaciones = ""
        notaquery = self.notacuatrimestral_set.filter(cuatrimestre=cuatrimestre)
        if notaquery.count() > 0:
            observaciones = notaquery[0].observaciones
        return observaciones

    def nota_trimestre(self,trimestre):
        nota = self.get_nota_trimestre(trimestre)
        np = self.get_np_trimestre(trimestre)
        observaciones = self.get_observaciones_trimestre(trimestre)
        return nota,observaciones,np

    def get_nota_media_cuatrimestre(self,cuatrimestre):
        nota = "0"
        notaquery = self.notacuatrimestral_set.filter(cuatrimestre=cuatrimestre)
        if notaquery.count() > 0:
            nota = notaquery[0].media()
        return nota

    def get_notas_cuatrimestre(self,cuatrimestre):
        nota = {}
        notaquery = self.notacuatrimestral_set.filter(cuatrimestre=cuatrimestre)
        if notaquery.count() > 0:
            nota = notaquery[0].notas_materias()
        else:
            print("No hemos encontrado notas de %s en el %s"%(self,cuatrimestre))
            lista_materias = LISTA_MATERIAS_TIPO_EVALUACION[self.grupo.curso.tipo_evaluacion]
            for materia in lista_materias:
                nota[materia]="--"
        return nota

    def get_nota_materia_cuatrimestre(self,cuatrimestre,materia):
        nota = "0"
        notaquery = self.notacuatrimestral_set.filter(cuatrimestre=cuatrimestre)
        if notaquery.count() > 0:
            if getattr(notaquery[0],"%_np"%materia):
                nota = "NP"
            else:
                nota = getattr(notaquery[0],materia)
        return nota

    def nota_final(self):
        if NotaCuatrimestral.objects.filter(asistencia=self, cuatrimestre=2).count() > 0:
            nota = self.get_nota_media_cuatrimestre(2)
            tipo = "C"
        elif NotaTrimestral.objects.filter(asistencia=self, trimestre=3).count() > 0:
            nota = self.get_nota_trimestre(3)
            tipo = "T"
        else:
            nota = "-"
            tipo = "-"

        nota_final = { "media": nota, "tipo": tipo, "faltas": self.faltas_finales(), "justificadas": self.justificadas_finales() }
        return nota_final

    def __unicode__(self):
        return "%s"%(self.alumno.id)

class PruebaNivel(models.Model):
    alumno = models.ForeignKey('Alumno')
    fecha_creacion = models.DateField(auto_now_add=True)
    resultado = models.DecimalField(max_digits=2,decimal_places=0,default=0)
    nivel_recomendado = models.ForeignKey('Curso')
    observaciones = models.TextField(max_length=350,default="")

class ResultadoCambridge(models.Model):
    alumno = models.ForeignKey('Alumno')
    ano = models.DecimalField(max_digits=4,decimal_places=0,default=2016)
    nivel = models.DecimalField(max_digits=1,decimal_places=0,default=1,choices=NIVELES_CAMBRIDGE)
    resultado = models.DecimalField(max_digits=2,decimal_places=0,default=1,choices=RESULTADOS_CAMBRIDGE)
    observaciones = models.TextField(max_length=350,default="")

class GrupoNotasParciales(models.Model):
    fecha_creacion = models.DateField(auto_now_add=True)
    grupo = models.ForeignKey('Grupo', related_name="notas_parciales")
    nombre = models.CharField(max_length=25)

class NotaParcial(models.Model):
    grupo_notas_parciales = models.ForeignKey('GrupoNotasParciales')
    asistencia = models.ForeignKey('Asistencia')
    nota = models.DecimalField(max_digits=3,decimal_places=0,default=0)

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

    listening = models.DecimalField(max_digits=3,decimal_places=0,default=0)
    listening_np = models.BooleanField("NP",default=False)
    listening_na = models.BooleanField(default=False)

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
        #print self.asistencia.grupo.curso.tipo_evaluacion
        if self.asistencia.grupo.curso.tipo_evaluacion == 1: #"elementary_intermediate":
            lista_materias = ['control']

        elif self.asistencia.grupo.curso.tipo_evaluacion == 2: #"elementary_intermediate":
            lista_materias = ['reading', 'grammar', 'writing', 'speaking', 'listening']

        elif self.asistencia.grupo.curso.tipo_evaluacion == 3: #"upper_proficiency":
            lista_materias = ['reading', 'useofenglish', 'writing', 'speaking', 'listening']

        else:
            lista_materias = ['grammar']
        lista_notas = []
        print(lista_materias,self.grammar)
        for materia in lista_materias:
            # ~ print "miramos si %s tiene na"%materia,getattr(n,"%s_na"%materia)
            nota_temp = getattr(self, materia)
            #print "hemos leido",nota_temp
            lista_notas.append(nota_temp)
                # ~ print "Lista", lista_notas
        total = float(0)
        for nota in lista_notas:
            total = total + float(nota)
        numero = float(len(lista_notas))
        media = (total / numero)
        #print "Total, numero notas, media", total, numero, media
        return media

        #nota_final = nota_media(lista_notas)

class NotaCuatrimestral(models.Model):
    asistencia = models.ForeignKey('Asistencia')
    cuatrimestre = models.DecimalField(max_digits=1, decimal_places=0)
    fecha_creacion = models.DateField(auto_now_add=True)
    observaciones = models.CharField(max_length=500,blank=True,null=True,default="")

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

    listening = models.DecimalField(max_digits=3, decimal_places=0, default=0)
    listening_np = models.BooleanField("NP", default=False)

    speaking = models.DecimalField(max_digits=3, decimal_places=0, default=0)
    speaking_np = models.BooleanField("NP", default=False)

    email_enviado = models.BooleanField(default=False)

    def notas_materias(self):
        """Devolvemos un dict con la lista de materias y su nota"""
        lista_materias = LISTA_MATERIAS_TIPO_EVALUACION[self.asistencia.grupo.curso.tipo_evaluacion]
        lista_notas = {}
        for materia in lista_materias:
            if getattr(self,materia+"_np"):
                nota_temp = "NP"
            else:
                nota_temp = getattr(self, materia)
            lista_notas[materia]=nota_temp
        return lista_notas

    def media(self):
        lista_materias = LISTA_MATERIAS_TIPO_EVALUACION[self.asistencia.grupo.curso.tipo_evaluacion]
        lista_notas = []
        for materia in lista_materias:
            # ~ print "miramos si %s tiene na"%materia,getattr(n,"%s_na"%materia)
            try:
                nota_temp = getattr(self, materia)
                lista_notas.append(nota_temp)
            except:
                pass
            # ~ print "Lista", lista_notas
        total = float(0)
        for nota in lista_notas:
            total = total + float(nota)
        if len(lista_notas) > 0:
            numero = float(len(lista_notas))
            media = (total / numero)
        else:
            media = "-"
        return media

        # nota_final = nota_media(lista_notas)
    
    def get_absolute_url(self):
        return reverse_lazy('nota_trimestral_editar', kwargs={'pk': self.pk })
    
    def enviar_mail(self):
        #print("Vamos a enviar los mails de la nota del alumno %s del cuatrimestre %s"%(self.asistencia.alumno,self.cuatrimestre))
        contexto = {}
        contexto['year']=self.asistencia.grupo.year.__unicode__()
        contexto['cuatrimestre']=self.cuatrimestre
        contexto['asistencia']=self.asistencia
        nota_html = render_to_string("alumnos_carta_nota_cuatrimestre.html",contexto,request=None)
        self.asistencia.alumno.enviar_mail("[EIDE] Notas Cuatrimestre",nota_html,mensaje_html=True)
        self.email_enviado = True
        self.save()

class NotaTrimestral(models.Model):
    asistencia = models.ForeignKey('Asistencia')
    trimestre = models.DecimalField(max_digits=1,decimal_places=0)
    fecha_creacion = models.DateField(auto_now_add=True)
    nota = models.DecimalField(max_digits=3,decimal_places=0,default=0)
    np = models.BooleanField("NP", default=False)
    observaciones = models.CharField(max_length=500,blank=True,null=True,default="")
    exp_oral = models.DecimalField("Expresión Oral", max_digits=1, decimal_places=0, choices=NOTAS_KIDS,blank=True,null=True,default=0)
    comp_oral = models.DecimalField("Comprensión Oral", max_digits=1, decimal_places=0, choices=NOTAS_KIDS,blank=True,null=True,default=0)
    exp_escrita = models.DecimalField("Expresión Escrita", max_digits=1, decimal_places=0, choices=NOTAS_KIDS,blank=True,null=True,default=0)
    comp_escrita = models.DecimalField("Comprensión Escrita", max_digits=1, decimal_places=0, choices=NOTAS_KIDS,blank=True,null=True,default=0)
    temas_repasar = models.CharField("Temas a repasar", max_length=200, blank=True, null=True, default="")
    aspectos_mejorar = models.CharField("Aspectos a mejorar", max_length=200, blank=True, null=True, default="")
    email_enviados = models.BooleanField(default=False)
    
    def get_absolute_url(self):
        return reverse_lazy('nota_trimestral_editar', kwargs={'pk': self.pk })

    def enviar_mail(self):
        print("Vamos a enviar los mails de la nota del alumno %s del trimestre %s"%(self.asistencia.alumno,self.trimestre))
        contexto = {}
        contexto['year']=self.asistencia.grupo.year.__unicode__()
        contexto['trimestre']=self.trimestre
        contexto['asistencia']=self.asistencia
        nota_html = render_to_string("alumnos_carta_nota.html",contexto,request=None)
        self.asistencia.alumno.enviar_mail("[EIDE] Notas Trimestre",nota_html,mensaje_html=True)
        self.email_enviado = True
        self.save()

class Falta(models.Model):
    asistencia = models.ForeignKey('Asistencia')
    mes = models.DecimalField(max_digits=2,decimal_places=0)
    dia = models.DecimalField(max_digits=2,decimal_places=0)

    def save(self, *args, **kwargs):
        #evitamos duplicar faltas el mismo día por error
        if Falta.objects.filter(asistencia=self.asistencia).filter(mes=self.mes).filter(dia=self.dia).count() > 0:
            print("Ya tiene falta ese día! no la guardamos.")
            return
        else:
            super(Falta, self).save(*args, **kwargs)  # Call the "real" save() method.
            #Si el grupo es de menores y suma cinco mandamos mail
            if self.asistencia.grupo.menores:
                #print "es un grupo de menores contamos las faltas"
                num_faltas_mes = Falta.objects.filter(asistencia=self.asistencia).filter(mes=self.mes).count()
                #print "tiene %s faltas"%num_faltas_mes
                if num_faltas_mes > 3:
                    #print "Mandamos mail"
                    subject="[Gestion Alumnos]Aviso de faltas %s en el mes %s"%(self.asistencia.alumno,self.mes)
                    message="El alumno %s en el grupo %s a sobrepasado el ńumero de faltas con un total %s en el mes de %s"% (self.asistencia.alumno,self.asistencia.grupo,num_faltas_mes,self.mes)
                    #print "Mandamos mail: %s \n %s"%(subject,message)
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
    empresa = models.ForeignKey('Empresa',default=1)
    fecha_creacion = models.DateField(auto_now_add=True)
    fecha_cargo = models.DateField(auto_now_add=True)
    mes = models.DecimalField(max_digits=2,decimal_places=0,choices=MONTHS.items())
    medio_mes = models.BooleanField(default=False)
    grupos_sueltos = models.BooleanField(default=False)
    grupos = models.ManyToManyField(Grupo,blank=True)#,limit_choices_to=Q(year=Year().get_activo()))
    fichero_csb19 = models.TextField(default="",blank=True)
    importe_total = models.FloatField(default=0,blank=True)
    recibos_generados = models.DecimalField(max_digits=4,decimal_places=0,default=0,blank=True)
    metalicos = models.DecimalField(max_digits=6,decimal_places=0,default=0,blank=True)
    numero_recibos = models.DecimalField(max_digits=6, decimal_places=0, default=0, blank=True)
    importe_recibos = models.FloatField(default=0,blank=True)
    importe_metalico = models.FloatField(default=0, blank=True)
    errores = models.TextField(default="",blank=True)

    def get_absolute_url(self):
        return reverse_lazy("recibo_detalle",args=[self.id])

    def get_total_alumnos(self):
        if self.grupos_sueltos:
            return self.grupos.all().aggregate(Count('asistencia'))['asistencia__count']
        else:
            return Grupo.objects.filter(year=Year().get_activo(), centro__in=self.empresa.centro_set.all()).aggregate(Count('asistencia'))['asistencia__count']

    def get_grupos(self):
        if self.grupos_sueltos:
            lista = self.grupos.all()
        else:
            lista = Grupo.objects.filter(year=Year().get_activo(), centro__in=self.empresa.centro_set.all())
        return lista

    def get_grupos_count(self):
        return len(self.get_grupos())

    def get_alumnos(self):
        return Asistencia.objects.filter(grupo__in=self.get_grupos()).filter(borrada=False).order_by('alumno__cuenta_bancaria')
    
    def get_alumnos_recibo(self):
        return Asistencia.objects.filter(grupo__in=self.get_grupos()).filter(borrada=False).filter(metalico=False).order_by('alumno__cuenta_bancaria')
        
    def get_alumnos_metalico(self):
        return Asistencia.objects.filter(grupo__in=self.get_grupos()).filter(borrada=False).filter(metalico=True)
        
    def get_alumnos_factura(self):
        return Asistencia.objects.filter(grupo__in=self.get_grupos()).filter(borrada=False).filter(factura=True)

    def csb19_crear_presentador(self):
        """Funcion que crea el campo presentador y lo añade al contenido"""
        contenido = ""
        cod_reg = "51"
        cod_dato = "80"
        relleno_b3 = ' ' * 6
        relleno_d = ' ' * (60 - len(self.empresa.nombre))
        relleno_e3 = ' ' * 12
        relleno_f = ' ' * 40
        relleno_g = ' ' * 14
        cabecera_presentador = cod_reg + cod_dato + str(self.empresa.cif) + str(self.empresa.get_sufijo()) + \
                               self.fecha_creacion.strftime("%d%m%y") + relleno_b3 + self.empresa.nombre + relleno_d +\
                               str(self.empresa.cuenta_bancaria.get_banco()) + str(self.empresa.cuenta_bancaria.get_oficina()) + \
                               relleno_e3 + relleno_f + relleno_g + "\r\n"
        self.fichero_csb19 = cabecera_presentador

    def csb19_crear_ordenante(self):
        """Funcion que crea el campo ordenante y lo añade al contenido"""
        cod_reg = "53"
        cod_dato = "80"
        procedimiento = "01"
        relleno_nombre = ' ' * (40 - len(self.empresa.nombre))
        relleno_e1 = ' ' * 8
        relleno_e3 = ' ' * 10
        relleno_f = ' ' * 40
        relleno_g = ' ' * 14
        cabecera_ordenante = cod_reg + cod_dato + str(self.empresa.cif) + str(self.empresa.get_sufijo()) + \
                             self.fecha_creacion.strftime("%d%m%y") + self.fecha_cargo.strftime("%d%m%y") + \
                             self.empresa.nombre + relleno_nombre +\
                             str(self.empresa.cuenta_bancaria.get_banco()) + str(self.empresa.cuenta_bancaria.get_oficina()) + \
                             str(self.empresa.cuenta_bancaria.get_dc()) + str(self.empresa.cuenta_bancaria.get_cuenta()) +\
                             relleno_e1 + procedimiento + relleno_e3 + relleno_f + relleno_g + '\r\n'
        self.fichero_csb19 += cabecera_ordenante

    def csb19_crear_individual(self,asistencia):
        ##Recibimos la asistencia y de ella sacamos: id, nombre, CCC, importe y concepto
        error = ""
        id = asistencia.id
        nombre_cargo = "%s %s" % (asistencia.alumno.apellido1, asistencia.alumno.apellido2)
        nombre_cargo = unidecode(nombre_cargo)
        ccc = asistencia.alumno.cuenta_bancaria.replace("-", "")
        importe_individual = float(0)
        if self.medio_mes:
            importe_individual = float(asistencia.ver_precio()) / 2
        else:
            importe_individual = float(asistencia.ver_precio())
        concepto = u"EIDE: %s, %s" % (asistencia.grupo.nombre, MONTHS[self.mes])
        concepto = unidecode(concepto)
        # Sumamos el importe al total
        self.numero_recibos += 1
        cod_reg = "56"
        cod_dato = "80"
        # relleno de 16
        relleno_f = ' ' * 16
        # relleno de 8
        relleno_h = ' ' * 8
        ##Normalizamos (rellenamos) los campos nombre, importe y concepto
        nombre_cargo = csb19_normalizar(nombre_cargo, 40)
        concepto = csb19_normalizar(concepto, 40)

        # Vamos con el importe
        importe_txt = csb19_ajustar(importe_individual, 10, 2)
        individual = str(cod_reg) + str(cod_dato) + self.empresa.cif + str(self.empresa.get_sufijo()) + \
                     csb19_ajustar(id, 12) + nombre_cargo + \
                     ccc + importe_txt + relleno_f + concepto + relleno_h + '\r\n'

        self.fichero_csb19 += str(individual)
        self.importe_recibos += importe_individual
        self.importe_total += importe_individual
        self.recibos_generados += 1
        if len(error) > 0:
            self.errores += "<br />" + error

    def csb19_crear_total_ordenante(self):
        cod_reg = "58"
        cod_dato = "80"
        relleno_b2 = " " * 12
        relleno_c = " " * 40
        relleno_d = " " * 20
        relleno_e2 = " " * 6
        relleno_f3 = " " * 20
        relleno_g = " " * 18
        importe_recibos = str(self.importe_recibos)
        numero_recibos = int(self.recibos_generados)
        print("Vamos a crear los totales de ordenante de %s € y %s recibos"%(importe_recibos,numero_recibos))
        total_ordenante = str(cod_reg) + str(cod_dato) + str(self.empresa.cif) + str(self.empresa.get_sufijo()) \
                          + relleno_b2 + relleno_c + relleno_d + csb19_ajustar(importe_recibos, 10, 2) \
                          + relleno_e2 + csb19_ajustar(numero_recibos, 10) + csb19_ajustar(numero_recibos+2, 10) + relleno_f3 \
                          + relleno_g + '\r\n'
        self.fichero_csb19 += total_ordenante

    def csb19_crear_total_general(self):
        cod_reg = "59"
        cod_dato = "80"
        relleno_b2 = " " * 12
        relleno_c = " " * 40
        relleno_d2 = " " * 16
        relleno_e2 = " " * 6
        relleno_f3 = " " * 20
        relleno_g = " " * 18
        num_ordenantes = "0001"
        ##FIXME ajustar el formato del importe total
        importe_recibos = str(self.importe_recibos)
        numero_recibos = int(self.recibos_generados)
        print("Vamos a crear los totales generales de %s € y %s recibos"%(importe_recibos,numero_recibos))
        total_general = str(cod_reg) + str(cod_dato) + str(self.empresa.cif) + str(self.empresa.get_sufijo()) + relleno_b2 + \
                        relleno_c + num_ordenantes + relleno_d2 + csb19_ajustar(importe_recibos, 10, 2) + relleno_e2 + \
                        csb19_ajustar(numero_recibos, 10) + csb19_ajustar(numero_recibos+4,10) + relleno_f3 + relleno_g
        self.fichero_csb19 += total_general

    def csb19_crear_totales(self):
        """creamos los totales"""
        self.csb19_crear_total_ordenante()
        self.csb19_crear_total_general()

    def csb19(self):
        #Limpiamos todos los datos
        self.importe_recibos=0
        self.importe_total=0
        self.importe_metalico=0
        self.recibos_generados=0
        self.numero_recibos=0
        self.fichero_csb19=""
        self.save()
        self.fecha_cargo = datetime.date.today()
        #Vamos con la cabecera del presentador
        self.csb19_crear_presentador()
        #Vamos con la cabecera del ordenante
        self.csb19_crear_ordenante()
        # Ahora los cargos
        lista_grupos = self.get_grupos()
        for grupo in lista_grupos:
            for asistencia in grupo.asistencia_set.filter(borrada=False):
                if asistencia.metalico:
                    if self.medio_mes:
                        importe = float(asistencia.ver_precio()) / 2
                    else:
                        importe = float(asistencia.ver_precio())
                    self.metalicos += 1
                    self.importe_metalico += importe
                    self.importe_total += importe
                else:
                    self.csb19_crear_individual(asistencia)

        self.save()
        self.csb19_crear_totales()
        print("Hemos creado %s recibos que sumanan un total de %s €" % (self.recibos_generados, self.importe_total))
        self.save()

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
    curso = models.ForeignKey('TurismoCurso', related_name='asignaturas')
    nombre = models.CharField(max_length=50, default="")
    profesor = models.ForeignKey('Profesor')

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

class TurismoPresencia(models.Model):
    asistencia = models.ForeignKey('TurismoAsistencia')
    mes = models.DecimalField(max_digits=2,decimal_places=0)
    dia = models.DecimalField(max_digits=2,decimal_places=0)

class TurismoFalta(models.Model):
    asistencia = models.ForeignKey('TurismoAsistencia')
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

class TurismoJustificada(models.Model):
    asistencia = models.ForeignKey('TurismoAsistencia')
    mes = models.DecimalField(max_digits=2,decimal_places=0)
    dia = models.DecimalField(max_digits=2,decimal_places=0)

class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ano_activo = models.ForeignKey(Year)
