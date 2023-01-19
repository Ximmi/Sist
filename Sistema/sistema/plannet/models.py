from pyexpat import model
from tabnanny import verbose
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from plannet.manager import UserManager, GroupManager, EstadosFinancierosManager


# Create your models here.
class Usuarios(AbstractBaseUser, PermissionsMixin):

    CHOICES = [('1', "Estudiante"), ('2', "Profesor")]
    nombre = models.CharField(max_length=50, verbose_name="Nombre", null=False)
    apellido = models.CharField(max_length=50, verbose_name="Apellido", null=False)
    correo = models.EmailField(max_length=50, verbose_name="Correo", null=False, unique=True)
    foto = models.ImageField(upload_to='images/', verbose_name="Foto", null=True, default='')
    num = models.CharField(max_length=50, verbose_name="Núm. de boleta o empleado", null= False)
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
       # fila = "Usuario: " + self.nombre + " " + self.apellido + "     Correo: " + self.correo
        fila =  self.nombre + " " + self.apellido 
        return fila
    
    def delete(self, using=None, keep_parents=False):
        self.foto.storage.delete(self.foto.name)
        super().delete()


    def trae_grupos(self):
        from plannet.models import Grupos
        resultado = Grupos.objects.filter(id_responsable=self).all()
        return resultado


    


class Estudiante(Usuarios):

    # objects = EstudianteManager()

    class Meta:
        proxy = False

    def __str__(self):
        return  f"Estudiante: {self.nombre} {self.apellido} email: {self.correo}"


class Profesor(Usuarios):

    class Meta:
        proxy = False

    def __str__(self):
        return  f"Profesor: {self.nombre} {self.apellido} email: {self.correo}"


class Grupos(models.Model):
    CHOICES = [('1', "enero-junio"), ('2', "agosto-diciembre")]
    nombre_grupo = models.CharField(max_length=50, verbose_name="Nombre del grupo")
    clave = models.CharField(max_length=50, verbose_name="Clave", unique=True, default=1)
    periodo = models.CharField(choices=CHOICES, null=True, blank=True, default=1, max_length=1) 
    ciclo = models.CharField(max_length=50, verbose_name="Año", null= True)
    id_responsable = models.ForeignKey('plannet.Usuarios', on_delete=models.CASCADE, related_name='Responsable',null=True, default=None)

    objects = GroupManager()

    class Meta:
        verbose_name = "Grupo"
        verbose_name_plural = "Grupos"
        ordering = ['id', 'nombre_grupo']

    def __str__(self):
        return f"{self.nombre_grupo}"
    
    def delete(self, using=None, keep_parents=False):
        super().delete()


class PlandeNegocio(models.Model):
    id_usuario = models.ForeignKey('plannet.Usuarios', on_delete=models.CASCADE, related_name='Usuario_Plan',null=True, default=None)
    tema = models.CharField(max_length=50, verbose_name="Tema", null=True, blank=True)
    subtema = models.CharField(max_length=50, verbose_name="Subtema", null=True, blank=True)
    actividad = models.FileField(upload_to='images/', verbose_name="Actividad", null=True, default='')
    puntuacion = models.IntegerField( verbose_name="Puntuación", null=True, blank=True)
    comentario = models.CharField(max_length=50, verbose_name="Comentario", null=True, blank=True)



#ESTA ES PARA LA CONSULTA DE ACTIVIDADES POR FASE
class EstadosFinancieros(models.Model):
    nombre_estado = models.CharField(max_length=50, verbose_name="Nombre de la actividad", null=True, blank=True)
    fase = models.CharField(max_length=50, verbose_name="Fase", null=True, blank=True)
    objects = EstadosFinancierosManager()

    class Meta:
        verbose_name = "Estado Financiero"
        verbose_name_plural = "Estados Financieros"
        ordering = ['id', 'nombre_estado']
    
    def __str__(self):
        return f"Nombre: {self.nombre_estado}"
    
    def delete(self, using=None, keep_parents=False):
        super().delete()


