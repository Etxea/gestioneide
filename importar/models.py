# -*- coding: utf-8 -*-
from django.db import models

from gestioneide.models import Alumno as Alumno_new
from gestioneide.models import Asistencia as Asistencia_new
from gestioneide.models import Year
from gestioneide.models import Libro as Libro_new
from gestioneide.models import Curso as Curso_new
from gestioneide.models import Grupo as Grupo_new
from gestioneide.models import Clase as Clase_new
from gestioneide.models import Aula as Aula_new
from gestioneide.models import Historia as Historia_new
from gestioneide.models import Profesor as Profesor_new

from sqlobject import *
from sqlobject.inheritance import InheritableSQLObject
import sys, datetime
import logging

import unicodedata
def elimina_tildes(s):
   return ''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))
 

dias = {'lunes': 1, 'martes': 2, 'miercoles': 3, "jueves":4, "viernes": 5}


logger = logging.getLogger('gestioneide.error')

class OldDatabase(models.Model):
    dbfile = models.FileField(upload_to='old_databases/%Y/%m/%d')
    imported = models.BooleanField(default=False) 
    message = models.CharField(max_length=500,default="")
    errors = models.CharField(max_length=500,default="")
    def addMessage(self,text):
        logger.error(text)
        self.message = self.message + text
    def addError(self,text):
        logger.error(text)
        self.errors = self.errors + text
    def doImport(self):
        self.message="<ul>"
        self.error="<ul>"
        year = Year.objects.get(activo=True)
        
        self.addMessage('<li>Iniciando importacion desde archivo %s </li>'%self.dbfile.path)
        sqlhub.processConnection = connectionForURI('sqlite://'+self.dbfile.path)
        
        from gestioneide.old_database_model import *

        
        self.addMessage('<li>Importamos los libros, primero vamos a vaciar la BBDD</li>')
        Libro_new.objects.all().delete()
        busqueda = Libro.select()
        
        self.addMessage('<li>Encontrados %d libros</li>'%busqueda.count())
        for libro in busqueda:
            if not libro.autor:
                autor = ""
            else:
                autor=libro.autor
            
            l = Libro_new(\
                id = libro.id,\
                titulo=libro.titulo,\
                autor=autor,\
                isbn=libro.isbn,\
                editorial=str(libro.editorial),\
            )
            l.save()

        
        self.addMessage('<li>Importamos las aulas, primero vamos a vaciar la BBDD</li>')
        Aula_new.objects.all().delete()
        busqueda = Aula.select()
        
        self.addMessage('<li>Encontrados %d aulas</li>'%busqueda.count())
        for aula in busqueda:
            a = Aula_new(\
                id=aula.id,\
                nombre="%s"%aula.numero,\
                aforo=aula.aforo,\
                pdi=False,\
                
            )
            a.save()
        
        
        self.addMessage('<li>Importamos los cursos, primero vamos a vaciar la BBDD</li>')
        Curso_new.objects.all().delete()
        busqueda = Curso.select()
        self.addMessage('<li>Encontrados %d cursos</li>'%busqueda.count())
        for curso in busqueda:
            if curso.modelo_notas == "elementary_intermediate":
                tipo_evaluacion=2
            elif curso.modelo_notas == "upper_proficiency":
                tipo_evaluacion=3
            else:
                tipo_evaluacion=1
            c = Curso_new(\
                nombre = curso.nombre,\
                precio = curso.precio,\
                ##No obligatorios
                examen = curso.examen,\
                nivel = curso.nivel,\
                nota_aprobado = curso.nota_aprobado,\
                solo_examen_final = curso.solo_examen_final,\
                tipo_evaluacion=tipo_evaluacion,\
            )
            c.save()
            for libro in curso.libros:
                try:
                    c.libros.add(Libro_new.objects.get(id=libro.id))
                except:
                    self.addError("No se ha podido anadir el libro %s al curso %s"%(libro.id,c.id))
                    print sys.exc_info()

                            
        self.addMessage('<li>Importamos los profesores, primero vamos a vaciar la BBDD</li>')
        Profesor_new.objects.all().delete()
        busqueda = Profesor.select()
        self.addMessage('<li>Encontrados %d profesores</li>'%busqueda.count())
        for profesor in busqueda:            
            p = Profesor_new(\
                id=profesor.id,\
                nombre=profesor.nombre,\
                apellido="%s %s"%(profesor.apellido1,profesor.apellido2),\
                telefono=profesor.telefono1
            )
            p.save()
        
        self.addMessage('<li>Importamos los grupos, primero vamos a vaciar la BBDD</li>')
        Grupo_new.objects.all().delete()
        busqueda = Grupo.select()
        self.addMessage('<li>Encontrados %d grupos</li>'%busqueda.count())
        for grupo in busqueda:
            curso = Curso_new.objects.get(nombre=grupo.curso.nombre)
            g = Grupo_new(\
                id=grupo.id,\
                year = year, \
                nombre=grupo.nombre,\
                curso=curso,\
                num_max=grupo.num_max,\
                menores=grupo.menores,\
            )
            g.save()
            #~ self.addMessage('Anadimos las clases')
            try:
                for clase in grupo.clases:
                    aula = Aula_new.objects.get(id=clase.aulaID)
                    inicio_txt = clase.horario.split("-")[0].replace(" ","")
                    inicio = datetime.time(int(inicio_txt.split(":")[0]),int(inicio_txt.split(":")[1]))
                    fin_txt = clase.horario.split("-")[1].replace(" ","")
                    fin = datetime.time(int(fin_txt.split(":")[0]),int(fin_txt.split(":")[1]))
                    #~ print inicio,fin
                    if clase.profesorID:
                        c = Clase_new(\
                            id=clase.id,\
                            grupo=g,\
                            profesor=Profesor_new.objects.get(id=clase.profesorID),\
                            aula=aula,\
                            dia_semana=dias[elimina_tildes(clase.dia_semana.lower())],\
                            hora_inicio=inicio_txt,\
                            hora_fin=fin_txt,\
                        )
                    else:
                        c = Clase_new(\
                            id=clase.id,\
                            grupo=g,\
                            aula=aula,\
                            dia_semana=dias[elimina_tildes(clase.dia_semana.lower())],\
                            hora_inicio=inicio_txt,\
                            hora_fin=fin_txt,\
                        )
                    c.save()
                    #~ print c.id,c.hora_inicio,c.hora_fin
                    c.save()
                    #~ logger.error("clase anadida")
            except:
                self.addMessage('<li>Error importando clase %s</li>'%clase);
                logger.error(sys.exc_info())
            #~ print g.nombre,g.clases.all()
            g.save()
            #~ logger.error("grupo añadido")
                
        self.addMessage('<li>Importamos los alumnos, primero vamos a vaciar la BBDD</li>')
        Alumno_new.objects.all().delete()
        busqueda = Alumno.select()
        self.addMessage('<li>Encontrados %d alumnos</li>'%busqueda.count())
        for persona in busqueda:
            #self.addMessage('Anadiendo el alumno %d'%persona.id)
            try:
                if type(persona.banco.codigo)==int:
                    banco = str(persona.banco.codigo)
                else:
                    banco = persona.banco.codigo
                banco = "0"*(4-len(banco))+banco
            except:
                banco = "2095"
            try:
                if type(persona.sucursal)==int:
                    sucursal = str(persona.sucursal)
                else:
                    sucursal = persona.sucursal
                sucursal = "0"*(4-len(sucursal))+sucursal
                
                if type(persona.dc)==int:
                    dc = str(persona.dc)
                else:
                    dc = persona.dc
                dc = "0"*(2-len(dc))+dc
                
                if type(persona.cuenta)==int:
                    dc = str(persona.cuenta)
                else:
                    dc = persona.cuenta
                cuenta = str(persona.cuenta)
                cuenta = "0"*(10-len(cuenta))+cuenta
                
                cuenta_bancaria = "%s-%s-%s-%s"%(banco,sucursal,dc,cuenta)
            except:
                logger.error('<li>%s</li>'%sys.last_traceback)
                self.addMessage('<li>Problema con la cuenta bancaria del alumno %d con cuenta %s. Error: %s </li>'%(persona.id,persona.cuenta,sys.exc_info()[0]))
                cuenta_bancaria = ""
                

            a = Alumno_new(id=persona.id,\
                activo = persona.activo,\
                nombre = persona.nombre,\
                apellido1 = persona.apellido1,\
                apellido2 = persona.apellido2,\
                fecha_nacimiento = persona.fecha_nacimiento,\
                fecha_creacion = persona.fecha_creacion,\
                telefono1 = persona.telefono1,\
                telefono2 = persona.telefono2,\
                email = persona.email,\
                cuenta_bancaria = cuenta_bancaria,\
                direccion = persona.direccion,\
                observaciones = persona.observaciones,\
                cp = persona.cp,\
                dni =persona.dni,)
            a.save()
        
        self.addMessage('<li>Importamos las asistencias, primero vamos a vaciar la BBDD</li>')
        Asistencia_new.objects.all().delete()
        busqueda = Asistencia.select()
        self.addMessage('<li>Encontrados %d asistencias, la vamos a importar al ano: %s</li>'%(busqueda.count(),year))
        for asis in busqueda:
            alumno = Alumno_new.objects.get(id=asis.alumno.id)
            grupo = Grupo_new.objects.get(id=asis.grupo.id)
            if (alumno.cuenta_bancaria==""):
                metalico=True
            else:
                metalico = asis.metalico
            try:
                precio = float(asis.precio)
                a = Asistencia_new(\
                    year=year,\
                    grupo=grupo,\
                    alumno=alumno,\
                    confirmado=asis.confirmado,\
                    factura=asis.factura,\
                    metalico=metalico,\
                    precio=precio,\
                )
            except:
                
                a = Asistencia_new(\
                    year = year,\
                    grupo=grupo,\
                    alumno=alumno,\
                    confirmado=asis.confirmado,\
                    factura=asis.factura,\
                    metalico=metalico,\
                )
            a.save()
        self.addMessage('<li>Importamos las historias, primero vamos a vaciar la BBDD</li>')
        Historia_new.objects.all().delete()
        busqueda = Historia.select()
        self.addMessage('<li>Encontrados %d historias</li>'%busqueda.count())
        for his in busqueda:
            try:
                alumno = Alumno_new.objects.get(id=his.alumno.id)
                h = Historia_new(\
                    alumno=alumno,\
                    fecha=his.fecha,\
                    tipo=his.tipo,\
                    anotacion=his.anotacion\
                )
                h.save()
            except:
                self.addMessage('Imposible importar la historia %s'%his)
                logger.error(sys.exc_info())
        
        self.addMessage("<li>Terminado</li></ul>")
        self.error=self.errors+"</ul>"
        self.imported=True
        self.save()
        print "Terminado"

class Document(models.Model):
    docfile = models.FileField(upload_to='documents/%Y/%m/%d')
