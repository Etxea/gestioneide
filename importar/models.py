# -*- coding: utf-8 -*-
from django.db import models


class OldDatabase(models.Model):
    dbfile = models.FileField(upload_to='old_databases/%Y/%m/%d')

class Document(models.Model):
    docfile = models.FileField(upload_to='documents/%Y/%m/%d')