#aquí es donde el usuario guarda los valores del balance general, inversiones e ingresos
class ContenidoEstados(models.Model):
    fila = models.CharField(max_length=50, verbose_name="Fila", null=True, blank=True)
    columna = models.CharField(max_length=50, verbose_name="Columna", null=True, blank=True)
    agrupacion = models.CharField(max_length=50, verbose_name="Agrupación", null=True, blank=True)
    numero_campo = models.IntegerField( verbose_name="Numero de campo", null=True, blank=True)
    id_estado = models.ForeignKey('plannet.EstadosFinancieros', on_delete=models.CASCADE, related_name='Estado_Contenido',null=True, default=None)


class EstadoUsuario(models.Model):
    id_usuario = models.ForeignKey('plannet.Usuarios', on_delete=models.CASCADE, related_name='Usuario_Estado',null=True, default=None)
    id_campo = models.ForeignKey('plannet.ContenidoEstados', on_delete=models.CASCADE, related_name='Campo',null=True, default=None)
    valor = models.IntegerField( verbose_name="Valor", null=True, blank=True)


class Definicion(models.Model):
    CHOICES = [('1', "Software"), ('2', "Hardware"), ('3', "Sistema embebido")]
    CHOICES2 = [('1', "Producto"), ('2', "Servicio")]
    id_usuario = models.ForeignKey('plannet.Usuarios', on_delete=models.CASCADE, related_name='Usuario_Definicion',null=True, default=None)
    nombre = models.CharField(max_length=100, verbose_name="Nombre del Producto", null=True, blank=True)
    descripcion = models.CharField(max_length=800, verbose_name="Definición", null=True, blank=True)
    tipo = models.CharField(choices=CHOICES, null=True, blank=True, default=1, max_length=1) 
    clasificacion = models.CharField(choices=CHOICES2, null=True, blank=True, default=1, max_length=1) 
    id_grupo = models.ForeignKey('Grupos', on_delete=models.CASCADE, blank=True, null=True)
    id_estado = models.ForeignKey('plannet.EstadosFinancieros', on_delete=models.CASCADE, related_name='Estado_Definicion',null=True, default=None)



class Objetivos(models.Model):
    id_usuario = models.ForeignKey('plannet.Usuarios', on_delete=models.CASCADE, related_name='Usuario_Ojetivos',null=True, default=None)
    mision = models.CharField(max_length=500, verbose_name="Misión", null=True, blank=True)
    vision = models.CharField(max_length=500, verbose_name="Visión", null=True, blank=True)
    objgeneral = models.CharField(max_length=300, verbose_name="Objetivo general", null=True, blank=True)
    objespecificos = models.CharField(max_length=500, verbose_name="Objetivos específicos", null=True, blank=True)
    id_estado = models.ForeignKey('plannet.EstadosFinancieros', on_delete=models.CASCADE, related_name='Estado_Objetivos',null=True, default=None)

class Ingresos(models.Model):
    id_usuario = models.ForeignKey('plannet.Usuarios', on_delete=models.CASCADE, related_name='Usuario_Ingresos',null=True, default=None)
    producto = models.CharField(max_length=50, verbose_name="Producto", null=True, blank=True)
    unidades = models.IntegerField( verbose_name="Unidades al año", null=True, blank=True)
    precio_unitario = models.IntegerField( verbose_name="Precio unitario", null=True, blank=True)
    ingresos = models.IntegerField( verbose_name="Ingresos por año", null=True, blank=True)
    id_estado = models.ForeignKey('plannet.EstadosFinancieros', on_delete=models.CASCADE, related_name='Estado_Ingresos',null=True, default=None)

