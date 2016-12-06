#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'patataman'
from gestioneide.models import Curso
from django.core.management.base import BaseCommand, CommandError
import re

class Command(BaseCommand):
    args = ''
    help = 'Fixea el tipo de evaluacion en base el nombre del grupo'

    def handle(self, *args, **options):
        texto_intermediate="intermediate"
        texto_elementary="elementary"
        texto_upper="upper"
        texto_proficiency="proficiency"
        for curso in Curso.objects.all():
            print curso.nombre,":",curso.tipo_evaluacion
            if len(re.findall(texto_intermediate,curso.nombre , flags=re.IGNORECASE)) or len(re.findall(texto_elementary,curso.nombre , flags=re.IGNORECASE)):
                print "Tiene inter o elemen"
                curso.tipo_evaluacion=2
                curso.save()
            if len(re.findall(texto_proficiency,curso.nombre , flags=re.IGNORECASE)) or len(re.findall(texto_upper,curso.nombre , flags=re.IGNORECASE)):
                print "Tiene upper o prof"
                curso.tipo_evaluacion=3
                curso.save()

         
                        
