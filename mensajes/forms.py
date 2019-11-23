# -*- coding: utf-8 -*-

from django import forms

class MensajeAllForm(forms.Form):
    titulo = forms.CharField(label='Título', max_length=100)
    mensaje = forms.Field(label='Mensaje', widget=forms.widgets.Textarea)