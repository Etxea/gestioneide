from django.conf.urls import url
from sermepa.views import *

urlpatterns = [
    url(r'^$', sermepa_ipn,name='sermepa_ipn'),
]
