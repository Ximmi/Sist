from cgitb import handler
import json 
from django.urls import reverse
from django.core.serializers.json import DjangoJSONEncoder
from urllib.request import Request
from django.shortcuts import get_object_or_404, render, redirect
from django.http import Http404, HttpResponse, HttpResponseNotFound, HttpResponseRedirect

from .tables import EnvaseTable, GastoAdministracionTable, GastoVentaTable, GrupoTable, IngresosTable, ManoObraTable, MaterialesTable
from .models import Emprendedor, Envase, EstadosFinancieros, GastoAdministracion, GastoVenta, Grupos, Ingresos, ManoObra, Materiales, Profesor, Usuarios, Coach, Estudiante, Emprendedor, EstadosFinancieros
from .forms import AgregaGastoAdministracionForm, AgregaGastoVentaForm, AgregaManoObraForm, EditaCoachForm, LoginForm, UsuarioForm, EditaProfesorForm, EditaEmprendedorForm, EditaEstudianteForm, GrupoForm, CreaGrupoForm, AgregaIngresosForm, AgregaMaterialesForm, AgregaEnvaseForm
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
    formulario = CreaGrupoForm(request.POST or None, request.FILES or None)
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
    estados = EstadosFinancieros.objects.all()
    return render(request, 'proyecciones/consulta_estados.html', {'estados': estados})


def consulta_graficas(request):
    js='/js/Graficas/graficas.js'
    ingreso_grafica = (
        Ingresos.objects.filter(id_usuario=request.user).values('producto', 'ingresos')
    )    
    jingreso_grafica = json.dumps(list(ingreso_grafica), cls=DjangoJSONEncoder)
    print(jingreso_grafica)
    context = {'js':js, 'jdumps':jingreso_grafica}
    return render(request, 'graficas/consulta_graficas.html', context=context)


def consulta_escenarios(request):
    return render(request, 'simulador/consulta_escenarios.html')


def genera_prediccion(request):
    return render(request, 'predicciones/genera_prediccion.html')

def consulta_planes(request, pk):
    return render(request,'plan/consulta_planes.html')

def ver_grupo(request, id_grupo):
    try:
        grupo = Grupos.objects.get(pk=id_grupo)
        tabla = GrupoTable(Usuarios.objects.filter(id_grupo=id_grupo), per_page_field=5)
        
    except Grupos.DoesNotExist:
        raise Http404("El grupo no existe")
    context = {'title': "Ver grupo",'subtitulo':grupo.nombre_grupo, 'tabla': tabla}
    return render(request,'usuarios/tabla_generica.html', context)


