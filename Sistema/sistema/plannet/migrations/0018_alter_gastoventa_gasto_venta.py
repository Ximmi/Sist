# Generated by Django 4.0.4 on 2023-01-20 07:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plannet', '0017_alter_retroalimentacion_calificacion_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gastoventa',
            name='gasto_venta',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Descripción del gasto de venta'),
        ),
    ]
