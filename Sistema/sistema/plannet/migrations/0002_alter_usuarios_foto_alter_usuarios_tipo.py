# Generated by Django 4.0.4 on 2022-05-19 04:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plannet', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuarios',
            name='foto',
            field=models.ImageField(null=True, upload_to='images/', verbose_name='Foto'),
        ),
        migrations.AlterField(
            model_name='usuarios',
            name='tipo',
            field=models.IntegerField(),
        ),
    ]