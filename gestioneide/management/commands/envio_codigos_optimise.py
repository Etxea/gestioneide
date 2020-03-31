#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'patataman'
from django.core.management.base import BaseCommand, CommandError
from gestioneide.models import Alumno
import csv

class Command(BaseCommand):
    #args = u'CSV con los código'
    help = u'Manda por mail los códigos a los alumnos'
    
    #def add_arguments(self, parser):
    #    parser.add_argument('--fichero', nargs='+', type=str)

    def handle(self, *args, **options):
        #if len(args)<1:
        #     raise CommandError('Falta fichero origen')
        #else:
        #   fichero = args[0]
        csvfile = open("codigos_optimise.csv",'rb')
        csvreader = csv.reader(csvfile,delimiter=',')
        mensaje = u"""
<html><body>
Hola %s,
<p>
Te enviamos el <b>código de tu workbook online</b>, para que puedas realizar los ejercicios del workbook optimise en la plataforma https://www.macmillaneducationeverywhere.com/. También te enviamos un <b>código de clase</b>, para que puedas unirte a tu clase de EIDE. La ventaja del libro online es que se pueden realizar los ejercicios de forma muy dinámica y tienes respuesta automática e inmediata.
</p>
<p>
Si ya estás registrado en la página de MacMillan, simplemente tendrás que añadir un código y unirte a la clase. Si no, podrás registrarte utilizando este código. Os colgaremos instrucciones en la plataforma Moodle https://online.eide.es/.
</p>

CÓDIGOS:
<br />
Código Workbook Online: <b>%s</b>
<br />
Código Clase: <b>%s</b>
<br />
Un saludo del equipo de EIDE.
</body></html>"""
        for linea in csvreader:
            alumno_id = linea[0].strip(" ")
            codigo_optimse = linea[1].strip(" ")
            codigo_clase = linea[2].strip(" ")
            alu = Alumno.objects.get(id=alumno_id)
            texto = mensaje%(alu.nombre,codigo_optimse,codigo_clase)
            print "Enviando al alumno %s el codigo %s"%(alumno_id,codigo_optimse)
            res = alu.enviar_mail("EIDE códigos optimise",texto,mensaje_html=True)
            if res:
                print "E-Mail enviado"
            else:
                print "error enviando el mail"

