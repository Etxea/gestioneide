"""
WSGI config for gestioneide project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

import os, sys

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gestioneide.settings")
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))



application = get_wsgi_application()
