#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gestioneide.models import *
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = 'Actualiza la contraseña de un usuario y se la enviamos al email.'
    def add_arguments(self, parser):
        parser.add_argument('user_id', type=int)

    def handle(self, *args, **options):
        user_id=options['user_id']
        try:
            user = User.objects.get(id=user_id)
        except:
            raise CommandError('User "%s" does not exist' % user_id)
        self.stdout.write(self.style.SUCCESS(u'Trabajando con el usuario "%s" %s' % (user_id,user)))
        password = User.objects.make_random_password()
        user.set_password(password)
        user.save()
        mensaje = u"""Te acabamos de crear un usuario o modificar la contraseña para el sistema de
            gestión de alumnos de EIDE. 

            Los datos de acceso son:
                https://gestion.eide.es
                usuario: %s
                contraseña: %s
          Guarda en lugar seguro estos datos por favor."""%(user.username,password)
        #print(user.username,password)
        user.email_user(u"Cambio contraseña en gestion de alumnos EIDE",mensaje)
        send_mail(u"Cambio contraseña en gestion de alumnos EIDE",mensaje,'webmaster@eide.es',['eide@eide.es','moebius1984@gmail.com'])

        
        
        
                        
