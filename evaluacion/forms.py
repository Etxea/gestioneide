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
        fields = ('reading','reading_np','useofenglish','useofenglish_np','writing','writing_np','speaking','speaking_np','listening','listening_np')
        exclude = ('id',)
        widgets = {
            'reading': forms.NumberInput(attrs={'style':'width: 75px;', 'max':100,'width':'3','size':'3','maxlength': '3'}),
            'reading_writing': forms.NumberInput(attrs={'style':'width: 75px;', 'max':100,'width':'3','size':'3','maxlength': '3'}),
            'useofenglish': forms.NumberInput(attrs={'style':'width: 75px;', 'max':100,'size':'2','maxlength': '2'}),
            'writing': forms.NumberInput(attrs={'style':'width: 75px;', 'max':100,'size':'2','maxlength': '2'}),
            'speaking': forms.NumberInput(attrs={'style':'width: 75px;', 'max':100,'size':'2','maxlength': '2'}),
            'listening': forms.NumberInput(attrs={'style':'width: 75px;', 'max':100,'size':'2','maxlength': '2'})
        }

class NotaUnitsCreateForm(ModelForm):
    class Meta:
        model = NotaUnits
        fields = ['id','unit1','unit2','unit3','unit4','unit5','unit6','unit7','unit8','unit9','unit10','unit11','unit12','unit13','unit14','unit15']
        widgets = {
            'id': forms.HiddenInput(),
            'unit1': forms.NumberInput(attrs={'style':'width: 50px;', 'max':100,'size':'2','maxlength': '2'}),
            'unit2': forms.NumberInput(attrs={'style':'width: 50px;', 'max':100,'size':'2','maxlength': '2'}),
            'unit3': forms.NumberInput(attrs={'style':'width: 50px;', 'max':100,'size':'2','maxlength': '2'}),
            'unit4': forms.NumberInput(attrs={'style':'width: 50px;', 'max':100,'size':'2','maxlength': '2'}),
            'unit5': forms.NumberInput(attrs={'style':'width: 50px;', 'max':100,'size':'2','maxlength': '2'}),
            'unit6': forms.NumberInput(attrs={'style':'width: 50px;', 'max':100,'size':'2','maxlength': '2'}),
            'unit7': forms.NumberInput(attrs={'style':'width: 50px;', 'max':100,'size':'2','maxlength': '2'}),
            'unit8': forms.NumberInput(attrs={'style':'width: 50px;', 'max':100,'size':'2','maxlength': '2'}),
            'unit9': forms.NumberInput(attrs={'style':'width: 50px;', 'max':100,'size':'2','maxlength': '2'}),
            'unit10': forms.NumberInput(attrs={'style':'width: 50px;', 'max':100,'size':'2','maxlength': '2'}),
            'unit11': forms.NumberInput(attrs={'style':'width: 50px;', 'max':100,'size':'2','maxlength': '2'}),
            'unit12': forms.NumberInput(attrs={'style':'width: 50px;', 'max':100,'size':'2','maxlength': '2'}),
            'unit13': forms.NumberInput(attrs={'style':'width: 50px;', 'max':100,'size':'2','maxlength': '2'}),
            'unit14': forms.NumberInput(attrs={'style':'width: 50px;', 'max':100,'size':'2','maxlength': '2'}),
            'unit15': forms.NumberInput(attrs={'style':'width: 50px;', 'max':100,'size':'2','maxlength': '2'}),
        }

