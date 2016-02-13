from django import forms
from localflavor.es.forms import *
from django.forms import ModelForm
from gestioneide.models import *


class AlumnoCreateForm(ModelForm):
    telefono1 = ESPhoneNumberField(required=True)
    telefono2 = ESPhoneNumberField(required=False)
    cuenta_bancaria = ESCCCField(required=False)
    dni = ESIdentityCardNumberField(required=False)
    cp = ESPostalCodeField(required=False)
    class Meta:
        model = Alumno
        #fields = ( "username", "email", "telefono1", "telefono2", "first_name", "last_name" )
        fields = '__all__'
        


    # def save(self, commit=True):
    #     if not commit:
    #         raise NotImplementedError("Can't create User and UserProfile without database save")
    #     user = super(AlumnoCreateForm, self).save(commit=True)
    #     user_profile = Alumno(user=user,telefono1=self.cleaned_data['telefono1'],telefono2=self.cleaned_data['telefono2'])
    #     user_profile.save()
    #     return user, user_profile
    
