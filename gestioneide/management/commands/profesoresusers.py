#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'patataman'
from gestioneide.models import *
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = 'Crea usuarios para los profesores y le envía vía mail la password.'

    def handle(self, *args, **options):
        for profesor in Profesor.objects.all():
            #print "Trabajando con",profesor,profesor.user
            if profesor.user:
                print "Ya tiene user",profesor.user.username
                #profesor.update_user_password()
            else:
                print "Le creamos usuario"
                profesor.create_user()
        
        
        
                        
