import os, sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gestioneide.settings")
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
#sys.path.append("/var/www/vhosts/eide.es/gestioneide")
#sys.path.insert(0,"/var/www/vhosts/eide.es/gestioneide/bin")
#sys.path.insert(0,"/var/www/vhosts/eide.es/gestioneide/lib/python2.7/site-packages/django")
#sys.path.insert(0,"/var/www/vhosts/eide.es/gestioneide/lib/python2.7/site-packages")

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()