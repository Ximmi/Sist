from cgitb import handler
from urllib.request import Request
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Emprendedor, Profesor, Usuarios, Coach, Estudiante, Emprendedor
from .forms import EditaCoachForm, LoginForm, UsuarioForm, EditaProfesorForm, EditaEmprendedorForm, EditaEstudianteForm, GrupoForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db import IntegrityError, transaction

# Create your views here.


def inicio(request):
    return render(request, 'paginas/inicio.html')
    # registro


def nosotros(request):
    return render(request, 'paginas/nosotros.html')


def contacto(request):
    return render(request, 'paginas/contacto.html')


def politicas(request):
    return render(request, 'paginas/politicas.html')


def productos(request):
    return render(request, 'paginas/productos.html')


def registro(request):
    formulario = UsuarioForm(request.POST or None, request.FILES or None)
    if formulario.is_valid():

        with transaction.atomic():
            # print(formulario.save())
            # Usuario.set_password(formulario.cleaned_data['password2'])
            # Usuario.save()
            tipo = formulario.cleaned_data['tipo']
            
            print(str(tipo))
            if(tipo == '1'):  # si es estudiante
                from .models import Estudiante
                estudiante = Estudiante.objects.create_user(
                    correo=formulario.cleaned_data['correo'],
                    password=formulario.cleaned_data['password2'],
                    nombre=formulario.cleaned_data['nombre'],
                    apellido=formulario.cleaned_data['apellido'],
                    foto=formulario.cleaned_data['foto'],
                    tipo=formulario.cleaned_data['tipo']
                )
                print(estudiante)

            elif(tipo == '2'):  # si es emprendedor
                from .models import Emprendedor
                # .objects indica que hace uso de todas las funciones definidas, incluidas las del manager
                emprendedor = Emprendedor.objects.create_user(
                    correo=formulario.cleaned_data['correo'],
                    password=formulario.cleaned_data['password2'],
                    nombre=formulario.cleaned_data['nombre'],
                    apellido=formulario.cleaned_data['apellido'],
                    foto=formulario.cleaned_data['foto'],
                    tipo=formulario.cleaned_data['tipo']
                )
                print(emprendedor)

            elif(tipo == '3'):  # si es profesor
                from .models import Profesor
                profesor = Profesor.objects.create_user(
                    correo=formulario.cleaned_data['correo'],
                    password=formulario.cleaned_data['password2'],
                    nombre=formulario.cleaned_data['nombre'],
                    apellido=formulario.cleaned_data['apellido'],
                    foto=formulario.cleaned_data['foto'],
                    tipo=formulario.cleaned_data['tipo']
                )
                print(profesor)

            elif(tipo == '4'):  # si es coach
                from .models import Coach
                coach = Coach.objects.create_user(
                    correo=formulario.cleaned_data['correo'],
                    password=formulario.cleaned_data['password2'],
                    nombre=formulario.cleaned_data['nombre'],
                    apellido=formulario.cleaned_data['apellido'],
                    foto=formulario.cleaned_data['foto'],
                    tipo=formulario.cleaned_data['tipo']
                )
                print(coach)
            else:
                print("No es ninguno de los tipos anteriores")
            messages.success(request, "Registro existoso")
            return redirect('inicio')

    return render(request, 'usuarios/llenarformulario.html', {'formulario': formulario, 'subtitulo': "Registro de cuenta", 'boton': "Regístrame"})


def inicio_sesion(request):
    formulario = LoginForm(request.POST or None, request.FILES or None)
    if formulario.is_valid():
        session = authenticate(
            correo=formulario.cleaned_data['correo'],
            password=formulario.cleaned_data['password']
        )
        if session.is_active:
            login(request, session)
        else:
            messages.error(request, 'La cuenta no se encuentra activa')
        return redirect('inicio')
    return render(request, 'usuarios/llenarformulario.html', {'formulario': formulario, 'subtitulo': "Iniciar sesión", 'boton': "Ingresar"})


def cerrar_sesion(request):
    logout(request)
    messages.success(request, "Sesión terminada")
    return redirect('inicio')


def terminos(request):
    return render(request, 'usuarios/terminos.html')


