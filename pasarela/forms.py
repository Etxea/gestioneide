from django.forms import ModelForm
from pasarela.models import *

class PagoForm(ModelForm):
    class Meta:
        model = Pago
        exclude = ('fecha_pago',)
