# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-13 07:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestioneide', '0003_auto_20160228_1748'),
    ]

    operations = [
        migrations.CreateModel(
            name='Year',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_year', models.DecimalField(decimal_places=0, default=2015, max_digits=4)),
                ('name', models.CharField(default=b'20XX-XX', max_length=8)),
                ('activo', models.BooleanField(default=1)),
            ],
        ),
    ]