from django import forms
from localflavor.es.forms import *
from django.forms import ModelForm
from gestioneide.models import *


class GrupoCreateForm(ModelForm):
    class Meta:
        model = Grupo
        fields = "__all__" 


    # def save(self, commit=True):
    #     if not commit:
    #         raise NotImplementedError("Can't create User and UserProfile without database save")
    #     user = super(GrupoCreateForm, self).save(commit=True)
    #     user_profile = Grupo(user=user,telefono1=self.cleaned_data['telefono1'],telefono2=self.cleaned_data['telefono2'])
    #     user_profile.save()
    #     return user, user_profile
    
class GrupoCreateForm(ModelForm):
    class Meta:
        model = Curso
        fields = "__all__" 
