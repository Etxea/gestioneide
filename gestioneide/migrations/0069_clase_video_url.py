# -*- coding: utf-8 -*-
# Generated by Django 1.11.21 on 2020-04-17 12:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestioneide', '0068_auto_20200416_0959'),
    ]

    operations = [
        migrations.AddField(
            model_name='clase',
            name='video_url',
            field=models.URLField(blank=True),
        ),
    ]
