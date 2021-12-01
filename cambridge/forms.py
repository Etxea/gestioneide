# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm, DateField
from django.forms.fields import BooleanField, ChoiceField, DecimalField
from django.forms.formsets import formset_factory
from django.forms.widgets import HiddenInput, NumberInput
from cambridge.models import *
from django.forms.models import inlineformset_factory
from bootstrap3_datetime.widgets import DateTimePicker
from localflavor.es.forms import *
from phonenumber_field.formfields import PhoneNumberField

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
    telephone = PhoneNumberField(label=_("Teléfono"))
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
        try:
            exam_id = kwargs.pop('exam_id')
        except:
            exam_id = None
            
        super(ModelForm, self).__init__(*args, **kwargs)
        if exam_id == None:
            #print("No tenemos examen fijado")
            self.fields['exam'].queryset = Exam.objects.filter(registration_end_date__gte=date.today(),schoolexam__isnull=True,venueexam__isnull=True).exclude(exam_type=5)
        else:
            self.fields['exam'].queryset = Exam.objects.filter(id=exam_id)

class LinguaskillRegistrationForm(ModelForm):
    telephone = PhoneNumberField(label=_("Teléfono"))
    #dni = ESIdentityCardNumberField()
    birth_date = DateField(label="Fecha Nac. (DD-MM-AAAA)", input_formats=['%d-%m-%Y'])
    proposed_date = DateField(label="Fecha Examen (DD-MM-AAAA)", input_formats=['%d-%m-%Y'])
    class Meta:
        model = LinguaskillRegistration
        #~ exclude = ('paid')
        fields = ['name','surname','birth_date','address','location','telephone','email','proposed_date']
        widgets = {
            'birth_date' : DateTimePicker(options={"format": "DD-MM-YYYY", "pickTime": False}),
            'proposed_date' : DateTimePicker(options={"format": "DD-MM-YYYY", "pickTime": False}),
        }
    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        self.fields['exam'].queryset = Exam.objects.filter(exam_type=5)

class SchoolRegistrationForm(ModelForm):
    telephone = PhoneNumberField(label=_("Teléfono"))
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
        super(SchoolRegistrationForm, self).__init__(*args, **kwargs)
        self.school_name = school_name
        #Limitamos los examenes a los de la escuela
        school = School.objects.get(name=school_name)
        #~ print(school)
        self.fields['exam'].queryset = SchoolExam.objects.filter(school=school,registration_end_date__gte=datetime.date.today())
        #~ self.fields['minor'].initial = True
        #~ self.fields['eide_alumn'].initial = False
        #~ self.fields['birth_date'].widget.format = '%d-%m-%Y'
        # at the same time, set the input format on the date field like you want it:
        #~ self.fields['birth_date'].input_formats = ['%d-%m-%Y']  

class RegistrationEditForm(ModelForm):
    telephone = PhoneNumberField(label=_("Teléfono"))
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
    telephone = PhoneNumberField(label=_("Teléfono"))
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

class PrepCenterRegistrationForm(ModelForm):
    prepcenter = forms.DecimalField(required=False,widget=HiddenInput())
    telephone = PhoneNumberField(label=_("Teléfono"))
    #dni = ESIdentityCardNumberField()
    postal_code = ESPostalCodeField(label=_("C.P."))
    birth_date = DateField(label="Fecha Nac. (DD-MM-AAAA)", input_formats=['%d-%m-%Y'])
    accept_conditions = BooleanField(
        label="Acepta las condiciones", 
        required=False)

    class Meta:
        model = Registration
        fields = ['prepcenter','exam','name','surname','address','location','postal_code','sex','birth_date','telephone','email','accept_conditions']
        widgets = {
            'birth_date' : DateTimePicker(options={"format": "DD-MM-YYYY", "pickTime": False}), 
            'exam': HiddenInput(),  
            'prepcenter': HiddenInput(),
            'postal_code': NumberInput(attrs={'size': 6})
                    
        }

PrepCenterRegistrationFormSet = formset_factory(
    PrepCenterRegistrationForm,
    extra = 0,
    max_num = 2,
    min_num = 1
)