# Generated by Django 4.0.4 on 2022-06-06 05:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('plannet', '0008_grupos_clave_alter_grupos_id_integrante_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='grupos',
            name='id_integrante',
        ),
    ]
