# -*- coding: utf-8 -*-

#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  


from models import *
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
