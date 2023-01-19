from django.utils.html import format_html
import django_tables2 as tables
import babel.numbers
from django_tables2.utils import A
from .models import Grupos, Inversion, Usuarios, PlandeNegocio, Ingresos, Materiales, Envase, Requerimientos, Gantt

def FormatoMoneda(value):
    return babel.numbers.format_currency(value, 'MXN', locale="es_MX")

class SummingColumn(tables.Column):
    def render_footer(self, bound_column, table):
        return FormatoMoneda(sum(bound_column.accessor.resolve(row) for row in table.data))

class SummingColumnNormal(tables.Column):
    def render_footer(self, bound_column, table):
        return sum(bound_column.accessor.resolve(row) for row in table.data)

class GrupoTable(tables.Table):
    portafolio = tables.LinkColumn("consulta_portafolio",
                                        verbose_name="Portafolio de evidencias",
                                        text ="Ver portafolio",
                                        args = [A("pk")],
                                        attrs={"a":{"class":"btn btn-light"}},
                                        orderable=False
                                        )                                      
    class Meta:
        model = Usuarios
        template_name = "django_tables2/bootstrap4.html"
        fields = ("foto","nombre", "apellido", "num", "portafolio" ) 
        attrs = {"class": "table table-hover"}

    def render_foto(self, value):
        return format_html("<img src=\"/images/{}\" class=\"rounded-circle\" height=\"30\" width=\"30\">", value)

    def before_render(self, request):
        #if request.user.has_perm('plannet.view_plandenegocio'):
        if request.user.tipo == '2':
            self.columns.show('portafolio')
            print('cayo en el if')
        else:
            #self.columns.show('portafolio')
            print('cayo en el else')



class IngresosTable(tables.Table):
    editar = tables.LinkColumn("edita_ingreso",
                                        verbose_name="Edita ingreso",
                                        text ="Editar",
                                        args = [A("pk")],
                                        attrs={"a":{"class":"btn btn-colores"}},
                                        orderable=False
                                        )
    eliminar = tables.LinkColumn("elimina_ingreso",
                                        verbose_name="Elimina ingreso",
                                        text ="Eliminar",
                                        args = [A("pk")],
                                        attrs={"a":{"class":"btn btn-lila"}},
                                        orderable=False
                                        )
    ingresos = SummingColumn()
    precio_unitario = tables.Column(footer="Total: ")

    def render_precio_unitario(self, value):
        return format_html("{}", FormatoMoneda(value))

    def render_ingresos(self,value):
        return format_html("{}", FormatoMoneda(value))

    class Meta:
        model = Ingresos
        template_name = "django_tables2/bootstrap4.html"
        fields = ("producto","unidades", "precio_unitario", "ingresos", "editar", "eliminar") 
        attrs = {"class": "table table-hover"}

    

class MaterialesTable(tables.Table):

    editar = tables.LinkColumn("edita_materiales",
                                        verbose_name="Edita materiales",
                                        text ="Editar",
                                        args = [A("pk")],
                                        attrs={"a":{"class":"btn btn-colores"}},
                                        orderable=False
                                        )
    eliminar = tables.LinkColumn("elimina_materiales",
                                        verbose_name="Elimina materiales",
                                        text ="Eliminar",
                                        args = [A("pk")],
                                        attrs={"a":{"class":"btn btn-lila"}},
                                        orderable=False
                                        )

    costo_anual = SummingColumn()
    volumen = tables.Column(footer="Total: ")

    def render_costo(self, value):
        return format_html("{}", FormatoMoneda(value))

    def render_costo_anual(self,value):
        return format_html("{}", FormatoMoneda(value))

    class Meta:
        model = Materiales
        template_name = "django_tables2/bootstrap4.html"
        fields = ("material","unidad_medida", "costo", "volumen", "costo_anual", "editar", "eliminar") 
        attrs = {"class": "table table-hover"}


