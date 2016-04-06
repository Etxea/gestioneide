#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'patataman'
from django.core.management.base import BaseCommand, CommandError
from gestioneide.models import Festivo, Year
import csv

class Command(BaseCommand):
    args = 'CSV con los festivos'
    help = 'Importa festivos a la BBDD desde un CSV bajado de http://opendata.euskadi.eus/contenidos/ds_eventos/calendario_laboral_2015'

    def handle(self, *args, **options):
        if len(args)<1:
             raise CommandError('Falta fichero origen')
        else:
			fichero = args[0]
			csvfile = open('calendario_laboral_2016.csv','rb')
			csvreader = csv.reader(csvfile,delimiter=';')
			year = Year.objects.get(activo=True)
			for linea in csvreader:
				ambito = linea[3].strip(" ")
				if ambito in ['Estado','CAV','Bizkaia','Santurtzi']:
					print linea[0],linea[1],linea[3]
					campos = linea[0].split("/")
					fecha = "%s-%s-%s"%(campos[2],campos[1],campos[0])
					Festivo.objects.get_or_create(fecha=fecha,anotacion=u"%s"%linea[2],tipo=6,year=year)

					
