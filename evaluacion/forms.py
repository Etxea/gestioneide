# -*- coding: utf-8 -*-

from django import forms
from localflavor.es.forms import *
from django.forms import ModelForm, BaseModelFormSet
from gestioneide.models import *
from django.forms.models import modelformset_factory

#~ class BaseNotaFormSet(BaseModelFormSet):
    #~ def __init__(self, *args, **kwargs):
        #~ super(BaseNotaFormSet, self).__init__(*args, **kwargs)
        #~ self.queryset = Nota.objects.filter(trimestre==kwargs['trimestre'])

class NotaCreateForm(ModelForm):
    class Meta:
        model = NotaCuatrimestral
        fields = ('reading','reading_np','useofenglish','useofenglish_np','writing','writing_np','speaking','speaking_np','listenning','listenning_np')
        exclude = ('id',)
        widgets = {
            'reading': forms.NumberInput(attrs={'style':'width: 75px;', 'max':100,'width':'3','size':'3','maxlength': '3'}),
            'reading_writing': forms.NumberInput(attrs={'style':'width: 75px;', 'max':100,'width':'3','size':'3','maxlength': '3'}),
            'useofenglish': forms.NumberInput(attrs={'style':'width: 75px;', 'max':100,'size':'2','maxlength': '2'}),
            'writing': forms.NumberInput(attrs={'style':'width: 75px;', 'max':100,'size':'2','maxlength': '2'}),
            'speaking': forms.NumberInput(attrs={'style':'width: 75px;', 'max':100,'size':'2','maxlength': '2'}),
            'listenning': forms.NumberInput(attrs={'style':'width: 75px;', 'max':100,'size':'2','maxlength': '2'})
        }

class NotaTrimestralCreateForm(ModelForm):
    class Meta:
        model = NotaTrimestral
        fields = ['id','nota','np','observaciones']
        widgets = {
            'id': forms.HiddenInput()
        }
#Form para KIDS con los campos de KIDs
class NotaTrimestralKidsCreateForm(ModelForm):
    class Meta:
        model = NotaTrimestral
        fields = ['id','nota','np','observaciones','exp_oral','comp_oral','exp_escrita','comp_escrita','temas_repasar','aspectos_mejorar']
        widgets = {
            'id': forms.HiddenInput()
        }

class ElementaryNotaCreateForm(NotaCreateForm):
    class Meta:
        model = NotaCuatrimestral
        fields = ['reading_writing','reading_writing_np', 'speaking','speaking_np','listenning','listenning_np','observaciones']

class IntermediateNotaCreateFrom(NotaCreateForm):
    class Meta:
        model = NotaCuatrimestral
        fields = ['reading','reading_np','writing','writing_np','speaking','speaking_np','listenning','listenning_np','observaciones']

class UpperNotaCreateFrom(NotaCreateForm):
    class Meta:
        model = NotaCuatrimestral
        fields = ['reading','reading_np','writing','writing_np','speaking','speaking_np','listenning','listenning_np','useofenglish','useofenglish_np','observaciones']


NotaFormSet = modelformset_factory(NotaCuatrimestral,form=NotaCreateForm,extra=0)

NotaTrimestralFormSet = modelformset_factory(NotaTrimestral,form=NotaTrimestralCreateForm,extra=0)
NotaTrimestralKidsFormSet = modelformset_factory(NotaTrimestral,form=NotaTrimestralKidsCreateForm,extra=0)

ElementayNotaFormSet = modelformset_factory(NotaCuatrimestral,form=ElementaryNotaCreateForm,extra=0)
IntermediateNotaFormSet = modelformset_factory(NotaCuatrimestral,form=IntermediateNotaCreateFrom,extra=0)
UpperNotaFormSet = modelformset_factory(NotaCuatrimestral,form=UpperNotaCreateFrom,extra=0)

FaltaFormSet = modelformset_factory(Falta,exclude=('mes','asistencia','id'),extra=0)
