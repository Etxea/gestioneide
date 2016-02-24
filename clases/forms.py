from django.forms import ModelForm
from django import forms
from gestioneide.models import *

class ClaseForm(ModelForm):
	class Meta:
		model = Clase
		exclude = ["padre"]
		widgets = {
			"hora_inicio": forms.widgets.DateTimeInput(format='%Y-%m-%d %H:%M:%S'),
			"hora_fin": forms.widgets.DateTimeInput(format='%Y-%m-%d %H:%M:%S'),
			}
