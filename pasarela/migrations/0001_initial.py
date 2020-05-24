# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-03 20:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pago',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('importe', models.DecimalField(decimal_places=2, max_digits=6)),
                ('descripcion', models.CharField(blank=True, max_length=250, verbose_name='Concepto')),
                ('fecha_creacion', models.DateField(auto_now_add=True)),
                ('fecha_pago', models.DateField(blank=True, null=True)),
            ],
        ),
    ]
