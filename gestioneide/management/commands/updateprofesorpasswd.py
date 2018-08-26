#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'patataman'
from gestioneide.models import *
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = 'Actualiza la contraseña de un  profesoriy encial al email la password.'
    def add_arguments(self, parser):
        parser.add_argument('profesor_id', type=int)

    def handle(self, *args, **options):
        profesor_id=options['profesor_id']
        try:
            profesor = Profesor.objects.get(id=profesor_id)
            self.stdout.write(self.style.SUCCESS(u'Trabajando con el profesor "%s" %s' % (profesor_id,profesor)))
            profesor.update_user_password()
        except:
            raise CommandError('Profesor "%s" does not exist' % profesor_id)
        
        
        
                        
