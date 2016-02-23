#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'patataman'
from django.core.management.base import BaseCommand, CommandError
from gestioneide.models import Alumno as Alumno_new
from gestioneide.models import Asistencia as Asistencia_new
from gestioneide.models import Ano
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

import unicodedata
def elimina_tildes(s):
   return ''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))
 

dias = {'lunes': 1, 'martes': 2, 'miercoles': 3, "jueves":4, "viernes": 5}

class Command(BaseCommand):
    args = 'sqlite database path'
    help = 'Importa datos de la BBDD de la anterior version del programa'

    def handle(self, *args, **options):
        if len(args)<1:
             raise CommandError('Falta fichero origen')
        else:
            bbdd = args[0]
            self.stdout.write('Iniciando importacion desde archivo %s'%bbdd)
            sqlhub.processConnection = connectionForURI('sqlite://'+bbdd)
            from gestioneide.old_database_model import *

            self.stdout.write('Importamos los libros, primero vamos a vaciar la BBDD')
            Libro_new.objects.all().delete()
            busqueda = Libro.select()
            self.stdout.write('Encontrados %d libros'%busqueda.count())
            for libro in busqueda:
		if not libro.autor:
			autor = ""
		else:
			autor=libro.autor
		print "autor",autor
                l = Libro_new(\
                    titulo=libro.titulo,\
                    autor=autor,\
                    isbn=libro.isbn,\
                    editorial=str(libro.editorial),\
                )
                l.save()
            
            self.stdout.write('Importamos las aulas, primero vamos a vaciar la BBDD')
            Aula_new.objects.all().delete()
            busqueda = Aula.select()
            self.stdout.write('Encontrados %d aulas'%busqueda.count())
            for aula in busqueda:
                a = Aula_new(\
                    id=aula.id,\
                    nombre="%s"%aula.numero,\
                    aforo=aula.aforo,\
                    pdi=False,\
                    
                )
                a.save()
            
            self.stdout.write('Importamos los cursos, primero vamos a vaciar la BBDD')
            Curso_new.objects.all().delete()
            busqueda = Curso.select()
            self.stdout.write('Encontrados %d cursos'%busqueda.count())
            for curso in busqueda:
                c = Curso_new(\
                    nombre = curso.nombre,\
                    precio = curso.precio,\
                    ##No obligatorios
                    examen = curso.examen,\
                    nivel = curso.nivel,\
                    nota_aprobado = curso.nota_aprobado,\
                    solo_examen_final = curso.solo_examen_final,\
                )
                c.save()
                for libro in curso.libros:
                    try:
                        c.libros.add(Libro_new.objects.filter(isbn=libro.isbn)[0])
                    except:
                        self.stdout.write("No se ha podido anadir el libro %s"%libro.isbn)

                                
            self.stdout.write('Importamos los profesfores, primero vamos a vaciar la BBDD')
            Profesor_new.objects.all().delete()
            busqueda = Profesor.select()
            self.stdout.write('Encontrados %d profesores'%busqueda.count())
            for profesor in busqueda:
                
                p = Profesor_new(\
                    id=profesor.id,\
                    nombre=profesor.nombre,\
                    apellido="%s %s"%(profesor.apellido1,profesor.apellido2),\
                    telefono=profesor.telefono1
                )
                p.save()
            
            self.stdout.write('Importamos los grupos, primero vamos a vaciar la BBDD')
            Grupo_new.objects.all().delete()
            busqueda = Grupo.select()
            self.stdout.write('Encontrados %d grupos'%busqueda.count())
            for grupo in busqueda:
                curso = Curso_new.objects.get(nombre=grupo.curso.nombre)
                g = Grupo_new(\
                    id=grupo.id,\
                    nombre=grupo.nombre,\
                    curso=curso,\
                    num_max=grupo.num_max,\
                    menores=grupo.menores,\
                )
                g.save()
                #~ self.stdout.write('Anadimos las clases')
                try:
                    for clase in grupo.clases:
                        if clase.profesorID:
                            profesor = Profesor_new.objects.get(id=clase.profesorID)
                        else:
                            profesor = None
                        aula = Aula_new.objects.get(id=clase.aulaID)
                        inicio_txt = clase.horario.split("-")[0].replace(" ","")
                        inicio = datetime.time(int(inicio_txt.split(":")[0]),int(inicio_txt.split(":")[1]))
                        fin_txt = clase.horario.split("-")[1].replace(" ","")
                        fin = datetime.time(int(fin_txt.split(":")[0]),int(fin_txt.split(":")[1]))
                        #~ print inicio,fin
                        c = Clase_new(\
                            id=clase.id,\
                            grupo=g,\
                            profesor=profesor,\
                            aula=aula,\
                            dia_semana=dias[elimina_tildes(clase.dia_semana.lower())],\
                            hora_inicio=inicio_txt,\
                            hora_fin=fin_txt,\
                        )
                        c.save()
                        #~ print c.id,c.hora_inicio,c.hora_fin
                        c.save()
                except:
                    self.stdout.write('Error importando clase');
                    print clase
                    print sys.exc_info()
                #~ print g.nombre,g.clases.all()
                g.save()
                    
            self.stdout.write('Importamos los alumnos, primero vamos a vaciar la BBDD')
            Alumno_new.objects.all().delete()
            busqueda = Alumno.select()
            self.stdout.write('Encontrados %d alumnos'%busqueda.count())
            for persona in busqueda:
                #self.stdout.write('Anadiendo el alumno %d'%persona.id)
                try:
                    if type(persona.banco.codigo)==int:
                        banco = str(persona.banco.codigo)
                    else:
                        banco = persona.banco.codigo
                    banco = "0"*(4-len(banco))+banco
                    
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
                    #~ print sys.last_traceback
                    self.stdout.write('Problema con la cuenta bancaria del alumno %d'%(persona.id))
                    print sys.exc_info()
                    print persona.cuenta
                    #~ self.stdout.write(sys.exc_info()[0])
                    
                    cuenta_bancaria = ""
                    

                a = Alumno_new(id=persona.id,\
                    activo = persona.activo,\
                    nombre = persona.nombre,\
                    apellido1 = persona.apellido1,\
                    apellido2 = persona.apellido2,\
                    telefono1 = persona.telefono1,\
                    telefono2 = persona.telefono2,\
                    email = persona.email,\
                    cuenta_bancaria = cuenta_bancaria,\
                    localidad = persona.ciudad,\
                    cp = persona.cp,\
                    dni =persona.dni,)
                a.save()
                
            self.stdout.write('Creamos el ano')  
            Ano.objects.all().delete()  
            ano = Ano(ano="2015-16",activo=True)
            ano.save()
            
            self.stdout.write('Importamos las asistencias, primero vamos a vaciar la BBDD')
            Asistencia_new.objects.all().delete()
            busqueda = Asistencia.select()
            self.stdout.write('Encontrados %d asistencias'%busqueda.count())
            for asis in busqueda:
                alumno = Alumno_new.objects.get(id=asis.alumno.id)
                grupo = Grupo_new.objects.get(id=asis.grupo.id)
                try:
                    precio = float(asis.precio)
                    a = Asistencia_new(\
                        ano=ano,\
                        grupo=grupo,\
                        alumno=alumno,\
                        confirmado=asis.confirmado,\
                        factura=asis.factura,\
                        metalico=asis.metalico,\
                        precio=precio,\
                    )
                except:
                    
                    a = Asistencia_new(\
                        ano=ano,\
                        grupo=grupo,\
                        alumno=alumno,\
                        confirmado=asis.confirmado,\
                        factura=asis.factura,\
                        metalico=asis.metalico,\
                    )
                a.save()
            self.stdout.write('Importamos las historias, primero vamos a vaciar la BBDD')
            Historia_new.objects.all().delete()
            busqueda = Historia.select()
            self.stdout.write('Encontrados %d historias'%busqueda.count())
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
                    self.stdout.write('Imposible importar la historia')
                    print his
                    