class Materiales(models.Model):
    CHOICES = [('1', "Unidad"),
                ('2', "Mes de servicio"),
                ('3', "Año de servicio")
                    ]
    id_usuario = models.ForeignKey('plannet.Usuarios', on_delete=models.CASCADE, related_name='Usuario_Materiales',null=True, default=None)
    material = models.CharField(max_length=50, verbose_name="Producto", null=True, blank=True)
    unidad_medida = models.CharField(choices=CHOICES, null=True, blank=True, default=1, max_length=1)
    costo = models.IntegerField( verbose_name="Costo por unidad", null=True, blank=True)
    volumen = models.IntegerField( verbose_name="Volumen requerido", null=True, blank=True)
    costo_anual = models.IntegerField( verbose_name="Costo por año", null=True, blank=True)
    id_estado = models.ForeignKey('plannet.EstadosFinancieros', on_delete=models.CASCADE, related_name='Estado_Materiales',null=True, default=None)

class Envase(models.Model):
    CHOICES = [('1', "Envase"),
                ('2', "Empaque"),
                ('3', "Embalaje"),
                ]
    id_usuario = models.ForeignKey('plannet.Usuarios', on_delete=models.CASCADE, related_name='Usuario_Envase',null=True, default=None)
    tipo_envase = models.CharField(choices=CHOICES, null=True, blank=True, default=1, max_length=1)
    volumen = models.IntegerField( verbose_name="Volumen de productos", null=True, blank=True)
    necesidad = models.IntegerField( verbose_name="Necesidad de envase", null=True, blank=True)
    costo = models.IntegerField( verbose_name="Costo unitario", null=True, blank=True)
    costo_anual = models.IntegerField( verbose_name="Costo anual", null=True, blank=True)
    id_estado = models.ForeignKey('plannet.EstadosFinancieros', on_delete=models.CASCADE, related_name='Estado_Envase',null=True, default=None)

class GastoAdministracion(models.Model):
    id_usuario = models.ForeignKey('plannet.Usuarios', on_delete=models.CASCADE, related_name='Usuario_GastoAdministracion',null=True, default=None)
    puesto = models.CharField(max_length=50, verbose_name="Nombre del puesto", null=True, blank=True)
    numero_personas = models.IntegerField( verbose_name="Número de personas", null=True, blank=True)
    pago_mensual = models.IntegerField( verbose_name="Pago mensual", null=True, blank=True)
    pago_anual = models.IntegerField( verbose_name="Pago anual", null=True, blank=True)
    prestaciones = models.IntegerField( verbose_name="Prestaciones 30%", null=True, blank=True)
    total_anual = models.IntegerField( verbose_name="Total anual", null=True, blank=True)
    id_estado = models.ForeignKey('plannet.EstadosFinancieros', on_delete=models.CASCADE, related_name='Estado_GastoAdministracion',null=True, default=None)

class GastoVenta(models.Model):
    id_usuario = models.ForeignKey('plannet.Usuarios', on_delete=models.CASCADE, related_name='Usuario_GastoVenta',null=True, default=None)
    gasto_venta = models.CharField(max_length=50, verbose_name="Descripción del gastode venta", null=True, blank=True)
    unidad = models.CharField(max_length=50, verbose_name="Unidad de medida", null=True, blank=True)
    gasto_unidad = models.IntegerField( verbose_name="Gasto por unidad", null=True, blank=True)
    cantidad = models.IntegerField( verbose_name="Cantidad requerida", null=True, blank=True)
    gasto_anual = models.IntegerField( verbose_name="Gasto por año", null=True, blank=True)
    id_estado = models.ForeignKey('plannet.EstadosFinancieros', on_delete=models.CASCADE, related_name='Estado_GastoVenta',null=True, default=None)


