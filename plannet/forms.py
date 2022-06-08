from django import forms
from .models import Coach, Emprendedor, Estudiante, GastoAdministracion, GastoVenta, Ingresos, ManoObra, Materiales, Profesor, Usuarios, Envase
from .models import Grupos
from django.utils.safestring import mark_safe
from django.contrib.auth import authenticate

class UsuarioForm(forms.ModelForm):
    password2 = forms.CharField(label="Contraseña", widget = forms.PasswordInput()) 
    passwordconfirm = forms.CharField(label="Confirmar contraseña", widget = forms.PasswordInput()) 
    terminos = forms.BooleanField(label=mark_safe('Acepto <a href="/terminos" target="_blank">Términos y condiciones</a>'))
    class Meta:
        model = Usuarios
        fields = ['nombre', 'apellido', 'correo', 'password2','passwordconfirm', 'foto', 'tipo']


    def clean_passwordconfirm(self):
        if self.cleaned_data['password2'] != self.cleaned_data['passwordconfirm']:
            self.add_error('password2', 'Las contraseñas no son iguales')

class  EditaEstudianteForm(forms.ModelForm):
    class Meta:
        model = Estudiante
        fields = ['foto', 'boleta']

class  EditaProfesorForm(forms.ModelForm):
    class Meta:
        model = Profesor
        fields = ['correo','foto', 'rfc', 'clave_institucion']

class EditaCoachForm(forms.ModelForm):
    class Meta:
        model = Coach
        fields = ['foto', 'rfc']

class EditaEmprendedorForm(forms.ModelForm):
    class Meta:
        model = Emprendedor
        fields = ['foto']




class LoginForm(forms.Form):
    correo = forms.CharField(
        label='correo',
        
    )

    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(
        )
    )

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        correo = self.cleaned_data['correo']
        password = self.cleaned_data['password']

        if not authenticate(correo=correo, password=password):
            raise forms.ValidationError('Los datos de usuario no son correctos')

        return self.cleaned_data




class GrupoForm(forms.Form):
    nombre_grupo = forms.CharField(
        label='Nombre del grupo', 
    )

    clave = forms.CharField(
        label='Clave',
    )
    class Meta:
        model = Grupos
        fields = ['nombre_grupo', 'clave']

    def clean(self):
        cleaned_data = super(GrupoForm, self).clean()
        nombre_grupo = self.cleaned_data['nombre_grupo']
        clave = self.cleaned_data['clave']

        query = Grupos.objects.filter(nombre_grupo=nombre_grupo, clave=clave).all()
        print(query)
        if  len(query) == 0:
            raise forms.ValidationError('El grupo no existe')
            self.add_error('clave', "Este es un error")
        
        return self.cleaned_data
        
class CreaGrupoForm(forms.ModelForm):
    nombre_grupo = forms.CharField(
        label='Nombre del grupo', 
    )

    clave = forms.CharField(
        label='Clave',
    )
    class Meta:
        model = Grupos
        fields = ['nombre_grupo', 'clave']

class AgregaIngresosForm(forms.ModelForm):
    ingresos = forms.IntegerField(
        disabled= True,
        required= False
    )
    class Meta:
        model = Ingresos
        fields = ['producto', 'unidades', 'precio_unitario', 'ingresos']


class AgregaMaterialesForm(forms.ModelForm):
    costo_anual = forms.IntegerField(
        disabled= True,
        required= False
    )
    class Meta:
        model = Materiales
        fields = ['material', 'unidad_medida', 'costo', 'volumen', 'costo_anual']

class AgregaEnvaseForm(forms.ModelForm):
    costo_anual = forms.IntegerField(
        disabled= True,
        required= False
    )
    class Meta:
        model = Envase
        fields = ['tipo_envase', 'volumen', 'necesidad', 'costo', 'costo_anual']

class AgregaGastoAdministracionForm(forms.ModelForm):
    pago_anual = forms.IntegerField(
        disabled= True,
        required= False
    )
    prestaciones = forms.IntegerField(
        disabled= True,
        required= False
    )
    total_anual = forms.IntegerField(
        disabled= True,
        required= False
    )
    class Meta:
        model = GastoAdministracion
        fields = ['puesto', 'numero_personas', 'pago_mensual', 'pago_anual', 'prestaciones', 'total_anual']

class AgregaGastoVentaForm(forms.ModelForm):
    gasto_anual = forms.IntegerField(
        disabled= True,
        required= False
    )
    class Meta:
        model = GastoVenta
        fields = ['gasto_venta', 'unidad', 'gasto_unidad', 'cantidad', 'gasto_anual']

class AgregaManoObraForm(forms.ModelForm):
    pago_anual = forms.IntegerField(
        disabled= True,
        required= False
    )
    prestaciones = forms.IntegerField(
        disabled= True,
        required= False
    )
    total_anual = forms.IntegerField(
        disabled= True,
        required= False
    )
    class Meta:
        model = ManoObra
        fields = ['puesto', 'numero_trabajadores', 'pago_mensual', 'pago_anual', 'prestaciones', 'total_anual']