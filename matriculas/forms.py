# -*- coding: utf-8 -*-
from django.forms import ModelForm,DateField
from models import MatriculaEide, MatriculaLinguaskill, Venue

class MatriculaEideForm(ModelForm):
    class Meta:
        model = MatriculaEide
        exclude = ('pagada','gestionada','alumno_id')


class MatriculaLinguaskillForm(ModelForm):
    class Meta:
        model = MatriculaLinguaskill
        exclude = ('pagada','registration_date')
    def __init__(self, *args, **kwargs):
        venue = kwargs.pop('venue')
        super(MatriculaLinguaskillForm, self).__init__(*args, **kwargs)
        #self.fields['venue'].queryset = Venue.objects.filter(name=venue)     