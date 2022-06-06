from django import forms
from .models import Coach, Emprendedor, Estudiante, Profesor, Usuarios
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
        