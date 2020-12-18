# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from models import Venue, LinguaskillLevel,Curso

admin.site.register(Venue)
admin.site.register(Curso)
admin.site.register(LinguaskillLevel)

