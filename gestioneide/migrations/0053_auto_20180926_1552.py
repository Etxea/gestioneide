# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2018-09-26 13:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestioneide', '0052_auto_20180922_1054'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recibo',
            name='metalicos',
            field=models.DecimalField(blank=True, decimal_places=0, default=0, max_digits=6),
        ),
        migrations.AlterField(
            model_name='recibo',
            name='numero_recibos',
            field=models.DecimalField(blank=True, decimal_places=0, default=0, max_digits=6),
        ),
    ]