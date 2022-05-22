from django.db import models

# Create your models here.
class Usuarios(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, verbose_name="Nombre")
    apellido = models.CharField(max_length=50, verbose_name="Apellido")
    correo = models.EmailField(max_length=50, verbose_name="Correo")
    password = models.CharField(max_length=30, verbose_name="Password")
    tipo = models.IntegerField()
    foto = models.ImageField(upload_to='images/', verbose_name="Foto", null=True)

    def __str__(self):
        fila = "Usuario: " + self.nombre + " " + self.apellido + "     Correo: " + self.correo
        return fila
    
    def delete(self, using=None, keep_parents=False):
        self.foto.storage.delete(self.foto.name)
        super().delete()


