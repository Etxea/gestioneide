# Generated by Django 2.2.25 on 2021-12-15 19:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gestioneide', '0079_alumno_sexo'),
        ('ticketbai', '0004_auto_20210908_2036'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticketbai_ticket',
            name='Emisor_ApellidosNombreRazonSocial',
        ),
        migrations.RemoveField(
            model_name='ticketbai_ticket',
            name='Emisor_NIF',
        ),
        migrations.AddField(
            model_name='ticketbai_ticket',
            name='FacturaSimplificada',
            field=models.CharField(choices=[('S', 'Sí'), ('N', 'No')], default='S', max_length=1),
        ),
        migrations.AddField(
            model_name='ticketbai_ticket',
            name='alumno_destinatario',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='gestioneide.Alumno'),
        ),
        migrations.AddField(
            model_name='ticketbai_ticket',
            name='empresa_emisor',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='gestioneide.Empresa'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='ticketbai_ticket',
            name='DatosFactura_ImporteTotalFactura',
            field=models.CharField(default='99.99', max_length=8, verbose_name='Importe Total'),
        ),
    ]
