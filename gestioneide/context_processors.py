from django.conf import settings
from gestioneide.models import Year

def current_year_processor(request):
    try:
        year = Year().get_activo(request)
    except:
        year = None
    try:
        year_global = Year().get_activo_global()
    except:
        year_global = None
    return {'year': year, 'year_global': year_global }

def gestioneide_settings(request):
    return {'GESTIONEIDE_MENSAJESGLOBLALES': settings.GESTIONEIDE_MENSAJESGLOBLALES }    
