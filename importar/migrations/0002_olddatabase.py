# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-22 23:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('importar', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OldDatabase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dbfile', models.FileField(upload_to=b'old_databases/%Y/%m/%d')),
            ],
        ),
    ]