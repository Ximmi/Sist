from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Usuarios
from .forms import UsuarioForm
# Create your views here.

def inicio(request):
    return render(request, 'paginas/inicio.html')

def nosotros(request):
    return render(request, 'paginas/nosotros.html')

def registro(request):
    formulario = UsuarioForm(request.POST or None, request.FILES or None)
    if formulario.is_valid():
        formulario.save()
        return redirect('inicio')
    return render(request, 'usuarios/registro.html', {'formulario': formulario})

def inicio_sesion(request):
    return render(request, 'usuarios/inicio_sesion.html')

def terminos(request):
    return render(request, 'usuarios/terminos.html')

def editar_perfil(request):
    return render(request, 'usuarios/editar_perfil.html')

def inicios(request):
    return render(request, 'usuarios/inicios.html')

def consulta_grupo(request):
    usuarios = Usuarios.objects.all()
    return render(request, 'usuarios/consulta_grupo.html', {'usuarios': usuarios})

def consulta_temas(request):
    return render(request, 'plan/consulta_temas.html')

def consulta_estados(request):
    return render(request, 'proyecciones/consulta_estados.html')

def consulta_graficas(request):
    return render(request, 'graficas/consulta_graficas.html')
 
def consulta_escenarios(request):
    return render(request, 'simulador/consulta_escenarios.html')

def genera_prediccion(request):
    return render(request, 'predicciones/genera_prediccion.html')