# -*- coding: utf-8 -*-
# Generated by Django 1.11.21 on 2020-04-16 07:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestioneide', '0067_auto_20200416_0803'),
    ]

    operations = [
        migrations.AlterField(
            model_name='centro',
            name='telefono',
            field=models.CharField(default=b'', max_length=12),
        ),
        migrations.AlterField(
            model_name='empresa',
            name='telefono',
            field=models.CharField(default=b'', max_length=12),
        ),
        migrations.AlterField(
            model_name='profesor',
            name='telefono',
            field=models.CharField(default=b'', max_length=12),
        ),
    ]
