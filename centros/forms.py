from django.forms import ModelForm
from localflavor.es.forms import *
from gestioneide.models import *

class CentroCreateForm(ModelForm):
    class Meta:
        fields = "__all__"
        model = Centro

class CentroChangeForm(ModelForm):
    class Meta:
        fields = "__all__"
        model = Centro