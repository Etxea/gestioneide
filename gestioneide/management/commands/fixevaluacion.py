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
        texto_first="first"
        texto_pre="pre"
        texto_advance="advance"
        texto_upper="upper"
        texto_proficiency="proficiency"
        for curso in Curso.objects.all():
            print curso.nombre,":",curso.tipo_evaluacion
            if len(re.findall(texto_intermediate,curso.nombre , flags=re.IGNORECASE))>0 or \
		len(re.findall(texto_elementary,curso.nombre , flags=re.IGNORECASE))>0 and \
		len(re.findall(texto_pre,curso.nombre , flags=re.IGNORECASE))>0:
                print "Tiene inter o elemen"
                curso.tipo_evaluacion=2
                curso.save()
            if len(re.findall(texto_intermediate,curso.nombre , flags=re.IGNORECASE))>0 and\
		not len(re.findall(texto_pre,curso.nombre , flags=re.IGNORECASE))>0:
                curso.tipo_evaluacion=3
                curso.save()
            if len(re.findall(texto_proficiency,curso.nombre , flags=re.IGNORECASE))>0 or \
		len(re.findall(texto_first,curso.nombre , flags=re.IGNORECASE))>0 or\
		len(re.findall(texto_advance,curso.nombre , flags=re.IGNORECASE))>0 or\
		len(re.findall(texto_upper,curso.nombre , flags=re.IGNORECASE))>0 :
                curso.tipo_evaluacion=4
                curso.save()
	    else:
		curso.tipo_evaluacion=1
		curso.save()

         
                        
