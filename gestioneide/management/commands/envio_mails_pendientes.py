#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'patataman'
from gestioneide.models import *
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Envia los mails que aun no habían sido enviados.'

    def handle(self, *args, **options):
        for email_pendiente in MailAlumno.objects.filter(enviado=False)[:500]:
            self.stdout.write(self.style.SUCCESS(u'Mandando mail %s de las %s : %s a %s' % (email_pendiente.id,email_pendiente.fecha,email_pendiente.titulo,email_pendiente.alumno)))

            if email_pendiente.creador.profesor:
                if email_pendiente.creador.profesor.email:
                    email_pendiente.enviado = \
                        email_pendiente.alumno.enviar_mail(email_pendiente.titulo,\
                        email_pendiente.mensaje,\
                        from_email=email_pendiente.creador.profesor.email)
            elif email_pendiente.creador.email:
        
                email_pendiente.enviado = \
                    email_pendiente.alumno.enviar_mail(email_pendiente.titulo,\
                        email_pendiente.mensaje,\
                        from_email=email_pendiente.creador.email)
            else:
                email_pendiente.enviado = \
                    email_pendiente.alumno.enviar_mail(email_pendiente.titulo,\
                    email_pendiente.mensaje)
            email_pendiente.save()



