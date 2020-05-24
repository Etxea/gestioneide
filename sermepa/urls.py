from django.conf.urls import url
from views import *

urlpatterns = [
    url(r'^$', sermepa_ipn,name='sermepa_ipn'),
]