def estado(request, pk):
    try:
        estado = EstadosFinancieros.objects.get(pk=pk)
        if(pk=='4'):
            js='/js/EstadosFinancieros/ingresos.js'
            from .models import Ingresos
            tabla = IngresosTable(Ingresos.objects.filter(id_estado=estado, id_usuario = request.user), per_page_field=5)
            formulario = AgregaIngresosForm(request.POST or None, request.FILES or None)
            if formulario.is_valid():
                ingreso = Ingresos.objects.model(
                    id_usuario = request.user,
                    producto = formulario.cleaned_data['producto'],
                    unidades = formulario.cleaned_data['unidades'],
                    precio_unitario = formulario.cleaned_data['precio_unitario'],
                    ingresos = formulario.cleaned_data['unidades']*formulario.cleaned_data['precio_unitario'],
                    id_estado = estado
                )
                ingreso.save()
                messages.success(request, "Producto agregado")
                return HttpResponseRedirect(reverse('estado', args=(estado.id,)))
        elif(pk == '5'):
            js='/js/EstadosFinancieros/materiales.js'
            from .models import Materiales
            tabla = MaterialesTable(Materiales.objects.filter(id_estado=estado, id_usuario = request.user), per_page_field=5)
            formulario = AgregaMaterialesForm(request.POST or None, request.FILES or None)
            if formulario.is_valid():
                material = Materiales.objects.model(
                    id_usuario = request.user,
                    material = formulario.cleaned_data['material'],
                    unidad_medida = formulario.cleaned_data['unidad_medida'],
                    costo = formulario.cleaned_data['costo'],
                    volumen = formulario.cleaned_data['volumen'],
                    costo_anual = formulario.cleaned_data['costo']*formulario.cleaned_data['volumen'],
                    id_estado = estado
                )
                material.save()
                messages.success(request, "Material agregado")
                return HttpResponseRedirect(reverse('estado', args=(estado.id,)))
        elif(pk == '6'):
            js='/js/EstadosFinancieros/envase.js'
            from .models import Envase
            tabla = EnvaseTable(Envase.objects.filter(id_estado=estado, id_usuario = request.user), per_page_field=5)
            formulario = AgregaEnvaseForm(request.POST or None, request.FILES or None)
            if formulario.is_valid():
                envase = Envase.objects.model(
                    id_usuario = request.user,
                    tipo_envase = formulario.cleaned_data['tipo_envase'],
                    volumen = formulario.cleaned_data['volumen'],
                    necesidad = formulario.cleaned_data['necesidad'],
                    costo = formulario.cleaned_data['costo'],
                    costo_anual = formulario.cleaned_data['costo']*formulario.cleaned_data['necesidad'],
                    id_estado = estado
                )
                envase.save()
                messages.success(request, "Envase, empaque o embalaje agregado")
                return HttpResponseRedirect(reverse('estado', args=(estado.id,)))
        elif(pk == '7'):
            js='/js/EstadosFinancieros/gastoadministracion.js'
            from .models import GastoAdministracion
            tabla = GastoAdministracionTable(GastoAdministracion.objects.filter(id_estado=estado, id_usuario = request.user), per_page_field=5)
            formulario = AgregaGastoAdministracionForm(request.POST or None, request.FILES or None)
            if formulario.is_valid():
                gasto = GastoAdministracion.objects.model(
                    id_usuario = request.user,
                    puesto = formulario.cleaned_data['puesto'],
                    numero_personas = formulario.cleaned_data['numero_personas'],
                    pago_mensual = formulario.cleaned_data['pago_mensual'],
                    pago_anual = formulario.cleaned_data['pago_mensual']*12,
                    prestaciones = formulario.cleaned_data['pago_mensual']*3.6,
                    total_anual = formulario.cleaned_data['pago_mensual']*3.6*formulario.cleaned_data['numero_personas'],
                    id_estado = estado
                )
                gasto.save()
                messages.success(request, "Puesto agregado")
                return HttpResponseRedirect(reverse('estado', args=(estado.id,)))
        elif(pk == '8'):
            js='/js/EstadosFinancieros/gastosventa.js'
            from .models import GastoVenta
            tabla = GastoVentaTable(GastoVenta.objects.filter(id_estado=estado, id_usuario = request.user), per_page_field=5)
            formulario = AgregaGastoVentaForm(request.POST or None, request.FILES or None)
            if formulario.is_valid():
                gastov = GastoVenta.objects.model(
                    id_usuario = request.user,
                    gasto_venta = formulario.cleaned_data['gasto_venta'],
                    unidad = formulario.cleaned_data['unidad'],
                    gasto_unidad = formulario.cleaned_data['gasto_unidad'],
                    cantidad = formulario.cleaned_data['cantidad'],
                    gasto_anual = formulario.cleaned_data['gasto_unidad']*formulario.cleaned_data['cantidad'],
                    id_estado = estado
                )
                gastov.save()
                messages.success(request, "Gasto de venta agregado")
                return HttpResponseRedirect(reverse('estado', args=(estado.id,)))
        elif(pk == '9'):
            js='/js/EstadosFinancieros/manoobra.js'
            from .models import ManoObra
            tabla = ManoObraTable(ManoObra.objects.filter(id_estado=estado, id_usuario = request.user), per_page_field=5)
            formulario = AgregaManoObraForm(request.POST or None, request.FILES or None)
            if formulario.is_valid():
                mobra = ManoObra.objects.model(
                    id_usuario = request.user,
                    puesto = formulario.cleaned_data['puesto'],
                    numero_trabajadores = formulario.cleaned_data['numero_trabajadores'],
                    pago_mensual = formulario.cleaned_data['pago_mensual'],
                    pago_anual = formulario.cleaned_data['pago_mensual']*12,
                    prestaciones = formulario.cleaned_data['pago_mensual']*3.6,
                    total_anual = formulario.cleaned_data['pago_mensual']*3.6*formulario.cleaned_data['numero_trabajadores'],
                    id_estado = estado
                )
                mobra.save()
                messages.success(request, "Puesto agregado")
                return HttpResponseRedirect(reverse('estado', args=(estado.id,)))
        else:
            tabla = GrupoTable(Usuarios.objects.filter(), per_page_field=5)
            formulario = AgregaIngresosForm(request.POST or None, request.FILES or None)
    except EstadosFinancieros.DoesNotExist:
        raise Http404("El Estado Financiero no existe")
    context = {'title': estado.nombre_estado,'subtitulo':estado.nombre_estado, 'tabla': tabla, 'form':formulario, 'boton': "Agregar", 'js':js}
    return render(request,'proyecciones/estado.html', context)


