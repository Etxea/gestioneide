from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from ticketbai.views import *

urlpatterns = [
    url(r'^$', login_required(TicketBai_TicketListView.as_view()),name="ticketbai_index"),
    url(r'new/$', login_required(TicketBai_TicketCreateView.as_view()),name="ticketbai_new"),
    url(r'detail/(?P<pk>\d+)$', login_required(TicketBai_TicketDetailView.as_view()),name="ticketbai_detail"),
]