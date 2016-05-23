#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'patataman'
from importar.models import OldDatabase
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    args = 'sqlite database path'
    help = 'Importa datos de la BBDD de la anterior version del programa'

    def handle(self, *args, **options):
        if len(args)<1:
             for old in OldDatabase.objects.all():
                 print "ID: %s archivo %s"%(old.id,old.dbfile)
             raise CommandError('Falta fichero origen')
   
        dbfile = OldDatabase.objects.get(id=int(args[0]))
        print "Vamos a importar ",dbfile.dbfile.path
        dbfile.fixbancos()
        
                        
