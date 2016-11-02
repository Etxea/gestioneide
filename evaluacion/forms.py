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
        model = Nota
        fields = ('reading','reading_np','useofenglish','useofenglish_np','writing','writing_np','speaking','speaking_np','listenning','listenning_np')
        widgets = {
            'reading': forms.NumberInput(attrs={'max':100,'width':'3','size':'3','maxlength': '3'}),
            'useofenglish': forms.NumberInput(attrs={'max':100,'size':'2','maxlength': '2'}),
            'writing': forms.NumberInput(attrs={'max':100,'size':'2','maxlength': '2'}),
            'speaking': forms.NumberInput(attrs={'max':100,'size':'2','maxlength': '2'}),
            'listenning': forms.NumberInput(attrs={'max':100,'size':'2','maxlength': '2'})
        }

class UpperNotaCreateFrom(NotaCreateForm):
    class Meta:
        model = Nota
        fields = ['reading','reading_np','useofenglish','useofenglish_np','writing','writing_np','speaking','speaking_np','listenning','listenning_np']


class ElementaryNotaCreateForm(NotaCreateForm):
    class Meta:
        model = Nota
        fields = ['reading','reading_np', 'grammar','grammar_np']
        

NotaFormSet = modelformset_factory(Nota,form=NotaCreateForm,extra=0)
ElementayNotaFormSet = modelformset_factory(Nota,form=NotaCreateForm,extra=0)
UpperNotaFormSet = modelformset_factory(Nota,form=UpperNotaCreateFrom,extra=0)

FaltaFormSet = modelformset_factory(Falta,exclude=('mes','asistencia','id'),extra=0)
