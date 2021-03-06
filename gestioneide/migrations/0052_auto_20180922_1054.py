# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2018-09-22 08:54
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('gestioneide', '0051_recibo_empresa'),
    ]

    operations = [
        migrations.AddField(
            model_name='recibo',
            name='fecha_cargo',
            field=models.DateField(auto_now_add=True, default=datetime.datetime(2018, 9, 22, 8, 54, 11, 919916, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='recibo',
            name='importe_metalico',
            field=models.FloatField(blank=True, default=0),
        ),
        migrations.AddField(
            model_name='recibo',
            name='importe_recibos',
            field=models.FloatField(blank=True, default=0),
        ),
        migrations.AddField(
            model_name='recibo',
            name='numero_recibos',
            field=models.DecimalField(blank=True, decimal_places=0, default=0, max_digits=4),
        ),
    ]
