# Generated by Django 4.0.4 on 2022-06-07 02:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plannet', '0013_remove_contenidoestados_campo_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='contenidoestados',
            name='agrupacion',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Agrupación'),
        ),
    ]