# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-10-09 20:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestioneide', '0026_auto_20161009_2213'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recibo',
            old_name='total',
            new_name='importe_total',
        ),
        migrations.AddField(
            model_name='recibo',
            name='recibos_generados',
            field=models.DecimalField(blank=True, decimal_places=0, default=0, max_digits=4),
        ),
    ]