class ManoObra(models.Model):
    id_usuario = models.ForeignKey('plannet.Usuarios', on_delete=models.CASCADE, related_name='Usuario_ManoObra',null=True, default=None)
    puesto = models.CharField(max_length=50, verbose_name="Nombre del puesto", null=True, blank=True)
    numero_trabajadores = models.IntegerField( verbose_name="Número de trabajadores", null=True, blank=True)
    pago_mensual = models.IntegerField( verbose_name="Pago mensual", null=True, blank=True)
    pago_anual = models.IntegerField( verbose_name="Pago anual", null=True, blank=True)
    prestaciones = models.IntegerField( verbose_name="Prestaciones 30%", null=True, blank=True)
    total_anual = models.IntegerField( verbose_name="Total anual", null=True, blank=True)
    id_estado = models.ForeignKey('plannet.EstadosFinancieros', on_delete=models.CASCADE, related_name='Estado_ManoObra',null=True, default=None)

class EstadoResultados(models.Model):
    id_usuario = models.ForeignKey('plannet.Usuarios', on_delete=models.CASCADE, related_name='Usuario_EstadoResultados',null=True, default=None)
    costo_ventas = models.IntegerField( verbose_name="Costo de ventas", null=True, blank=True)
    materias_primas = models.IntegerField( verbose_name="Materias Primas", null=True, blank=True)
    mano_obra = models.IntegerField( verbose_name="Mano de obra", null=True, blank=True)
    utilidad_bruta = models.IntegerField( verbose_name="Utilidad bruta", null=True, blank=True)
    gastos_generales = models.IntegerField( verbose_name="Gastos generales", null=True, blank=True)
    gastos_administracion = models.IntegerField( verbose_name="Gastos de administración", null=True, blank=True)
    gastos_venta = models.IntegerField( verbose_name="Gastos de venta", null=True, blank=True)
    utilidad_antes_impuestos = models.IntegerField( verbose_name="Utiidad antes de impuestos", null=True, blank=True)
    impuesto = models.IntegerField( verbose_name="Impuesto a la utilidad", null=True, blank=True)
    utilidad_neta = models.IntegerField( verbose_name="Utilidad neta", null=True, blank=True)
    id_estado = models.ForeignKey('plannet.EstadosFinancieros', on_delete=models.CASCADE, related_name='Estado_EstadoResultados',null=True, default=None)

class Inversion(models.Model):
    id_usuario = models.ForeignKey('plannet.Usuarios', on_delete=models.CASCADE, related_name='Usuario_Inversion',null=True, default=None)
    tipo_inversion = models.CharField(max_length=50, verbose_name="Tipo de inversión", null=True, blank=True)
    socios = models.IntegerField( verbose_name="Inversión de socios", null=True, blank=True, default=0)
    bancos = models.IntegerField( verbose_name="Inversión de bancos", null=True, blank=True, default=0)
    gobiernof = models.IntegerField( verbose_name="Inversión de gobierno federal", null=True, blank=True, default=0)
    gobiernoe = models.IntegerField( verbose_name="Inversión de gobierno estatal", null=True, blank=True, default=0)
    otras = models.IntegerField( verbose_name="Otras inversiones", null=True, blank=True, default=0)
    total = models.IntegerField( verbose_name="Total", null=True, blank=True)
    id_estado = models.ForeignKey('plannet.EstadosFinancieros', on_delete=models.CASCADE, related_name='Estado_Inversion',null=True, default=None)

class Requerimientos(models.Model):
    CHOICES = [('1', "Funcional"),
                ('2', "No funcional")
                ]
    id_usuario = models.ForeignKey('plannet.Usuarios', on_delete=models.CASCADE, related_name='Usuario_Requerimientos',null=True, default=None)
    numero = models.IntegerField( verbose_name="Volumen de productos", null=True, blank=True)
    tipo_requerimiento = models.CharField(choices=CHOICES, null=True, blank=True, default=1, max_length=1)
    Requerimiento = models.CharField(max_length=50, verbose_name="Descripción del requerimiento", null=True, blank=True)
    id_estado = models.ForeignKey('plannet.EstadosFinancieros', on_delete=models.CASCADE, related_name='Estado_Requerimientos',null=True, default=None)

