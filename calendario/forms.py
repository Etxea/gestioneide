from django import forms
from django.forms import ModelForm
from gestioneide.models import *

class FestivoForm(ModelForm):
    class Meta:
        model = Festivo
        fields = '__all__'
