from models import Year

def current_year_processor(request):
    try:
        year = Year().get_activo()
    except:
        year = None
    return {'year': year }
