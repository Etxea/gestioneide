from django.forms import ModelForm
from localflavor.es.forms import *
from gestioneide.models import *

class EmpresaCreateForm(ModelForm):
    class Meta:
        fields = "__all__"
        model = Empresa

class EmpresaChangeForm(ModelForm):
    class Meta:
        fields = "__all__"
        model = Empresa