class EnvaseTable(tables.Table):

    editar = tables.LinkColumn("edita_envase",
                                        verbose_name="Edita envase",
                                        text ="Editar",
                                        args = [A("pk")],
                                        attrs={"a":{"class":"btn btn-colores"}},
                                        orderable=False
                                        )
    eliminar = tables.LinkColumn("elimina_envase",
                                        verbose_name="Elimina envase",
                                        text ="Eliminar",
                                        args = [A("pk")],
                                        attrs={"a":{"class":"btn btn-lila"}},
                                        orderable=False
                                        )

    costo_anual = SummingColumn()
    costo = tables.Column(footer="Total: ")

    def render_costo(self, value):
        return format_html("{}", FormatoMoneda(value))

    def render_costo_anual(self,value):
        return format_html("{}", FormatoMoneda(value))

    class Meta:
        model = Envase
        template_name = "django_tables2/bootstrap4.html"
        fields = ("tipo_envase","volumen", "necesidad", "costo", "costo_anual", "editar", "eliminar") 
        attrs = {"class": "table table-hover"}


class GastoAdministracionTable(tables.Table):

    editar = tables.LinkColumn("edita_gastoadministracion",
                                        verbose_name="Edita puesto",
                                        text ="Editar",
                                        args = [A("pk")],
                                        attrs={"a":{"class":"btn btn-colores"}},
                                        orderable=False
                                        )
    eliminar = tables.LinkColumn("elimina_gastoadministracion",
                                        verbose_name="Elimina puesto",
                                        text ="Eliminar",
                                        args = [A("pk")],
                                        attrs={"a":{"class":"btn btn-lila"}},
                                        orderable=False
                                        )
    numero_personas = SummingColumnNormal()
    pago_mensual = SummingColumn()
    pago_anual = SummingColumn()
    total_anual = SummingColumn()
    prestaciones = SummingColumn()
    puesto = tables.Column(footer="Total: ")

    def render_pago_mensual(self, value):
        return format_html("{}", FormatoMoneda(value))

    def render_pago_anual(self,value):
        return format_html("{}", FormatoMoneda(value))

    def render_prestaciones(self, value):
        return format_html("{}", FormatoMoneda(value))

    def render_total_anual(self,value):
        return format_html("{}", FormatoMoneda(value))

    class Meta:
        model = Envase
        template_name = "django_tables2/bootstrap4.html"
        fields = ("puesto","numero_personas", "pago_mensual", "pago_anual", "prestaciones", "total_anual", "editar", "eliminar") 
        attrs = {"class": "table table-hover"}


class GastoVentaTable(tables.Table):

    editar = tables.LinkColumn("edita_gastoventa",
                                        verbose_name="Edita gasto de venta",
                                        text ="Editar",
                                        args = [A("pk")],
                                        attrs={"a":{"class":"btn btn-colores"}},
                                        orderable=False
                                        )
    eliminar = tables.LinkColumn("elimina_gastoventa",
                                        verbose_name="Elimina gasto de venta",
                                        text ="Eliminar",
                                        args = [A("pk")],
                                        attrs={"a":{"class":"btn btn-lila"}},
                                        orderable=False
                                        )

    gasto_anual = SummingColumn()
    cantidad = tables.Column(footer="Total: ")

    def render_gasto_unidad(self, value):
        return format_html("{}", FormatoMoneda(value))

    def render_gasto_anual(self,value):
        return format_html("{}", FormatoMoneda(value))

    class Meta:
        model = Envase
        template_name = "django_tables2/bootstrap4.html"
        fields = ("gasto_venta","unidad", "gasto_unidad", "cantidad", "gasto_anual", "editar", "eliminar") 
        attrs = {"class": "table table-hover"}


