from django.forms import ModelForm,HiddenInput,MultipleHiddenInput
from gestioneide.models import *

class AsistenciaCreateForm(ModelForm):
    class Meta:
        model = Asistencia
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super(AsistenciaCreateForm, self).__init__(*args, **kwargs)
        self.fields['grupo'].queryset = Grupo.objects.filter(year=Year().get_activo(self.request))
        self.fields['year'] = Year().get_activo(self.request)

class AsistenciaGrupoCreateForm(ModelForm):
    class Meta:
        model = Asistencia
        fields = '__all__'
        widgets = {
            #'grupo': HiddenInput(),
            #'year': HiddenInput(),
            'borrada': HiddenInput(),
        }
