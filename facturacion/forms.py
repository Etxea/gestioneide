from django import forms
from localflavor.es.forms import *
from django.forms import ModelForm
from gestioneide.models import *

class ReciboCreateForm(ModelForm):
    class Meta:
        model = Recibo
        fields = ['year', 'empresa', 'mes', 'medio_mes', 'grupos_sueltos']
    def get_success_url():
        return reverse_lazy('recibo_editar', args=(self.object.id))

class ReciboUpdateForm(ModelForm):
    class Meta:
        model = Recibo
        exclude = ['fichero_csb19', 'recibos_generados', 'importe_recibos', 'metalicos', 'importe_metalico', 'importe_total', 'numero_recibos', 'errores']
    def __init__(self, *args, **kwargs):
        super(ReciboUpdateForm, self).__init__(*args, **kwargs)

        if self.instance:
            centros = self.instance.empresa.centro_set.all
            print centros
            grupos = Grupo.objects.filter(centro__in=self.instance.empresa.centro_set.all(),year=Year().get_activo())
            self.fields['grupos'].widget = forms.SelectMultiple(attrs={'size': '%s'%len(grupos)})
            self.fields['grupos'].queryset = grupos
