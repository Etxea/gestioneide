from django import forms
from localflavor.es.forms import *
from django.forms import ModelForm
from gestioneide.models import *


class GrupoCreateForm(ModelForm):
    class Meta:
        model = Grupo
        fields = "__all__" 
