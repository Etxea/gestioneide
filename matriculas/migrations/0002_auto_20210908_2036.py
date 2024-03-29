# Generated by Django 2.2.24 on 2021-09-08 18:36

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('matriculas', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registration',
            name='exam',
            field=models.ForeignKey(limit_choices_to={'registration_end_date__gte': datetime.date(2021, 9, 8)}, on_delete=django.db.models.deletion.CASCADE, to='matriculas.Exam'),
        ),
    ]
