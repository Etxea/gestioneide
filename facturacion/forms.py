from django import forms
from localflavor.es.forms import *
from django.forms import ModelForm
from gestioneide.models import *

class ReciboCreateForm(ModelForm):
    class Meta:
        model = Recibo
        #~ fields = '__all__'
        exclude = ['fichero_csb19']

