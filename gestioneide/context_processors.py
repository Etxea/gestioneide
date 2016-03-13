from models import Year

def current_year_processor(request):
    try:
        year = Year.objects.get(activo=True)
    except:
        year = None
    return {'year': year }
