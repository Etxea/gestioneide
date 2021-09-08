# -*- coding: utf-8 -*-

#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  


from django import forms
from django.forms import ModelForm
from hobetuz.models import *
from localflavor.es.forms import *
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _

class CursoForm(ModelForm):
	class Meta:
		fields = '__all__'
		model = Curso
		
class RegistrationForm(ModelForm):
	class Meta:
		model = Registration
		fields = '__all__'
	telephone = PhoneNumberField(_("Teléfono Fijo (*)"))
	telephone2 = PhoneNumberField(_("Teléfono Móvil (*)"))
	#dni = ESIdentityCardNumberField()
	#~ postal_code = ESPostalCodeField(label=_("Código Postal"))
	#~ class Meta:
		#~ model = Registration
		#~ exclude = ('paid')
	#~ 
	#~ def __init__(self, *args, **kwargs):
		#~ super(ModelForm, self).__init__(*args, **kwargs)
		#~ self.fields['birth_date'].widget.format = '%d-%m-%Y'
#~ 
		#~ # at the same time, set the input format on the date field like you want it:
		#~ self.fields['birth_date'].input_formats = ['%d-%m-%Y']	

class Registration2019Form(ModelForm):
	class Meta:
		model = Registration2019
		fields = '__all__'
	telephone = PhoneNumberField(_("Teléfono (*)"))
	#curso = forms.MultipleChoiceField(choices=CURSOS_2019, widget=forms.CheckboxSelectMultiple())

#~ class RegistrationEditForm(ModelForm):
	#~ telephone = ESPhoneNumberField(label=_("Teléfono"))
	#~ #dni = ESIdentityCardNumberField()
	#~ postal_code = ESPostalCodeField(label=_("Código Postal"))
	#~ class Meta:
		#~ model = Registration
	#~ def __init__(self, *args, **kwargs):
		#~ super(ModelForm, self).__init__(*args, **kwargs)
		#~ self.fields['birth_date'].widget.format = '%d-%m-%Y'
#~ 
		#~ # at the same time, set the input format on the date field like you want it:
		#~ self.fields['birth_date'].input_formats = ['%d-%m-%Y']
