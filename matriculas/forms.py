# -*- coding: utf-8 -*-
from django.forms import ModelForm
from models import *
class MatriculaEideForm(ModelForm):
    class Meta:
        model = MatriculaEide
        exclude = ('pagada',)