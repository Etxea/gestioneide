# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2019-01-06 21:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mensajes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mensaje',
            name='todos',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='mensaje',
            name='leido',
            field=models.BooleanField(default=False),
        ),
    ]
