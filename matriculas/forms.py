# -*- coding: utf-8 -*-
from django.forms import ModelForm,DateField
from models import MatriculaEide, MatriculaLinguaskill, LinguaskillLevel, Venue
from localflavor.es.forms import *
from django.utils.translation import ugettext_lazy as _

from bootstrap3_datetime.widgets import DateTimePicker


class MatriculaEideForm(ModelForm):
    class Meta:
        model = MatriculaEide
        exclude = ('pagada','gestionada','alumno_id')


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
    def __init__(self, *args, **kwargs):
        venue_name = kwargs.pop('venue')
        super(MatriculaLinguaskillForm, self).__init__(*args, **kwargs)
        self.fields['level'].queryset = LinguaskillLevel.objects.filter(venue=Venue.objects.filter(name=venue_name))
             