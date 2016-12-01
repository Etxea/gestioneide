#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'patataman'
from importar.models import OldDatabase, Year
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    args = 'Sqlite database file ID, year'
    help = 'Importa notas de la BBDD de la anterior version del programa'

    def handle(self, *args, **options):
        if len(args)<2:
             for old in OldDatabase.objects.all():
                 print "ID: %s archivo %s"%(old.id,old.dbfile)
             for year in Year.objects.all():
                 print "ID: %s archivo %s"%(year.id,year)
             raise CommandError('Falta fichero origen y/o ano')
   
        dbfile = OldDatabase.objects.get(id=int(args[0]))
        ano=int(args[1])
        print "Vamos a importar las notas desde ",dbfile.dbfile.path, "para el año",ano
        dbfile.doImportNotas(ano)
        
                        
