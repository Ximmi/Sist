from unicodedata import name
from django.contrib.auth.models import BaseUserManager
from django.db import transaction,models
from django.contrib.auth.models import Group


class UserManager(BaseUserManager, models.Manager):

    def _create_user(self, correo, password, is_superuser, **extra_fields):
        with transaction.atomic():
            user = self.model(
                correo = correo,
                is_superuser = is_superuser,
                **extra_fields
            )
            user.set_password(password)
            user.save(using=self.db)
            # asgina el grupo
            tipo = user.tipo
            if(tipo == '1'):  # si es estudiante
                user.groups.set(Group.objects.filter(name="Estudiante"))
            elif(tipo == '2'):  # si es emprendedor
                user.groups.set(Group.objects.filter(name="Emprendedor"))
            elif(tipo == '3'):  # si es profesor
                user.groups.set(Group.objects.filter(name="Profesor"))
            elif(tipo == '4'):  # si es coach
                user.groups.set(Group.objects.filter(name="Coach"))
                
        return user

    def create_user(self, correo, password=None, **extra_fields):
        return self._create_user(correo, password, False, **extra_fields)

    def create_superuser(self, correo, password=None, **extra_fields):
        return self._create_user(correo, password, True, **extra_fields)



class GroupManager(models.Manager):
    def create_grupo(self, nombre_grupo, clave, id_responsable):
        with transaction.atomic():
            grupo = self.model(
                nombre_grupo = nombre_grupo,
                clave = clave,
                id_responsable = id_responsable
            )
            
            grupo.save(using=self.db)
            # asgina el grupo
                
        return grupo

class EstadosFinancierosManager(models.Manager):
    def create_estado_financiero(self, nombre_estado, id_contenido_estado):
        with transaction.atomic():
            estado = self.model(
                nombre_estado =  nombre_estado,
                id_contenido_estado = id_contenido_estado
            )

            estado.save(using=self.db)
            #asigna el estado financiero