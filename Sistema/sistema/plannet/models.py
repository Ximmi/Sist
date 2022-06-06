from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from plannet.manager import UserManager, GroupManager


# Create your models here.
class Usuarios(AbstractBaseUser, PermissionsMixin):

    CHOICES = [('1', "Estudiante"), ('2', "Emprendedor"), ('3', "Profesor"), ('4', "Coach") ]
    nombre = models.CharField(max_length=50, verbose_name="Nombre", null=False)
    apellido = models.CharField(max_length=50, verbose_name="Apellido", null=False)
    correo = models.EmailField(max_length=50, verbose_name="Correo", null=False, unique=True)
    foto = models.ImageField(upload_to='images/', verbose_name="Foto", null=True, default='')
    id_grupo = models.ForeignKey('Grupos', on_delete=models.CASCADE, blank=True, null=True)
    tipo = models.CharField(choices=CHOICES, null=True, blank=True, default=1, max_length=1) 
    activo = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'correo'
    objects = UserManager()
    

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
        ordering = ['id', 'nombre']
        permissions = [('ingresa_grupo', 'Ingresa a grupo'), ('crea_grupo', 'Crea grupo')]


    def __str__(self):
        fila = "Usuario: " + self.nombre + " " + self.apellido + "     Correo: " + self.correo
        return fila
    
    def delete(self, using=None, keep_parents=False):
        self.foto.storage.delete(self.foto.name)
        super().delete()


    def trae_grupos(self):
        from plannet.models import Grupos
        resultado = Grupos.objects.filter(id_responsable=self).all()
        return resultado


    


class Estudiante(Usuarios):
    boleta = models.CharField(max_length=50, verbose_name="Boleta", null=True, default=None)

    # objects = EstudianteManager()

    class Meta:
        proxy = False

    def __str__(self):
        return  f"Estudiante: {self.nombre} {self.apellido} email: {self.correo}"


class Emprendedor(Usuarios):
    class Meta:
        proxy = False

    def __str__(self):
        return  f"Emprendedor: {self.nombre} {self.apellido} email: {self.correo}"

class Profesor(Usuarios):

    rfc = models.CharField(max_length=50, verbose_name="RFC", null=True, default=None)
    clave_institucion = models.CharField(max_length=50, verbose_name="Clave de institucion", null=True, default=None)
    class Meta:
        proxy = False

    def __str__(self):
        return  f"Profesor: {self.nombre} {self.apellido} email: {self.correo}"

class Coach(Usuarios):
    
    rfc = models.CharField(max_length=50, verbose_name="RFC", null=True, default=None)
    class Meta:
        proxy = False

    def __str__(self):
        return  f"Coach: {self.nombre} {self.apellido} email: {self.correo}"

class Grupos(models.Model):
    nombre_grupo = models.CharField(max_length=50, verbose_name="Nombre grupo", unique=True)
    clave = models.CharField(max_length=50, verbose_name="Clave", null=True)
    id_responsable = models.ForeignKey('plannet.Usuarios', on_delete=models.CASCADE, related_name='Responsable',null=True, default=None)

    objects = GroupManager()

    class Meta:
        verbose_name = "Grupo"
        verbose_name_plural = "Grupos"
        ordering = ['id', 'nombre_grupo']

    def __str__(self):
        return f"Grupo: {self.nombre_grupo} clave: {self.clave}"
    
    def delete(self, using=None, keep_parents=False):
        super().delete()


