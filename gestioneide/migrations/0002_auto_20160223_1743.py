# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-23 16:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestioneide', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='libro',
            name='autor',
            field=models.CharField(blank=True, default=b'', max_length=25),
        ),
    ]
