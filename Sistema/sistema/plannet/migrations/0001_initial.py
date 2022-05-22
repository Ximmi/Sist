# Generated by Django 4.0.4 on 2022-05-19 04:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Usuarios',
            fields=[
                ('id_usuario', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50, verbose_name='Nombre')),
                ('apellido', models.CharField(max_length=50, verbose_name='Apellido')),
                ('correo', models.EmailField(max_length=50, verbose_name='Correo')),
                ('password', models.CharField(max_length=30, verbose_name='Password')),
                ('tipo', models.IntegerField(max_length=1)),
                ('foto', models.ImageField(null=True, upload_to='images/', verbose_name='foto')),
            ],
        ),
    ]