class ManoObraTable(tables.Table):

    editar = tables.LinkColumn("edita_manoobra",
                                        verbose_name="Edita puesto",
                                        text ="Editar",
                                        args = [A("pk")],
                                        attrs={"a":{"class":"btn btn-colores"}},
                                        orderable=False
                                        )
    eliminar = tables.LinkColumn("elimina_manoobra",
                                        verbose_name="Elimina puesto",
                                        text ="Eliminar",
                                        args = [A("pk")],
                                        attrs={"a":{"class":"btn btn-lila"}},
                                        orderable=False
                                        )

    numero_trabajadores = SummingColumnNormal()
    pago_mensual = SummingColumn()
    pago_anual = SummingColumn()
    total_anual = SummingColumn()
    prestaciones = SummingColumn()
    puesto = tables.Column(footer="Total: ")

    def render_pago_mensual(self, value):
        return format_html("{}", FormatoMoneda(value))

    def render_pago_anual(self,value):
        return format_html("{}", FormatoMoneda(value))

    def render_prestaciones(self, value):
        return format_html("{}", FormatoMoneda(value))

    def render_total_anual(self,value):
        return format_html("{}", FormatoMoneda(value))

    class Meta:
        model = Envase
        template_name = "django_tables2/bootstrap4.html"
        fields = ("puesto","numero_trabajadores", "pago_mensual", "pago_anual", "prestaciones", "total_anual", "editar", "eliminar") 
        attrs = {"class": "table table-hover"}


class InversionesTable(tables.Table):

    editar = tables.LinkColumn("edita_inversion",
                                        verbose_name="Edita tipo de inversión",
                                        text ="Editar",
                                        args = [A("pk")],
                                        attrs={"a":{"class":"btn btn-colores"}},
                                        orderable=False
                                        )
    eliminar = tables.LinkColumn("elimina_inversion",
                                        verbose_name="Elimina tipo de inversión",
                                        text ="Eliminar",
                                        args = [A("pk")],
                                        attrs={"a":{"class":"btn btn-lila"}},
                                        orderable=False
                                        )

    socios = SummingColumn()
    bancos = SummingColumn()
    gobiernof = SummingColumn()
    gobiernoe =SummingColumn()
    otras = SummingColumn()
    total = SummingColumn()
    tipo_inversion = tables.Column(footer="Total: ")

    def render_socios(self, value):
        return format_html("{}", FormatoMoneda(value))

    def render_bancos(self,value):
        return format_html("{}", FormatoMoneda(value))

    def render_gobiernof(self,value):
        return format_html("{}", FormatoMoneda(value))

    def render_gobiernoe(self,value):
        return format_html("{}", FormatoMoneda(value))

    def render_otras(self,value):
        return format_html("{}", FormatoMoneda(value))

    def render_total(self,value):
        return format_html("{}", FormatoMoneda(value))

    class Meta:
        model = Inversion
        template_name = "django_tables2/bootstrap4.html"
        fields = ("tipo_inversion","socios", "bancos", "gobiernof", "gobiernoe", "otras", "total", "editar", "eliminar") 
        attrs = {"class": "table table-hover"}


class RequerimientosTable(tables.Table):
    editar = tables.LinkColumn("edita_requerimiento",
                                        verbose_name="Edita requerimiento",
                                        text ="Editar",
                                        args = [A("pk")],
                                        attrs={"a":{"class":"btn btn-colores"}},
                                        orderable=False
                                        )
    eliminar = tables.LinkColumn("elimina_requerimiento",
                                        verbose_name="Elimina requerimiento",
                                        text ="Eliminar",
                                        args = [A("pk")],
                                        attrs={"a":{"class":"btn btn-lila"}},
                                        orderable=False
                                        )
    class Meta:
        model = Requerimientos
        template_name = "django_tables2/bootstrap4.html"
        fields = ("numero","tipo_requerimiento", "Requerimiento", "editar", "eliminar") 
        attrs = {"class": "table table-hover"}


class GanttTable(tables.Table):
    editar = tables.LinkColumn("edita_tarea",
                                        verbose_name="Edita tarea",
                                        text ="Editar",
                                        args = [A("pk")],
                                        attrs={"a":{"class":"btn btn-colores"}},
                                        orderable=False
                                        )
    eliminar = tables.LinkColumn("elimina_tarea",
                                        verbose_name="Elimina tarea",
                                        text ="Eliminar",
                                        args = [A("pk")],
                                        attrs={"a":{"class":"btn btn-lila"}},
                                        orderable=False
                                        )
    class Meta:
        model = Gantt
        template_name = "django_tables2/bootstrap4.html"
        fields = ("fase","numtarea", "asignado", "estado", "fechaini", "fechafin", "notas", "predecesora",
         "editar", "eliminar") 
        attrs = {"class": "table table-hover"}


