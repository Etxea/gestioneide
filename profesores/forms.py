from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from localflavor.es.forms import *
from gestioneide.models import *

#~ class ProfesorCreateForm(UserCreationForm):
class ProfesorCreateForm(ModelForm):
    telefono = ESPhoneNumberField(required=False)
    class Meta:
        model = Profesor
        fields = ( "nombre","apellido","email", "telefono",  )
        #~ 
    #~ def save(self, commit=True):
        #~ if not commit:
            #~ raise NotImplementedError("Can't create User and UserProfile without database save")
        #~ user = super(ProfesorCreateForm, self).save(commit=True)
        #~ user_profile = Profesor(user=user,telefono=self.cleaned_data['telefono'])
        #~ user_profile.save()
        #~ return user, user_profile


#~ class ProfesorChangeForm(UserChangeForm):
class ProfesorChangeForm(ModelForm):
    telefono = ESPhoneNumberField(required=False)
    class Meta:
        model = Profesor
        fields = ( "nombre","apellido","email", "telefono",  )
        
        

