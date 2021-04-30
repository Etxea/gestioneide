# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class TicketBai_Ticket(models.Model):
    create_time = models.DateTimeField(auto_now_add=True)
