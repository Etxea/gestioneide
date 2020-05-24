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


from django import forms
from django.forms import ModelForm, DateField
from models import *
from django.forms.models import inlineformset_factory
#~ from django.forms.extras.widgets import SelectDateWidget
from bootstrap3_datetime.widgets import DateTimePicker
from localflavor.es.forms import *
from django.contrib.admin import widgets                                       
from django.utils.translation import gettext_lazy as _
from datetime import date

class ExamForm(ModelForm):
    
    class Meta:
        model = Exam
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        #self.fields['exam_date'].widget = DateTimePicker(options={"format": "DD-MM-YYYY", "pickTime": False})
        #self.fields['registration_end_date'].wifget = DateTimePicker(options={"format": "DD-MM-YYYY", "pickTime": False})
        #self.fields['exam_date'].input_formats = ['%Y-%m-%d']   
        #self.fields['registration_end_date'].input_formats = ['%Y-%m-%d']   
        self.fields['exam_date'].widget = forms.widgets.DateInput(format='%Y-%m-%d')
        self.fields['registration_end_date'].widget = forms.widgets.DateInput(format='%Y-%m-%d')

class SchoolExamForm(ModelForm):
    class Meta:
        model = SchoolExam
        fields = '__all__'
    def __init__(self, school_name, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        self.fields['exam_date'].widget.format = '%d-%m-%Y'
        self.fields['registration_end_date'].widget.format = '%d-%m-%Y'
        self.fields['exam_date'].input_formats = ['%d-%m-%Y']   
        self.fields['registration_end_date'].input_formats = ['%d-%m-%Y']   

        self.school_name = school_name
        #Limitamos los examenes a los de la escuela
        school = School.objects.get(name=school_name)
        self.fields['level'].queryset = SchoolLevel.objects.filter(school=school)
        
        
class RegistrationForm(ModelForm):
    telephone = ESPhoneNumberField(label=_("Teléfono"))
    #dni = ESIdentityCardNumberField()
    postal_code = ESPostalCodeField(label=_("Código Postal"))
    birth_date = DateField(label="Fecha Nac. (DD-MM-AAAA)", input_formats=['%d-%m-%Y'])
    class Meta:
        model = Registration
        #~ exclude = ('paid')
        fields = ['exam','minor','tutor_name','tutor_surname','name','surname','address','location','postal_code','sex','birth_date','telephone','email','eide_alumn','centre_name']
        widgets = {
            'birth_date' : DateTimePicker(options={"format": "DD-MM-YYYY", "pickTime": False}),
        }
    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        self.fields['exam'].queryset = Exam.objects.filter(registration_end_date__gte=date.today(),schoolexam__isnull=True,venueexam__isnull=True).exclude(exam_type=5)

class LinguaskillRegistrationForm(ModelForm):
    telephone = ESPhoneNumberField(label=_("Teléfono"))
    #dni = ESIdentityCardNumberField()
    birth_date = DateField(label="Fecha Nac. (DD-MM-AAAA)", input_formats=['%d-%m-%Y'])
    proposed_date = DateField(label="Fecha Examen (DD-MM-AAAA)", input_formats=['%d-%m-%Y'])
    class Meta:
        model = LinguaskillRegistration
        #~ exclude = ('paid')
        fields = ['exam','name','surname','birth_date','address','location','telephone','email','eide_alumn','centre_name','proposed_date']
        widgets = {
            'birth_date' : DateTimePicker(options={"format": "DD-MM-YYYY", "pickTime": False}),
            'proposed_date' : DateTimePicker(options={"format": "DD-MM-YYYY", "pickTime": False}),
        }
    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        self.fields['exam'].queryset = Exam.objects.filter(exam_type=5)


class SchoolRegistrationForm(ModelForm):
    telephone = ESPhoneNumberField(label=_("Teléfono"))
    #dni = ESIdentityCardNumberField()
    postal_code = ESPostalCodeField(label=_("Código Postal"))
    birth_date = DateField(label="Fecha Nac. (DD-MM-AAAA)", input_formats=['%d-%m-%Y'])
    class Meta:
        model = Registration
        #~ exclude = 'paid','minor','eide_alumn','centre_name')
        fields = ['exam','tutor_name','tutor_surname','name','surname','address','location','postal_code','sex','birth_date','telephone','email']
        widgets = {
            'birth_date' : DateTimePicker(options={"format": "DD-MM-YYYY", "pickTime": False}),
        }
    def __init__(self, school_name, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        self.school_name = school_name
        #Limitamos los examenes a los de la escuela
        school = School.objects.get(name=school_name)
        #~ print school
        self.fields['exam'].queryset = SchoolExam.objects.filter(school=school,registration_end_date__gte=datetime.date.today())
        #~ self.fields['minor'].initial = True
        #~ self.fields['eide_alumn'].initial = False
        #~ self.fields['birth_date'].widget.format = '%d-%m-%Y'
        # at the same time, set the input format on the date field like you want it:
        #~ self.fields['birth_date'].input_formats = ['%d-%m-%Y']  

class RegistrationEditForm(ModelForm):
    telephone = ESPhoneNumberField(label=_("Teléfono"))
    #dni = ESIdentityCardNumberField()
    postal_code = ESPostalCodeField(label=_("Código Postal"))
    class Meta:
        model = Registration
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        self.fields['birth_date'].widget.format = '%d-%m-%Y'

        # at the same time, set the input format on the date field like you want it:
        self.fields['birth_date'].input_formats = ['%d-%m-%Y']

class VenueExamForm(ModelForm):
    class Meta:
        model = VenueExam
        fields = '__all__'
        widgets = {
            'birth_date' : DateTimePicker(options={"format": "DD-MM-YYYY", "pickTime": False}),
        }
    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        self.fields['exam_date'].widget.format = '%d-%m-%Y'
        self.fields['registration_end_date'].widget.format = '%d-%m-%Y'
        self.fields['exam_date'].input_formats = ['%d-%m-%Y']   
        self.fields['registration_end_date'].input_formats = ['%d-%m-%Y']   
        self.fields['level'].queryset = Level.objects.filter(schoollevel__isnull=True)
        


class VenueRegistrationForm(ModelForm):
    telephone = ESPhoneNumberField(label=_("Teléfono"))
    #dni = ESIdentityCardNumberField()
    postal_code = ESPostalCodeField(label=_("Código Postal"))
    class Meta:
        model = Registration
        #~ exclude = ('paid','minor','eide_alumn','centre_name','tutor_name','tutor_surname')
        fields = ['exam','tutor_name','tutor_surname','name','surname','address','location','postal_code','sex','birth_date','telephone','email']
    def __init__(self, venue_name, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        self.venue_name = venue_name
        #Limitamos los examenes a los de la escuela
        venue = Venue.objects.get(name=venue_name)
        self.fields['exam'].queryset = VenueExam.objects.filter(venue=venue)
        self.fields['birth_date'].widget.format = '%d-%m-%Y'
        self.fields['birth_date'].input_formats = ['%d-%m-%Y']  
