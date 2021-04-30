from django.conf.urls import url
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic import TemplateView

from views import *
from forms import *
from models import *


urlpatterns = [
    url(r'$', TemplateView.as_view( template_name='ticketbai/index.html' ),name="ticketbai_index"),
]