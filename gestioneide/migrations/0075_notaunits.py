# Generated by Django 2.2.24 on 2021-09-08 19:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gestioneide', '0074_auto_20210619_0903'),
    ]

    operations = [
        migrations.CreateModel(
            name='NotaUnits',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unit1', models.DecimalField(decimal_places=0, default=0, max_digits=3)),
                ('unit2', models.DecimalField(decimal_places=0, default=0, max_digits=3)),
                ('unit3', models.DecimalField(decimal_places=0, default=0, max_digits=3)),
                ('unit4', models.DecimalField(decimal_places=0, default=0, max_digits=3)),
                ('asistencia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestioneide.Asistencia')),
            ],
        ),
    ]
