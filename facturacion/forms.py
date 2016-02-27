from django import forms
from localflavor.es.forms import *
from django.forms import ModelForm
from gestioneide.models import *

class ReciboCreateForm(ModelForm):
    class Meta:
        model = Recibo
        #fields = ( "username", "email", "telefono1", "telefono2", "first_name", "last_name" )
        fields = '__all__'

