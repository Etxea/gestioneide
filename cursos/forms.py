from bootstrap3_datetime.widgets import DateTimePicker
from django import forms
from django.forms import ModelForm
from gestioneide.models import *

class CursoForm(ModelForm):
    class Meta:
        model = Curso
        fields = '__all__'
        widgets = {
            'inicio' : DateTimePicker(options={"format": "YYYY-MM-DD", "pickTime": False}),
            'fin' : DateTimePicker(options={"format": "YYYY-MM-DD", "pickTime": False})
        }