def edita_ingreso(request, pk):
    try: 
        print(pk)
        js='/js/EstadosFinancieros/ingresos.js'
        ingreso = Ingresos.objects.get(pk=pk)
        formulario = AgregaIngresosForm(request.POST or None, request.FILES or None, instance=ingreso)
        if formulario.is_valid():
            ingreso_editado = formulario.save()
            ingreso_editado.ingresos = ingreso_editado.unidades * ingreso_editado.precio_unitario
            ingreso_editado.save()
            messages.success(request, " Producto actualizado")
            return HttpResponseRedirect(reverse('estado', args=(ingreso_editado.id_estado.id, )))
    except Ingresos.DoesNotExist:
        raise Http404("Ingresos no existe")   
    context = {'title': 'Edita ingreso','subtitulo':'Edita ingreso',  'form':formulario, 'boton': "Editar", 'js':js}
    return render(request,'proyecciones/edita_estado.html', context)

def elimina_ingreso(request, pk):
    ingreso = get_object_or_404(Ingresos, pk=pk)
    ingreso.delete()
    messages.success(request, " Producto eliminado")
    return HttpResponseRedirect(reverse('estado', args=(ingreso.id_estado.id, )))

def edita_materiales(request, pk):
    try: 
        print(pk)
        js='/js/EstadosFinancieros/materiales.js'
        material = Materiales.objects.get(pk=pk)
        formulario = AgregaMaterialesForm(request.POST or None, request.FILES or None, instance=material)
        if formulario.is_valid():
            material_editado = formulario.save()
            material_editado.costo_anual = material_editado.costo * material_editado.volumen
            material_editado.save()
            messages.success(request, "Material actualizado")
            return HttpResponseRedirect(reverse('estado', args=(material_editado.id_estado.id, )))
    except Materiales.DoesNotExist:
        raise Http404("Materiales no existe")   
    context = {'title': 'Edita material','subtitulo':'Edita material',  'form':formulario, 'boton': "Editar", 'js':js}
    return render(request,'proyecciones/edita_estado.html', context)

def elimina_materiales(request, pk):
    material = get_object_or_404(Materiales, pk=pk)
    material.delete()
    messages.success(request, "Material eliminado")
    return HttpResponseRedirect(reverse('estado', args=(material.id_estado.id, )))

def edita_envase(request, pk):
    try: 
        print(pk)
        js='/js/EstadosFinancieros/materiales.js'
        envase = Envase.objects.get(pk=pk)
        formulario = AgregaEnvaseForm(request.POST or None, request.FILES or None, instance=envase)
        if formulario.is_valid():
            envase_editado = formulario.save()
            envase_editado.costo_anual = envase_editado.costo * envase_editado.necesidad
            envase_editado.save()
            messages.success(request, "Envase actualizado")
            return HttpResponseRedirect(reverse('estado', args=(envase_editado.id_estado.id, )))
    except Envase.DoesNotExist:
        raise Http404("Envases no existe")   
    context = {'title': 'Edita envase','subtitulo':'Edita envase',  'form':formulario, 'boton': "Editar", 'js':js}
    return render(request,'proyecciones/edita_estado.html', context)

def elimina_envase(request, pk):
    envase = get_object_or_404(Envase, pk=pk)
    envase.delete()
    messages.success(request, "Envase eliminado")
    return HttpResponseRedirect(reverse('estado', args=(envase.id_estado.id, )))


