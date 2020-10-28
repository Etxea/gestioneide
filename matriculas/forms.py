# -*- coding: utf-8 -*-
from django.forms import ModelForm,DateField
from models import MatriculaEide, MatriculaLinguaskill, LinguaskillLevel, Venue

class MatriculaEideForm(ModelForm):
    class Meta:
        model = MatriculaEide
        exclude = ('pagada','gestionada','alumno_id')


class MatriculaLinguaskillForm(ModelForm):
    class Meta:
        model = MatriculaLinguaskill
        exclude = ('paid','registration_date')
    def __init__(self, *args, **kwargs):
        venue_name = kwargs.pop('venue')
        super(MatriculaLinguaskillForm, self).__init__(*args, **kwargs)
        self.fields['level'].queryset = LinguaskillLevel.objects.filter(venue=Venue.objects.filter(name=venue_name))
             