def editar_perfil(request):
    print(request.user)
    usuario = request.user
    tipo = usuario.get_tipo_display()
    
    if(tipo == "Profesor"):
        profesor = Profesor.objects.get(id=request.user.id)
        formulario = EditaProfesorForm(
            request.POST or None, request.FILES or None,
            instance=profesor
        )
    elif(tipo == "Coach"):
        coach = Coach.objects.get(id=request.user.id)
        formulario = EditaCoachForm(
            request.POST or None, request.FILES or None,
            instance=coach
        )
    elif(tipo == "Estudiante"):
        estudiante = Estudiante.objects.get(id=request.user.id)
        formulario = EditaEstudianteForm(
            request.POST or None, request.FILES or None,
            instance=estudiante
        )
    elif(tipo == "Emprendedor"):
        #emprendedor = Emprendedor.get(id=request.user.id)
        formulario = EditaEmprendedorForm(
            request.POST or None, request.FILES or None,
            #instance=emprendedor
            instance=request.user
        )
    # def valid_validform...
    if request.method == 'POST':
        if formulario.is_valid():
            usuarioModificado = formulario.save()
            usuarioModificado.save()
            messages.success(request, "Perfil actualizado")
            return redirect('inicio')

    return render(request, 'usuarios/editar_perfil.html', {'form': formulario, 'subtitulo': " ", 'boton': "Editar", 'title':"Editar perfil"}) 




def consulta_grupo(request):
    #usuarios = Usuarios.objects.all()
    #return render(request, 'usuarios/consulta_grupo.html', {'usuarios': usuarios})
    formulario = GrupoForm(request.POST or None, request.FILES or None)

    if formulario.is_valid():
        with transaction.atomic():
            from .models import Grupos
            nombre_grupo = formulario.cleaned_data['nombre_grupo']
            clave = formulario.cleaned_data['clave']
            grupo = Grupos.objects.filter(nombre_grupo=nombre_grupo, clave=clave).all()[0]
            #user = Usuarios.objects.filter(id=request.user.id)
            user = request.user
            user.id_grupo = grupo
            user.save()
            messages.success(request, "Te has inscrito a un grupo")
            return redirect('inicio')

    context = {'formulario': formulario, 'subtitulo': "Inscríbete en un grupo", 'boton': "Inscribirme", 'grupos': request.user.trae_grupos()}
    return render(request, 'usuarios/consulta_grupo.html', context=context)

def crea_grupo(request):
    formulario = GrupoForm(request.POST or None, request.FILES or None)
    if formulario.is_valid():
        from .models import Grupos
        grupo = Grupos.objects.create_grupo(
            nombre_grupo = formulario.cleaned_data['nombre_grupo'],
            clave = formulario.cleaned_data['clave'],
            id_responsable = request.user
            )
        messages.success(request, "Grupo agregado")
        return redirect('inicio')
    context = {'formulario': formulario, 'subtitulo': "Crea un grupo", 'boton': "Crear"}
    return render(request, 'usuarios/crea_grupo.html', context=context)


def consulta_temas(request):
    return render(request, 'plan/consulta_temas.html')


def consulta_estados(request):
    return render(request, 'proyecciones/consulta_estados.html')


def consulta_graficas(request):
    tipo_1 = Usuarios.objects.filter(tipo='1').count
    tipo_1 = int(tipo_1)
    print("Usuarios estudiantes: " + str(tipo_1))

    tipo_2 = Usuarios.objects.filter(tipo='2').count
    tipo_2 = int(tipo_2)
    print("Usuarios estudiantes: " + str(tipo_2))

    tipo_3 = Usuarios.objects.filter(tipo='3').count
    tipo_3 = int(tipo_3)
    print("Usuarios estudiantes: " + str(tipo_3))

    tipo_4 = Usuarios.objects.filter(tipo='4').count
    tipo_4 = int(tipo_4)
    print("Usuarios estudiantes: " + str(tipo_4))

    tipo_list = ['Estudiante', 'Emprendedor', 'Profesor', 'Coach']
    number_list = [tipo_1, tipo_2, tipo_3, tipo_4]
    context = {'tipo_list':tipo_list, 'number_list':number_list}

    return render(request, 'graficas/consulta_graficas.html', context)


def consulta_escenarios(request):
    return render(request, 'simulador/consulta_escenarios.html')


def genera_prediccion(request):
    return render(request, 'predicciones/genera_prediccion.html')

def consulta_planes(request):
    return render(request,'plan/consulta_planes.html')

#Temas del plan
def tema0_1(request):
    return render(request,'temas/tema0_1.html')

def tema1_1(request):
    return render(request,'temas/tema1_1.html')

def tema1_2(request):
    return render(request,'temas/tema1_2.html')
    
def tema1_3(request):
    return render(request,'temas/tema1_3.html')

def tema1_4(request):
    return render(request,'temas/tema1_4.html')
