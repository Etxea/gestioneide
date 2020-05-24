# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from localflavor.es.forms import *
from django.forms import ModelForm
from gestioneide.models import *
from django.contrib.auth.models import User

class ConfirmacionForm(forms.Form):
    title = forms.CharField()
    message = forms.CharField(widget=forms.Textarea)