from models import Ano
import sys

def current_year_processor(request):
    print "buscamos el ano"
    try:
        year = Ano.objects.filter(activo=True)[0]
        print "Tenemos el ano",year
    except:
        print "error", sys.exc_info()[0]
        year = None
    return {'year': year }
