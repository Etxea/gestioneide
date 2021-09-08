import os, sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gestioneide.settings")
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