def edita_gastoadministracion(request, pk):
    try: 
        print(pk)
        js='/js/EstadosFinancieros/materiales.js'
        gasto = GastoAdministracion.objects.get(pk=pk)
        formulario = AgregaEnvaseForm(request.POST or None, request.FILES or None, instance=gasto)
        if formulario.is_valid():
            gasto_editado = formulario.save()
            gasto_editado.pago_anual = gasto_editado.pago_mensual * 12
            gasto_editado.prestaciones = gasto_editado.pago_mensual * 3.6
            gasto_editado.total_anual = gasto_editado.pago_mensual * 3.6 * gasto_editado.numero_personas
            gasto_editado.save()
            messages.success(request, "Puesto actualizado")
            return HttpResponseRedirect(reverse('estado', args=(gasto_editado.id_estado.id, )))
    except GastoAdministracion.DoesNotExist:
        raise Http404("Gasto de administración no existe")   
    context = {'title': 'Edita gasto de administración','subtitulo':'Edita gasto de administración',  'form':formulario, 'boton': "Editar", 'js':js}
    return render(request,'proyecciones/edita_estado.html', context)

def elimina_gastoadministracion(request, pk):
    gasto = get_object_or_404(GastoAdministracion, pk=pk)
    gasto.delete()
    messages.success(request, "Puesto eliminado")
    return HttpResponseRedirect(reverse('estado', args=(gasto.id_estado.id, )))

def edita_gastoventa(request, pk):
    try: 
        print(pk)
        js='/js/EstadosFinancieros/gastosventa.js'
        gastov = GastoVenta.objects.get(pk=pk)
        formulario = AgregaGastoVentaForm(request.POST or None, request.FILES or None, instance=gastov)
        if formulario.is_valid():
            gastov_editado = formulario.save()
            gastov_editado.gasto_anual = gastov_editado.gasto_unidad * gastov_editado.cantidad
            gastov_editado.save()
            messages.success(request, "Gasto de venta actualizado")
            return HttpResponseRedirect(reverse('estado', args=(gastov_editado.id_estado.id, )))
    except GastoVenta.DoesNotExist:
        raise Http404("Gasto de venta no existe")   
    context = {'title': 'Edita gasto de venta','subtitulo':'Edita gasto de venta',  'form':formulario, 'boton': "Editar", 'js':js}
    return render(request,'proyecciones/edita_estado.html', context)

def elimina_gastoventa(request, pk):
    gastov = get_object_or_404(GastoVenta, pk=pk)
    gastov.delete()
    messages.success(request, "Gasto eliminado")
    return HttpResponseRedirect(reverse('estado', args=(gastov.id_estado.id, )))

def edita_manoobra(request, pk):
    try: 
        print(pk)
        js='/js/EstadosFinancieros/manoobra.js'
        mobra = ManoObra.objects.get(pk=pk)
        formulario = AgregaManoObraForm(request.POST or None, request.FILES or None, instance=mobra)
        if formulario.is_valid():
            mobra_editado = formulario.save()
            mobra_editado.pago_anual = mobra_editado.pago_mensual * 12
            mobra_editado.prestaciones = mobra_editado.pago_mensual * 3.6
            mobra_editado.total_anual = mobra_editado.pago_mensual * 3.6 * mobra_editado.numero_trabajadores
            mobra_editado.save()
            messages.success(request, "Puesto actualizado")
            return HttpResponseRedirect(reverse('estado', args=(mobra_editado.id_estado.id, )))
    except ManoObra.DoesNotExist:
        raise Http404("Mano de Obra no existe")   
    context = {'title': 'Edita Mano de Obra','subtitulo':'Edita Mano de Obra',  'form':formulario, 'boton': "Editar", 'js':js}
    return render(request,'proyecciones/edita_estado.html', context)

def elimina_manoobra(request, pk):
    mobra = get_object_or_404(ManoObra, pk=pk)
    mobra.delete()
    messages.success(request, "Puesto eliminado")
    return HttpResponseRedirect(reverse('estado', args=(mobra.id_estado.id, )))

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
