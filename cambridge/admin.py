# -*- coding: utf-8 -*-
from cambridge.models import *
from django.contrib import admin

class RegistrationAdmin(admin.ModelAdmin):
    search_fields = (['dni'])

class LinguaskillRegistrationAdmin(admin.ModelAdmin):
    search_fields = (['dni'])


class LevelAdmin(admin.ModelAdmin):
    pass

class ExamAdmin(admin.ModelAdmin):
	pass

class SchoolAdmin(admin.ModelAdmin):
	pass
	
class SchoolExamAdmin(admin.ModelAdmin):
	pass

class SchoolLevelAdmin(admin.ModelAdmin):
    pass


admin.site.register(LinguaskillRegistration, LinguaskillRegistrationAdmin)
admin.site.register(Registration, RegistrationAdmin)
admin.site.register(Level, LevelAdmin)
admin.site.register(Exam, ExamAdmin)

admin.site.register(SchoolLevel, SchoolLevelAdmin)
admin.site.register(SchoolExam, SchoolExamAdmin)
admin.site.register(School, SchoolAdmin)

class VenueAdmin(admin.ModelAdmin):
	pass
	
class VenueExamAdmin(admin.ModelAdmin):
	pass
admin.site.register(VenueExam, VenueExamAdmin)
admin.site.register(Venue, VenueAdmin)
