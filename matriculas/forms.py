# -*- coding: utf-8 -*-
from django.forms import ModelForm,DateField
from matriculas.models import *
from localflavor.es.forms import *
from django.utils.translation import ugettext_lazy as _
from datetime import date
from bootstrap3_datetime.widgets import DateTimePicker

class MatriculaEideForm(ModelForm):
    class Meta:
        model = MatriculaEide
        exclude = ('pagada','gestionada','alumno_id')

class MatriculaCursoForm(ModelForm):
    postal_code = ESPostalCodeField(label="Código Postal")
    birth_date = DateField(label="Fecha Nac. (DD-MM-AAAA)", input_formats=['%d-%m-%Y'])
    
    class Meta:
        model = MatriculaCurso
        exclude = ('paid','registration_date', 'password')
        # widgets = {
        #     'proposed_date' : DateTimePicker(options={"format": "DD-MM-YYYY", "pickTime": False}),
        #     'birth_date' : DateTimePicker(options={"format": "DD-MM-YYYY", "pickTime": False}),
        # }
    def __init__(self, *args, **kwargs):
        try:
            self.curso = kwargs.pop('curso')
            super(MatriculaCursoForm, self).__init__(*args, **kwargs)
            self.fields['curso'].choices = self.curso
        except:
            super(MatriculaCursoForm, self).__init__(*args, **kwargs)


class MatriculaLinguaskillForm(ModelForm):
    proposed_date = DateField(label="Fecha Propuesta (DD-MM-AAAA)", input_formats=['%d-%m-%Y'])
    postal_code = ESPostalCodeField(label="Código Postal")
    birth_date = DateField(label="Fecha Nac. (DD-MM-AAAA)", input_formats=['%d-%m-%Y'])
    
    class Meta:
        model = MatriculaLinguaskill
        exclude = ('paid','registration_date')
        # widgets = {
        #     'proposed_date' : DateTimePicker(options={"format": "DD-MM-YYYY", "pickTime": False}),
        #     'birth_date' : DateTimePicker(options={"format": "DD-MM-YYYY", "pickTime": False}),
        # }
    def __init__(self, venue, *args, **kwargs):
        super(MatriculaLinguaskillForm, self).__init__(*args, **kwargs)
        #venue_name = kwargs.pop('venue')
        self.fields['level'].queryset = LinguaskillLevel.objects.filter(venue=Venue.objects.get(name=venue))

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
    #telephone = ESPhoneNumberField(label=_("Teléfono"))
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

class SchoolRegistrationForm(ModelForm):
    #telephone = ESPhoneNumberField(label=_("Teléfono"))
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
    #telephone = ESPhoneNumberField(label=_("Teléfono"))
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
    #telephone = ESPhoneNumberField(label=_("Teléfono"))
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
