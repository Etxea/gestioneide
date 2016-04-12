from django import forms
from localflavor.es.forms import *
from django.forms import ModelForm, BaseModelFormSet
from gestioneide.models import *

from django.forms.models import modelformset_factory


NotaFormSet = modelformset_factory(Nota,exclude=('trimestre','asistencia','id'),extra=0)
ElementayNotaFormSet = modelformset_factory(Nota,exclude=('trimestre','asistencia','id'),extra=0)
UpperNotaFormSet = modelformset_factory(Nota,exclude=('trimestre','asistencia','id'),extra=0)
FaltaFormSet = modelformset_factory(Falta,exclude=('mes','asistencia','id'),extra=0)

class BaseNotaFormSet(BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        super(BaseNotaFormSet, self).__init__(*args, **kwargs)
        self.queryset = Nota.objects.filter(trimestre==kwargs['trimestre'])

class NotaCreateForm(ModelForm):
    class Meta:
        model = Nota
        #fields = ( "username", "email", "telefono1", "telefono2", "first_name", "last_name" )
        fields = '__all__'
        
class UpperNotaCreateFrom(NotaCreateForm):
    class Meta:
        model = Nota
        fields = ["grammar", "grammar_np"]
        

class ElementaryNotaCreateForm(NotaCreateForm):
    class Meta:
        model = Nota
        fields = ["writing", "writing_np"]
        