class Gantt(models.Model):
    CHOICES = [('1', "Planeación"),('2', "Análisis"), ('3', "Diseño"), ('4', "Desarrollo"),
                ('5', "Pruebas"), ('6', "Implementación"), ('7', "Cierre del proyecto")
    ]
    CHOICES2 = [('1', "No iniciada"), ('2', "En progreso"), ('3', "Finalizada")]
    id_usuario = models.ForeignKey('plannet.Usuarios', on_delete=models.CASCADE, related_name='Usuario_Gantt',null=True, default=None)
    fase = models.CharField(choices=CHOICES, null=True, blank=True, default=1, max_length=1)
    numtarea = models.IntegerField( verbose_name="Número de tarea", null=True, blank=True)
    asignado = models.CharField(max_length=80, verbose_name="Asignado a", null=True, blank=True)
    estado = models.CharField(choices=CHOICES2, null=True, blank=True, default=1, max_length=1)
    fechaini = models.DateField(verbose_name="Fecha inicial")
    fechafin = models.DateField(verbose_name="Fecha final")
    notas = models.CharField(max_length=100, verbose_name="Notas y comentarios", null=True, blank=True)
    predecesora = models.IntegerField( verbose_name="Tarea predecesora", null=True, blank=True)
    id_estado = models.ForeignKey('plannet.EstadosFinancieros', on_delete=models.CASCADE, related_name='Estado_Gantt',null=True, default=None)


class DisArquitectura(models.Model):
    id_usuario = models.ForeignKey('plannet.Usuarios', on_delete=models.CASCADE, related_name='Usuario_DisArquitectura',null=True, default=None)
    archivo = models.FileField()
    id_estado = models.ForeignKey('plannet.EstadosFinancieros', on_delete=models.CASCADE, related_name='Estado_DisArquitectura',null=True, default=None)

class ActPruebas(models.Model):
    id_usuario = models.ForeignKey('plannet.Usuarios', on_delete=models.CASCADE, related_name='Usuario_ActPruebas',null=True, default=None)
    archivo = models.FileField()
    id_estado = models.ForeignKey('plannet.EstadosFinancieros', on_delete=models.CASCADE, related_name='Estado_ActPruebas',null=True, default=None)

class ActDespliegue(models.Model):
    id_usuario = models.ForeignKey('plannet.Usuarios', on_delete=models.CASCADE, related_name='Usuario_ActDespliegue',null=True, default=None)
    archivo = models.FileField()
    id_estado = models.ForeignKey('plannet.EstadosFinancieros', on_delete=models.CASCADE, related_name='Estado_ActDespliegue',null=True, default=None)

class Documentacion(models.Model):
    id_usuario = models.ForeignKey('plannet.Usuarios', on_delete=models.CASCADE, related_name='Usuario_Documentacion',null=True, default=None)
    archivo = models.FileField()
    id_estado = models.ForeignKey('plannet.EstadosFinancieros', on_delete=models.CASCADE, related_name='Estado_Documentacion',null=True, default=None)



class Retroalimentacion(models.Model):
    CHOICES = [('1', 1), ('2', 2), ('3', 3), ('4', 4), ('5', 5),
                ('6', 6), ('7', 7), ('8', 8), ('9', 9), ('10', 10)
                ]
    id_usuario = models.ForeignKey('plannet.Usuarios', on_delete=models.CASCADE, related_name='Usuario_Retroalimentacion',null=True, default=None)
    calificacion = models.IntegerField(choices=CHOICES, null=True, blank=True, default=1, max_length=2)
    comentario = models.CharField(max_length=50, verbose_name="Retroalimentación", null=True, blank=True)
    id_estado = models.ForeignKey('plannet.EstadosFinancieros', on_delete=models.CASCADE, related_name='Estado_Retroalimentacion',null=True, default=None)
