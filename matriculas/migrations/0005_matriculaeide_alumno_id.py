# -*- coding: utf-8 -*-
# Generated by Django 1.11.21 on 2020-05-29 16:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matriculas', '0004_auto_20200529_1742'),
    ]

    operations = [
        migrations.AddField(
            model_name='matriculaeide',
            name='alumno_id',
            field=models.DecimalField(blank=True, decimal_places=0, default=0, max_digits=6),
        ),
    ]
