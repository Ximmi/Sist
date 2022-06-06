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




class GrupoForm(forms.ModelForm):
    class Meta:
        model = Grupos
        fields = '__all__'