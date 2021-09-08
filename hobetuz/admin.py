# -*- coding: utf-8 -*-
from hobetuz.models import *
from django.contrib import admin

class RegistrationAdmin(admin.ModelAdmin):
    pass
class CursoAdmin(admin.ModelAdmin):
    pass

admin.site.register(Registration, RegistrationAdmin)
admin.site.register(Registration2019, RegistrationAdmin)
admin.site.register(Curso, CursoAdmin)

