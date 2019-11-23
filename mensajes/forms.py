# -*- coding: utf-8 -*-
from django import forms
from mensajes.models import *

class MensajeForm(forms.ModelForm):
    class Meta:
        model = Mensaje
        fields = "__all__"
        widgets = {
            #'titulo': forms.CharField(label='Título', max_length=100),
            'creador': forms.HiddenInput(), 
            'leido': forms.HiddenInput(), 
            'todos': forms.HiddenInput(),
        }

class MensajeAllForm(forms.Form):
    titulo = forms.CharField(label='Título', max_length=100)
    mensaje = forms.Field(label='Mensaje', widget=forms.widgets.Textarea)