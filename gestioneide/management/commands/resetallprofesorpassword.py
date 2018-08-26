#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'patataman'
from gestioneide.models import *
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Actualiza la contraseña de todos los profesores y la envía al email asociado.'

    def handle(self, *args, **options):
        for profesor in Profesor.objects.all():
                self.stdout.write(self.style.SUCCESS(u'Trabajando con el profesor %s' % (profesor)))
                if not profesor.user:
                    self.stdout.write(self.style.WARNING('Profesor SIN USUARIO %s' % (profesor)))
                    continue
                if profesor.user.is_active:
                    profesor.update_user_password()
                else:
                    self.stdout.write(
                        self.style.SUCCESS('Profesor dado de BAJA %s' % (profesor)))



