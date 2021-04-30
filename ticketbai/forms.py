# -*- coding: utf-8 -*-

from django import forms
from django.forms import ModelForm
from models import *

class CursoForm(ModelForm):
	class Meta:
		fields = '__all__'
		model = TicketBai_Ticket