class NotaUnitsWritingCreateForm(ModelForm):
    class Meta:
        model = NotaUnitsWriting
        fields = ['id','unit1','unit2','unit3','unit4','unit5','unit6','unit7','unit8','unit9','unit10','unit11','unit12','unit13','unit14','unit15']
        widgets = {
            'id': forms.HiddenInput(),
            'writing_number': forms.HiddenInput(),
            'unit1': forms.NumberInput(attrs={'style':'width: 50px;', 'max':100,'size':'2','maxlength': '2'}),
            'unit2': forms.NumberInput(attrs={'style':'width: 50px;', 'max':100,'size':'2','maxlength': '2'}),
            'unit3': forms.NumberInput(attrs={'style':'width: 50px;', 'max':100,'size':'2','maxlength': '2'}),
            'unit4': forms.NumberInput(attrs={'style':'width: 50px;', 'max':100,'size':'2','maxlength': '2'}),
            'unit5': forms.NumberInput(attrs={'style':'width: 50px;', 'max':100,'size':'2','maxlength': '2'}),
            'unit6': forms.NumberInput(attrs={'style':'width: 50px;', 'max':100,'size':'2','maxlength': '2'}),
            'unit7': forms.NumberInput(attrs={'style':'width: 50px;', 'max':100,'size':'2','maxlength': '2'}),
            'unit8': forms.NumberInput(attrs={'style':'width: 50px;', 'max':100,'size':'2','maxlength': '2'}),
            'unit9': forms.NumberInput(attrs={'style':'width: 50px;', 'max':100,'size':'2','maxlength': '2'}),
            'unit10': forms.NumberInput(attrs={'style':'width: 50px;', 'max':100,'size':'2','maxlength': '2'}),
            'unit11': forms.NumberInput(attrs={'style':'width: 50px;', 'max':100,'size':'2','maxlength': '2'}),
            'unit12': forms.NumberInput(attrs={'style':'width: 50px;', 'max':100,'size':'2','maxlength': '2'}),
            'unit13': forms.NumberInput(attrs={'style':'width: 50px;', 'max':100,'size':'2','maxlength': '2'}),
            'unit14': forms.NumberInput(attrs={'style':'width: 50px;', 'max':100,'size':'2','maxlength': '2'}),
            'unit15': forms.NumberInput(attrs={'style':'width: 50px;', 'max':100,'size':'2','maxlength': '2'}),
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
        fields = ['reading_writing','reading_writing_np', 'speaking','speaking_np','listening','listening_np','observaciones']

class IntermediateNotaCreateFrom(NotaCreateForm):
    class Meta:
        model = NotaCuatrimestral
        fields = ['reading','reading_np','writing','writing_np','speaking','speaking_np','listening','listening_np','observaciones']

class UpperNotaCreateFrom(NotaCreateForm):
    class Meta:
        model = NotaCuatrimestral
        fields = ['reading','reading_np','writing','writing_np','speaking','speaking_np','listening','listening_np','useofenglish','useofenglish_np','observaciones']



NotaFormSet = modelformset_factory(NotaCuatrimestral,form=NotaCreateForm,extra=0)

NotaUnitsFormSet = modelformset_factory(NotaUnits,form=NotaUnitsCreateForm,extra=0)
NotaUnitsWritingFormSet = modelformset_factory(NotaUnitsWriting,form=NotaUnitsWritingCreateForm,extra=0)
NotaTrimestralFormSet = modelformset_factory(NotaTrimestral,form=NotaTrimestralCreateForm,extra=0)
NotaTrimestralKidsFormSet = modelformset_factory(NotaTrimestral,form=NotaTrimestralKidsCreateForm,extra=0)

ElementayNotaFormSet = modelformset_factory(NotaCuatrimestral,form=ElementaryNotaCreateForm,extra=0)
IntermediateNotaFormSet = modelformset_factory(NotaCuatrimestral,form=IntermediateNotaCreateFrom,extra=0)
UpperNotaFormSet = modelformset_factory(NotaCuatrimestral,form=UpperNotaCreateFrom,extra=0)

FaltaFormSet = modelformset_factory(Falta,exclude=('mes','asistencia','id'),extra=0)


## Notas parciales
class GrupoNotasParcialesCreateForm(ModelForm):
    class Meta:
        model = GrupoNotasParciales
        fields = '__all__'
        widgets = {
        #     'id': forms.HiddenInput(),
             'grupo': forms.HiddenInput()
        }


class NotaParcialCreateForm(ModelForm):
    class Meta:
        model = NotaParcial
        fields = '__all__'
        widgets = {
            'nota': forms.NumberInput(attrs={'style':'width: 75px;', 'max':100,'width':'3','size':'3','maxlength': '3'}),
            'grupo_notas_parciales': forms.HiddenInput(),
            'asistencia': forms.HiddenInput()
        }


NotaParcialFormSet = modelformset_factory(NotaParcial, form=NotaParcialCreateForm, extra=0)


# class NotaParcialFormSet(BaseNotaParcialFormSet):
#     def __init__(self, *args,  **kwargs):
#         print("Dentro de NotaParcialFormSet con grupo_notas_parciales: ",kwargs['grupo_notas_parciales'])
#         ##self.grupo_notas_parciales = GrupoNotasParciales.objects.get(id=int(kwargs['grupo_notas_parciales']))
#         super(NotaParcialFormSet, self).__init__(*args, **kwargs)

