from cgitb import handler
import json 
from django.urls import reverse
from django.db.models import F
from django.core.serializers.json import DjangoJSONEncoder
from urllib.request import Request
from django.shortcuts import get_object_or_404, render, redirect
from django.http import Http404, HttpResponse, HttpResponseNotFound, HttpResponseRedirect

from .tables import EnvaseTable, GastoAdministracionTable, GastoVentaTable, GrupoTable, IngresosTable, InversionesTable, ManoObraTable, MaterialesTable, RequerimientosTable, GanttTable, RetroalimentacionTable, GrupoAlumnoTable
from .models import Envase, EstadosFinancieros, GastoAdministracion, GastoVenta, Grupos, Ingresos, Inversion, ManoObra, Materiales, Profesor, Usuarios, Estudiante,  EstadosFinancieros
from .forms import AgregaGastoAdministracionForm, AgregaGastoVentaForm, AgregaInversionesForm, AgregaManoObraForm, LoginForm, UsuarioForm, EditaProfesorForm, EditaEstudianteForm, GrupoForm, CreaGrupoForm, AgregaIngresosForm, AgregaMaterialesForm, AgregaEnvaseForm
from .forms import EditaRetroalimentacionForm, EditaObjetivosForm, EditaDisArquitecturaForm, EditaActPruebasForm, EditaActDespliegueForm, EditaDocumentacionForm, AgregaReportarForm
from .forms import AgregaDefinicionForm, AgregaOjetivoForm, AgregaRequerimientoForm, AgregaRetroalimentacionForm, AgregaDisArquitecturaForm, AgregaActPruebasForm, AgregaActDespliegueForm, AgregaDocumentacionForm, AgregaGanttForm, EditaDefinicionForm
from .models import Definicion, Objetivos, Requerimientos, Retroalimentacion, DisArquitectura, ActPruebas, ActDespliegue, Documentacion, Reportar
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db import IntegrityError, transaction
from django.db.models import Q



# Create your views here.


def inicio(request):
    return render(request, 'paginas/inicio.html')
    # registro


def nosotros(request):
    return render(request, 'paginas/nosotros.html')


def busquedarepo(request):
    queryset = request.GET.get("buscar")
    posts = Definicion.objects.filter()
    if(queryset):
        posts = Definicion.objects.filter(
            Q(nombre__icontains = queryset) | 
            Q(descripcion__icontains = queryset)
        ).distinct()
    posts = posts.select_related('id_usuario') 
    posts = posts.select_related('id_grupo')

    context = {'title':'Repositorio', 'posts': posts}
    return render(request, 'plan/busquedarepo.html', context)

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
            num = formulario.cleaned_data['num']
            
            print(str(num))
            if(len(num) == 10):  # si es estudiante
                from .models import Estudiante
                estudiante = Estudiante.objects.create_user(
                    correo=formulario.cleaned_data['correo'],
                    password=formulario.cleaned_data['password2'],
                    nombre=formulario.cleaned_data['nombre'],
                    apellido=formulario.cleaned_data['apellido'],
                    num=formulario.cleaned_data['num'],
                    foto=formulario.cleaned_data['foto'],
                    tipo = '1'
                )
                print(estudiante)
          
            elif(len(num) == 6):  # si es profesor
                from .models import Profesor
                profesor = Profesor.objects.create_user(
                    correo=formulario.cleaned_data['correo'],
                    password=formulario.cleaned_data['password2'],
                    nombre=formulario.cleaned_data['nombre'],
                    apellido=formulario.cleaned_data['apellido'],
                    num=formulario.cleaned_data['num'],
                    foto=formulario.cleaned_data['foto'],
                    tipo = '2'
                )
                print(profesor)
            else:
                print("No es un número de boleta o empleado válido")
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
    return render(request, 'usuarios/llenarformulario.html', {'formulario': formulario, 'subtitulo': "Inicia sesión", 'boton': "Ingresar"})


def cerrar_sesion(request):
    logout(request)
    messages.success(request, "Sesión terminada")
    return redirect('inicio')


def terminos(request):
    return render(request, 'usuarios/terminos.html')

def editar_retro(request, pk):
    retroalimentacion = Retroalimentacion.objects.get(pk=pk)
    print(retroalimentacion)
    formulario = EditaRetroalimentacionForm(request.POST or None, request.FILES or None, instance = retroalimentacion)
    if request.method == 'POST':
        if formulario.is_valid():
            retromodificada = formulario.save()
            print(retroalimentacion)
            retromodificada.save()
            messages.success(request, "Calificación actualizada")
            return redirect('inicio')
    return render(request, 'proyecciones/editar_retro.html', {'form': formulario, 'subtitulo': " ", 'boton': "Editar", 'title':"Editar retroalimentación"}) 

def editar_estadoformula2(request,pk):
    resacti = Objetivos.objects.get(id_usuario = pk)
    formulario = EditaObjetivosForm(request.POST or None, request.FILES or None, instance = resacti)
    if request.method == 'POST':
        if formulario.is_valid():
            resactimodificada = formulario.save()
            #print(retroalimentacion)
            resactimodificada.save()
            messages.success(request, "Información actualizada")
            return redirect('inicio')
    return render(request, 'proyecciones/editar_retro.html', {'form': formulario, 'subtitulo': " ", 'boton': "Editar", 'title':"Editar retroalimentación"}) 

def editar_estadoformula8(request,pk):
    resacti = DisArquitectura.objects.get(id_usuario = pk)
    formulario = EditaDisArquitecturaForm(request.POST or None, request.FILES or None, instance = resacti)
    if request.method == 'POST':
        if formulario.is_valid():
            resactimodificada = formulario.save()
            #print(retroalimentacion)
            resactimodificada.save()
            messages.success(request, "Información actualizada")
            return redirect('inicio')
    return render(request, 'proyecciones/editar_retro.html', {'form': formulario, 'subtitulo': " ", 'boton': "Editar", 'title':"Editar retroalimentación"}) 

def editar_estadoformula10(request,pk):
    resacti = ActPruebas.objects.get(id_usuario = pk)
    formulario = EditaActPruebasForm(request.POST or None, request.FILES or None, instance = resacti)
    if request.method == 'POST':
        if formulario.is_valid():
            resactimodificada = formulario.save()
            #print(retroalimentacion)
            resactimodificada.save()
            messages.success(request, "Información actualizada")
            return redirect('inicio')
    return render(request, 'proyecciones/editar_retro.html', {'form': formulario, 'subtitulo': " ", 'boton': "Editar", 'title':"Editar retroalimentación"}) 

def editar_estadoformula11(request,pk):
    resacti = ActDespliegue.objects.get(id_usuario = pk)
    formulario = EditaActDespliegueForm(request.POST or None, request.FILES or None, instance = resacti)
    if request.method == 'POST':
        if formulario.is_valid():
            resactimodificada = formulario.save()
            #print(retroalimentacion)
            resactimodificada.save()
            messages.success(request, "Información actualizada")
            return redirect('inicio')
    return render(request, 'proyecciones/editar_retro.html', {'form': formulario, 'subtitulo': " ", 'boton': "Editar", 'title':"Editar retroalimentación"}) 


def editar_estadoformula12(request,pk):
    resacti = Documentacion.objects.get(id_usuario = pk)
    formulario = EditaDocumentacionForm(request.POST or None, request.FILES or None, instance = resacti)
    if request.method == 'POST':
        if formulario.is_valid():
            resactimodificada = formulario.save()
            #print(retroalimentacion)
            resactimodificada.save()
            messages.success(request, "Información actualizada")
            return redirect('inicio')
    return render(request, 'proyecciones/editar_retro.html', {'form': formulario, 'subtitulo': " ", 'boton': "Editar", 'title':"Editar retroalimentación"}) 


def editar_estadoformula(request,pk): #pk para id_usuario

    resacti = Definicion.objects.get(id_usuario = pk)
    formulario = EditaDefinicionForm(request.POST or None, request.FILES or None, instance = resacti)
    if request.method == 'POST':
        if formulario.is_valid():
            resactimodificada = formulario.save()
            #print(retroalimentacion)
            resactimodificada.save()
            messages.success(request, "Información actualizada")
            return redirect('inicio')
    return render(request, 'proyecciones/editar_retro.html', {'form': formulario, 'subtitulo': " ", 'boton': "Editar", 'title':"Editar retroalimentación"}) 



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
    elif(tipo == "Estudiante"):
        estudiante = Estudiante.objects.get(id=request.user.id)
        formulario = EditaEstudianteForm(
            request.POST or None, request.FILES or None,
            instance=estudiante
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
        grupo = Grupos.objects.model(
            nombre_grupo = formulario.cleaned_data['nombre_grupo'],
            clave = formulario.cleaned_data['clave'],
            periodo = formulario.cleaned_data['periodo'],
            ciclo = formulario.cleaned_data['ciclo'],
            id_responsable = request.user
        )
        grupo.save()
        messages.success(request, "Grupo agregado")
        return redirect('inicio')
    context = {'formulario': formulario, 'subtitulo': "Crea un grupo", 'boton': "Crear"}
    return render(request, 'usuarios/crea_grupo.html', context=context)


def consulta_temas(request):
    return render(request, 'plan/consulta_temas.html')


def consulta_estados(request):
    #estados = EstadosFinancieros.objects.all()
    return render(request, 'proyecciones/consulta_estados.html'
    #, {'estados': estados}
    )


def consulta_graficas(request):
    js='/js/Graficas/graficas.js'
    ingreso_grafica = (
        Ingresos.objects.filter(id_usuario=request.user).values('producto', 'ingresos')
    )    
    jingreso_grafica = json.dumps(list(ingreso_grafica), cls=DjangoJSONEncoder)
    print(jingreso_grafica)
    context = {'js':js, 'jdumps':jingreso_grafica}
    return render(request, 'graficas/consulta_graficas.html', context=context)


def consulta_graficas_ingresos(request):
    js = '/js/Graficas/graficas.js'
    ingreso_grafica = (
        Ingresos.objects.filter(id_usuario=request.user).annotate(x=F('producto'), y=F('ingresos')).values('x', 'y')
    )
    jingreso_grafica = json.dumps(list(ingreso_grafica), cls=DjangoJSONEncoder)
    print(jingreso_grafica)
    context = {
        'barratituloGrafica':'Gráficas de Presupuestos de ingresos',
        'tituloGrafica':'"Ingresos"',
        'js': js,
        'jdumps': jingreso_grafica
    }
    return render(request, 'graficas/consulta_graficas.html', context=context)

def consulta_graficas_Materiales(request):
    js = '/js/Graficas/graficas.js'
    Materiales_grafica = (
        Materiales.objects.filter(id_usuario=request.user).annotate(x=F('material'), y=F('costo_anual')).values('x', 'y')
    )
    jMateriales_grafica = json.dumps(list(Materiales_grafica), cls=DjangoJSONEncoder)
    print(jMateriales_grafica)
    context = {
        'barratituloGrafica':'Gráficas de Presupuesto de material',
        'tituloGrafica':'"Materiales"',
        'js': js,
        'jdumps': jMateriales_grafica
    }
    return render(request, 'graficas/consulta_graficas.html', context=context)

def consulta_graficas_Envase(request):
    js = '/js/Graficas/graficas.js'
    Envase_grafica = (
        Envase.objects.filter(id_usuario=request.user).annotate(x=F('tipo_envase'), y=F('costo_anual')).values('x', 'y')
    )
    jEnvase_grafica = json.dumps(list(Envase_grafica), cls=DjangoJSONEncoder)
    print(jEnvase_grafica)
    context = {
        'barratituloGrafica':'Gráficas de Presupuesto de envase',
        'tituloGrafica':'"Envases"',
        'js': js,
        'jdumps': jEnvase_grafica
    }
    return render(request, 'graficas/consulta_graficas.html', context=context)

def consulta_graficas_GastosAdministracion(request):
    js = '/js/Graficas/graficas.js'
    GastosAdministracion_grafica = (
        GastoAdministracion.objects.filter(id_usuario=request.user).annotate(x=F('puesto'), y=F('total_anual')).values('x', 'y')
    )
    jGastoAdmin_grafica = json.dumps(list(GastosAdministracion_grafica), cls=DjangoJSONEncoder)
    print(jGastoAdmin_grafica)
    context = {
        'barratituloGrafica':'Gráficas de Presupuesto de gastos de administración y ventas',
        'tituloGrafica':'"Gastos administración"',
        'js': js,
        'jdumps': jGastoAdmin_grafica
    }
    return render(request, 'graficas/consulta_graficas.html', context=context)

def consulta_graficas_GastosVenta(request):
    js = '/js/Graficas/graficas.js'
    GastosVenta_grafica = (
        GastoVenta.objects.filter(id_usuario=request.user).annotate(x=F('gasto_venta'), y=F('gasto_anual')).values('x', 'y')
    )
    jGastoVenta_grafica = json.dumps(list(GastosVenta_grafica), cls=DjangoJSONEncoder)
    print(jGastoVenta_grafica)
    context = {
        'barratituloGrafica':'Gráficas de Presupuesto de gastos de ventas',
        'tituloGrafica':'"Gastos de ventas"',
        'js': js,
        'jdumps': jGastoVenta_grafica
    }
    return render(request, 'graficas/consulta_graficas.html', context=context)


def consulta_graficas_ManoObra(request):
    js = '/js/Graficas/graficas.js'
    ManoObra_grafica = (
        ManoObra.objects.filter(id_usuario=request.user).annotate(x=F('puesto'), y=F('total_anual')).values('x', 'y')
    )
    jManoObra_grafica = json.dumps(list(ManoObra_grafica), cls=DjangoJSONEncoder)
    print(jManoObra_grafica)
    context = {
        'barratituloGrafica':'Gráficas de Presupuesto de mano de obra',
        'tituloGrafica':'"Mano de obra"',
        'js': js,
        'jdumps': jManoObra_grafica
    }
    return render(request, 'graficas/consulta_graficas.html', context=context)

def consulta_escenarios(request):
    return render(request, 'simulador/consulta_escenarios.html')


def genera_prediccion(request):
    return render(request, 'predicciones/genera_prediccion.html')

def consulta_portafolio(request, pk):
    alumno = Usuarios.objects.get(pk=pk)
    from .models import Reportar
    if Reportar.objects.filter(id_usuario=alumno.id).exists():
        retroactual = Reportar.objects.get(id_usuario= alumno.id)
        formulario = '0'
    else:
        retroactual = '1'
        formulario = AgregaReportarForm(request.POST or None, request.FILES or None)
        if formulario.is_valid():
                from .models import Reportar
                repo = Reportar.objects.model(
                    id_usuario = alumno,
                    motivo = formulario.cleaned_data['motivo']
                )
                repo.save()
                messages.success(request, "Portafolio reportado")
                #return HttpResponseRedirect(reverse('consulta_portafolio', args=(alumno.id)))

    context = {'title':'Portafolio de evidencias', 'alumno': alumno, 'retroactual':retroactual, 'form':formulario}
    return render(request,'plan/consulta_portafolio.html', context)

def ver_grupo(request, id_grupo):
    try:
        grupo = Grupos.objects.get(pk=id_grupo)
        if(request.user.tipo == '2'):
            tabla = RetroalimentacionTable(Usuarios.objects.filter(id_grupo=id_grupo), per_page_field=5)
        else: 
            tabla = GrupoAlumnoTable(Usuarios.objects.filter(id_grupo=id_grupo), per_page_field=5)
    except Grupos.DoesNotExist:
        raise Http404("El grupo no existe")
    context = {'title': "Ver grupo",'subtitulo':grupo.nombre_grupo, 'tabla': tabla}
    return render(request,'usuarios/tabla_generica.html', context)

def estadoformulaprofe(request, pk, usu):
    estado = EstadosFinancieros.objects.get(pk=pk)
    alumno = Usuarios.objects.get(pk=usu)
    print('Alumno: ' + str(alumno.id) + str(alumno.nombre) + str(alumno.apellido))
    if(pk=='1'):
        actividad = '1'
        from .models import Definicion, Retroalimentacion
        if Definicion.objects.filter(id_usuario= alumno.id).exists():
            definicion = Definicion.objects.get(id_usuario= alumno.id)
        else:
            definicion = '0'
        if Retroalimentacion.objects.filter(id_usuario= alumno.id, id_estado = estado.id).exists():
            retroactual = Retroalimentacion.objects.get(id_usuario= alumno.id, id_estado = estado.id)
            formulario = '2'
        else: #si no existe se agrega
            retroactual = '1'
            formulario = AgregaRetroalimentacionForm(request.POST or None, request.FILES or None)
            if formulario.is_valid():
                from .models import Retroalimentacion
                retroalimentacion = Retroalimentacion.objects.model(
                    id_usuario = alumno,
                    calificacion = formulario.cleaned_data['calificacion'],
                    comentario = formulario.cleaned_data['comentario'],
                    id_estado = estado
                )
                retroalimentacion.save()
                messages.success(request, "Retroalimentación agregada")
                return HttpResponseRedirect(reverse('estadoformulaprofe', args=(estado.id,alumno.id)))
    if(pk=='2'):
        actividad = '2'
        from .models import Objetivos, Retroalimentacion
        if Objetivos.objects.filter(id_usuario= alumno.id).exists():
            definicion = Objetivos.objects.get(id_usuario= alumno.id)
        else:
            definicion = '0'
        if Retroalimentacion.objects.filter(id_usuario= alumno.id, id_estado = estado.id).exists():
            retroactual = Retroalimentacion.objects.get(id_usuario= alumno.id, id_estado = estado.id)
            formulario = '2'
        else:
            retroactual = '1'
            formulario = AgregaRetroalimentacionForm(request.POST or None, request.FILES or None)
            if formulario.is_valid():
                from .models import Retroalimentacion
                retroalimentacion = Retroalimentacion.objects.model(
                    id_usuario = alumno,
                    calificacion = formulario.cleaned_data['calificacion'],
                    comentario = formulario.cleaned_data['comentario'],
                    id_estado = estado
                )
                retroalimentacion.save()
                messages.success(request, "Retroalimentación agregada")
                return HttpResponseRedirect(reverse('estadoformulaprofe', args=(estado.id,alumno.id)))
    if(pk=='8'):
        actividad = '8'
        from .models import DisArquitectura, Retroalimentacion
        if DisArquitectura.objects.filter(id_usuario= alumno.id).exists():
            definicion = DisArquitectura.objects.get(id_usuario= alumno.id)
        else:
            definicion = '0'
        if Retroalimentacion.objects.filter(id_usuario= alumno.id, id_estado = estado.id).exists():
            retroactual = Retroalimentacion.objects.get(id_usuario= alumno.id, id_estado = estado.id)
            formulario = '2'
        else:
            retroactual = '1'
            formulario = AgregaRetroalimentacionForm(request.POST or None, request.FILES or None)
            if formulario.is_valid():
                from .models import Retroalimentacion
                retroalimentacion = Retroalimentacion.objects.model(
                    id_usuario = alumno,
                    calificacion = formulario.cleaned_data['calificacion'],
                    comentario = formulario.cleaned_data['comentario'],
                    id_estado = estado
                )
                retroalimentacion.save()
                messages.success(request, "Retroalimentación agregada")
                return HttpResponseRedirect(reverse('estadoformulaprofe', args=(estado.id,alumno.id)))

    if(pk=='10'):
        actividad = '10'
        from .models import ActPruebas, Retroalimentacion
        if ActPruebas.objects.filter(id_usuario= alumno.id).exists():
            definicion = ActPruebas.objects.get(id_usuario= alumno.id)
        else:
            definicion = '0'
        if Retroalimentacion.objects.filter(id_usuario= alumno.id, id_estado = estado.id).exists():
            retroactual = Retroalimentacion.objects.get(id_usuario= alumno.id, id_estado = estado.id)
            formulario = '2'
        else:
            retroactual = '1'
            formulario = AgregaRetroalimentacionForm(request.POST or None, request.FILES or None)
            if formulario.is_valid():
                from .models import Retroalimentacion
                retroalimentacion = Retroalimentacion.objects.model(
                    id_usuario = alumno,
                    calificacion = formulario.cleaned_data['calificacion'],
                    comentario = formulario.cleaned_data['comentario'],
                    id_estado = estado
                )
                retroalimentacion.save()
                messages.success(request, "Retroalimentación agregada")
                return HttpResponseRedirect(reverse('estadoformulaprofe', args=(estado.id,alumno.id)))

    if(pk=='11'):
        actividad = '11'
        from .models import ActDespliegue, Retroalimentacion
        if ActDespliegue.objects.filter(id_usuario= alumno.id).exists():
            definicion = ActDespliegue.objects.get(id_usuario= alumno.id)
        else:
            definicion = '0'
        if Retroalimentacion.objects.filter(id_usuario= alumno.id, id_estado = estado.id).exists():
            retroactual = Retroalimentacion.objects.get(id_usuario= alumno.id, id_estado = estado.id)
            formulario = '2'
        else:
            retroactual = '1'
            formulario = AgregaRetroalimentacionForm(request.POST or None, request.FILES or None)
            if formulario.is_valid():
                from .models import Retroalimentacion
                retroalimentacion = Retroalimentacion.objects.model(
                    id_usuario = alumno,
                    calificacion = formulario.cleaned_data['calificacion'],
                    comentario = formulario.cleaned_data['comentario'],
                    id_estado = estado
                )
                retroalimentacion.save()
                messages.success(request, "Retroalimentación agregada")
                return HttpResponseRedirect(reverse('estadoformulaprofe', args=(estado.id,alumno.id)))
    if(pk=='12'):
        actividad = '12'
        from .models import Documentacion, Retroalimentacion
        if Documentacion.objects.filter(id_usuario= alumno.id).exists():
            definicion = Documentacion.objects.get(id_usuario= alumno.id)
        else:
            definicion = '0'
        if Retroalimentacion.objects.filter(id_usuario= alumno.id, id_estado = estado.id).exists():
            retroactual = Retroalimentacion.objects.get(id_usuario= alumno.id, id_estado = estado.id)
            formulario = '2'
        else:
            retroactual = '1'
            formulario = AgregaRetroalimentacionForm(request.POST or None, request.FILES or None)
            if formulario.is_valid():
                from .models import Retroalimentacion
                retroalimentacion = Retroalimentacion.objects.model(
                    id_usuario = alumno,
                    calificacion = formulario.cleaned_data['calificacion'],
                    comentario = formulario.cleaned_data['comentario'],
                    id_estado = estado
                )
                retroalimentacion.save()
                messages.success(request, "Retroalimentación agregada")
                return HttpResponseRedirect(reverse('estadoformulaprofe', args=(estado.id,alumno.id)))
    print('actividad = ' + actividad)
    context =  context = {'title': estado.nombre_estado, 'actividad': actividad, 'definicion':definicion, 'subtitulo':estado.nombre_estado, 'form': formulario, 'boton': "Evaluar", 'retroactual': retroactual}
    return render(request, 'proyecciones/estadoformulaprofe.html', context)



def estadotabla(request, pk):
    try:
        estado = EstadosFinancieros.objects.get(pk=pk)
        if(pk=='7'):
            from .models import Requerimientos
            formulario = AgregaRequerimientoForm(request.POST or None, request.FILES or None)
            tabla = RequerimientosTable(Requerimientos.objects.filter(id_estado=estado, id_usuario = request.user),per_page_field=5)
            if formulario.is_valid():
                requerimiento = Requerimientos.objects.model(
                   id_usuario = request.user,
                   numero = formulario.cleaned_data['numero'],
                   tipo_requerimiento = formulario.cleaned_data['tipo_requerimiento'],
                   Requerimiento = formulario.cleaned_data['Requerimiento'],
                   id_estado = estado
                )
                requerimiento.save()
                messages.success(request, "Requerimientos agregados")
                return HttpResponseRedirect(reverse('estadotabla', args=(estado.id,)))
        elif (pk=='9'):
            from .models import Gantt
            formulario = AgregaGanttForm(request.POST or None, request.FILES or None)
            tabla = GanttTable(Gantt.objects.filter(id_estado=estado, id_usuario = request.user),per_page_field=5)
            if formulario.is_valid():
                gantt = Gantt.objects.model(
                   id_usuario = request.user,
                   fase = formulario.cleaned_data['fase'],
                   numtarea = formulario.cleaned_data['numtarea'],
                   asignado = formulario.cleaned_data['asignado'],
                   estado = formulario.cleaned_data['estado'],
                   fechaini = formulario.cleaned_data['fechaini'],
                   fechafin = formulario.cleaned_data['fechafin'],
                   notas = formulario.cleaned_data['notas'],
                   predecesora = formulario.cleaned_data['predecesora'],
                   id_estado = estado
                )
                gantt.save()
                messages.success(request, "Actividades para la programación agregadas")
                return HttpResponseRedirect(reverse('estadotabla', args=(estado.id,)))
    except EstadosFinancieros.DoesNotExist:
        raise Http404("El Estado Financiero no existe")
    context = {'title': estado.nombre_estado,'subtitulo':estado.nombre_estado, 'tabla': tabla, 'form':formulario, 'boton': "Entregar"}
    return render(request,'proyecciones/estadotabla.html', context)


def estadoformula(request, pk):
    try:
        estado = EstadosFinancieros.objects.get(pk=pk)
        if(pk=='1'):
            print('info del request: ' + str(request.user) )
            print('id_grupo: ' + str(request.user.id_grupo) )
            actividad = '1'
            from .models import Definicion, Retroalimentacion
            if Retroalimentacion.objects.filter(id_usuario= request.user.id, id_estado = estado.id).exists():
                retroactual = Retroalimentacion.objects.get(id_usuario= request.user.id, id_estado = estado.id)
            else:
                retroactual = '0'
            if Definicion.objects.filter(id_usuario= request.user.id).exists():
                definicion = Definicion.objects.get(id_usuario= request.user.id)
                formulario = '0' #no se muestra el formulario
            else: 
                definicion = '0' #no existe definición
                formulario = AgregaDefinicionForm(request.POST or None, request.FILES or None)
                if formulario.is_valid():
                    from .models import Definicion
                    definicion = Definicion.objects.model(
                    id_usuario = request.user,
                    nombre = formulario.cleaned_data['nombre'],
                    tipo = formulario.cleaned_data['tipo'],
                    descripcion = formulario.cleaned_data['descripcion'],
                    clasificacion = formulario.cleaned_data['clasificacion'],
                    id_grupo = request.user.id_grupo,
                    id_estado = estado
                    )
                    definicion.save()
                    messages.success(request, "Definición del negocio agregada")
                    return HttpResponseRedirect(reverse('estadoformula', args=(estado.id,)))
        elif (pk=='2'):
            actividad = '2'
            from .models import Objetivos, Retroalimentacion
            if Retroalimentacion.objects.filter(id_usuario= request.user.id, id_estado = estado.id).exists():
                retroactual = Retroalimentacion.objects.get(id_usuario= request.user.id, id_estado = estado.id)
            else:
                retroactual = '0'
            if Objetivos.objects.filter(id_usuario= request.user.id).exists():
                definicion = Objetivos.objects.get(id_usuario= request.user.id)
                formulario = '0' #no se muestra el formulario
            else:
                definicion = '0'
                formulario = AgregaOjetivoForm(request.POST or None, request.FILES or None)
                if formulario.is_valid():  
                    definicion = Objetivos.objects.model(
                    id_usuario = request.user,
                    mision = formulario.cleaned_data['mision'],
                    vision = formulario.cleaned_data['vision'],
                    objgeneral = formulario.cleaned_data['objgeneral'],
                    objespecificos = formulario.cleaned_data['objespecificos'],
                    id_estado = estado
                    )
                    definicion.save()
                    messages.success(request, "Misión, Visión u Objetivos agregados")
                    return HttpResponseRedirect(reverse('estadoformula', args=(estado.id,)))

        elif (pk=='8'):
            actividad = '8'
            from .models import DisArquitectura, Retroalimentacion
            if Retroalimentacion.objects.filter(id_usuario= request.user.id, id_estado = estado.id).exists():
                retroactual = Retroalimentacion.objects.get(id_usuario= request.user.id, id_estado = estado.id)
            else:
                retroactual = '0'
            if DisArquitectura.objects.filter(id_usuario= request.user.id).exists():
                definicion = DisArquitectura.objects.get(id_usuario= request.user.id)
                formulario = '0' #no se muestra el formulario
            else: 
                definicion = '0' #no existe definición
                formulario = AgregaDisArquitecturaForm(request.POST or None, request.FILES or None)
                if formulario.is_valid():
                    definicion = DisArquitectura.objects.model(
                    id_usuario = request.user,
                    archivo = formulario.cleaned_data['archivo'],
                    id_estado = estado
                    )
                    definicion.save()
                    messages.success(request, "Archivo del Diseño de la arquitectura agregado")
                    return HttpResponseRedirect(reverse('estadoformula', args=(estado.id,)))
        elif (pk=='10'):
            actividad = '10'
            from .models import ActPruebas, Retroalimentacion
            if Retroalimentacion.objects.filter(id_usuario= request.user.id, id_estado = estado.id).exists():
                retroactual = Retroalimentacion.objects.get(id_usuario= request.user.id, id_estado = estado.id)
            else:
                retroactual = '0'
            if ActPruebas.objects.filter(id_usuario= request.user.id).exists():
                definicion = ActPruebas.objects.get(id_usuario= request.user.id)
                formulario = '0' #no se muestra el formulario
            else: 
                definicion = '0' #no existe definición
                formulario = AgregaActPruebasForm(request.POST or None, request.FILES or None)
                if formulario.is_valid():
                    definicion = ActPruebas.objects.model(
                    id_usuario = request.user,
                    archivo = formulario.cleaned_data['archivo'],
                    id_estado = estado
                    )
                    definicion.save()
                    messages.success(request, "Archivo de las actividades para la programación agregado")
                    return HttpResponseRedirect(reverse('estadoformula', args=(estado.id,)))
        elif (pk=='11'):
            actividad = '11'
            from .models import ActDespliegue, Retroalimentacion
            if Retroalimentacion.objects.filter(id_usuario= request.user.id, id_estado = estado.id).exists():
                retroactual = Retroalimentacion.objects.get(id_usuario= request.user.id, id_estado = estado.id)
            else:
                retroactual = '0'
            if ActDespliegue.objects.filter(id_usuario= request.user.id).exists():
                definicion = ActDespliegue.objects.get(id_usuario= request.user.id)
                formulario = '0' #no se muestra el formulario
            else: 
                definicion = '0' #no existe definición
                formulario = AgregaActDespliegueForm(request.POST or None, request.FILES or None)
                if formulario.is_valid():
                    definicion = ActDespliegue.objects.model(
                    id_usuario = request.user,
                    archivo = formulario.cleaned_data['archivo'],
                    id_estado = estado
                    )
                    definicion.save()
                    messages.success(request, "Archivo de las actividades para las pruebas e implementación agregado")
                    return HttpResponseRedirect(reverse('estadoformula', args=(estado.id,)))
        elif (pk=='12'):
            actividad = '12'
            from .models import Documentacion, Retroalimentacion
            if Retroalimentacion.objects.filter(id_usuario= request.user.id, id_estado = estado.id).exists():
                retroactual = Retroalimentacion.objects.get(id_usuario= request.user.id, id_estado = estado.id)
            else:
                retroactual = '0'
            if Documentacion.objects.filter(id_usuario= request.user.id).exists():
                definicion = Documentacion.objects.get(id_usuario= request.user.id)
                formulario = '0' #no se muestra el formulario
            else: 
                definicion = '0' #no existe definición
                formulario = AgregaDocumentacionForm(request.POST or None, request.FILES or None)
                if formulario.is_valid():
                    from .models import Documentacion
                    definicion = Documentacion.objects.model(
                    id_usuario = request.user,
                    archivo = formulario.cleaned_data['archivo'],
                    id_estado = estado
                    )
                    definicion.save()
                    messages.success(request, "Archivo de las actividades para las pruebas e implementación agregado")
                    return HttpResponseRedirect(reverse('estadoformula', args=(estado.id,)))

    except EstadosFinancieros.DoesNotExist:
        raise Http404("El Estado Financiero no existe") 
    context = {'title': estado.nombre_estado,'subtitulo':estado.nombre_estado,  'form':formulario, 'boton': "Entregar", 'retroactual':retroactual, 'definicion':definicion, 'actividad':actividad}
    return render(request,'proyecciones/estadoformula.html', context)

##Los de las TABLAS
def estado(request, pk):
    try:
        estado = EstadosFinancieros.objects.get(pk=pk)
        if(pk=='6'): #Financiamiento fase 2
            js='/js/EstadosFinancieros/inversiones.js'
            from .models import Inversion, Retroalimentacion
            if Retroalimentacion.objects.filter(id_usuario= request.user.id, id_estado = estado.id).exists():
                retroactual = Retroalimentacion.objects.get(id_usuario= request.user.id, id_estado = estado.id)
            else:
                retroactual = '0'
            tabla = InversionesTable(Inversion.objects.filter(id_estado=estado, id_usuario = request.user), per_page_field=5)
            formulario = AgregaInversionesForm(request.POST or None, request.FILES or None)
            if formulario.is_valid():
                inversion = Inversion.objects.model(
                    id_usuario = request.user,
                    tipo_inversion = formulario.cleaned_data['tipo_inversion'],
                    socios = formulario.cleaned_data['socios'],
                    bancos = formulario.cleaned_data['bancos'],
                    gobiernof = formulario.cleaned_data['gobiernof'],
                    gobiernoe = formulario.cleaned_data['gobiernoe'],
                    otras = formulario.cleaned_data['otras'],
                    total = formulario.cleaned_data['socios']+formulario.cleaned_data['bancos']+formulario.cleaned_data['gobiernof']+formulario.cleaned_data['gobiernoe']+formulario.cleaned_data['otras'],
                    id_estado = estado
                )
                inversion.save()
                messages.success(request, "Inversión agregada")
                return HttpResponseRedirect(reverse('estado', args=(estado.id,)))
        elif(pk=='15'): #Ingresos fase 4
            js='/js/EstadosFinancieros/ingresos.js'
            from .models import Ingresos, Retroalimentacion
            if Retroalimentacion.objects.filter(id_usuario= request.user.id, id_estado = estado.id).exists():
                retroactual = Retroalimentacion.objects.get(id_usuario= request.user.id, id_estado = estado.id)
            else:
                retroactual = '0'
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
        elif(pk == '3'): #Caracteristicas del producto fase 1
            js='/js/EstadosFinancieros/materiales.js'
            from .models import Materiales, Retroalimentacion
            if Retroalimentacion.objects.filter(id_usuario= request.user.id, id_estado = estado.id).exists():
                retroactual = Retroalimentacion.objects.get(id_usuario= request.user.id, id_estado = estado.id)
            else:
                retroactual = '0'
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
        
        elif(pk == '5'):
            js='/js/EstadosFinancieros/gastosventa.js'
            from .models import GastoVenta, Retroalimentacion
            if Retroalimentacion.objects.filter(id_usuario= request.user.id, id_estado = estado.id).exists():
                retroactual = Retroalimentacion.objects.get(id_usuario= request.user.id, id_estado = estado.id)
            else:
                retroactual = '0'
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
                messages.success(request, "Inversión necesaria agregada")
                return HttpResponseRedirect(reverse('estado', args=(estado.id,)))
        elif(pk == '4'): # presupuesto de mano de obra fase 1
            js='/js/EstadosFinancieros/manoobra.js'
            from .models import ManoObra, Retroalimentacion
            if Retroalimentacion.objects.filter(id_usuario= request.user.id, id_estado = estado.id).exists():
                retroactual = Retroalimentacion.objects.get(id_usuario= request.user.id, id_estado = estado.id)
            else:
                retroactual = '0'
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

    except EstadosFinancieros.DoesNotExist:
        raise Http404("El Estado Financiero no existe")
    context = {'title': estado.nombre_estado,'subtitulo':estado.nombre_estado, 'tabla': tabla, 'form':formulario, 'boton': "Entregar", 'js':js, 'retroactual':retroactual}
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

def edita_inversion(request, pk):
    try: 
        print(pk)
        js='/js/EstadosFinancieros/inversiones.js'
        inversion = Inversion.objects.get(pk=pk)
        formulario = AgregaInversionesForm(request.POST or None, request.FILES or None, instance=inversion)
        if formulario.is_valid():
            inversion_editado = formulario.save()
            inversion_editado.total = inversion_editado.socios + inversion_editado.bancos +  inversion_editado.gobiernof + inversion_editado.gobiernoe +  inversion_editado.otras
            inversion_editado.save()
            messages.success(request, "Inversion actualizada")
            return HttpResponseRedirect(reverse('estado', args=(inversion_editado.id_estado.id, )))
    except Inversion.DoesNotExist:
        raise Http404("Inversion no existe")   
    context = {'title': 'Edita Inversión','subtitulo':'Edita inversión',  'form':formulario, 'boton': "Editar", 'js':js}
    return render(request,'proyecciones/edita_estado.html', context)

def elimina_inversion(request, pk):
    inversion = get_object_or_404(Inversion, pk=pk)
    inversion.delete()
    messages.success(request, "Inversión eliminada")
    return HttpResponseRedirect(reverse('estado', args=(inversion.id_estado.id, )))



def edita_requerimiento(request, pk):
    try: 
        print(pk)
        requer = Requerimientos.objects.get(pk=pk)
        formulario = AgregaRequerimientoForm(request.POST or None, request.FILES or None, instance=requer)
        if formulario.is_valid():
            requer_editado = formulario.save()
            requer_editado.save()
            messages.success(request, "Envase actualizado")
            return HttpResponseRedirect(reverse('estado', args=(requer_editado.id_estado.id, )))
    except Envase.DoesNotExist:
        raise Http404("Envases no existe")   
    context = {'title': 'Edita envase','subtitulo':'Edita envase',  'form':formulario, 'boton': "Editar"}
    return render(request,'proyecciones/edita_estado.html', context)

def elimina_requerimiento(request, pk):
    requer = get_object_or_404(Requerimientos, pk=pk)
    requer.delete()
    messages.success(request, "Requerimiento eliminado")
    return HttpResponseRedirect(reverse('estadoformula', args=(requer.id_estado.id, )))



def estadoprofe(request, pk, usu):
    try:
        estado = EstadosFinancieros.objects.get(pk=pk)
        alumno = Usuarios.objects.get(pk = usu)
        if(pk=='6'): #Financiamiento fase 2
            js='/js/EstadosFinancieros/inversiones.js'
            from .models import Inversion, Retroalimentacion
            tabla = InversionesTable(Inversion.objects.filter(id_estado=estado, id_usuario = alumno.id), per_page_field=5)
            if Retroalimentacion.objects.filter(id_usuario= alumno.id, id_estado = estado.id).exists():
                retroactual = Retroalimentacion.objects.get(id_usuario= alumno.id, id_estado = estado.id)
                formulario = '2'
            else:
                retroactual = '1'
                formulario = AgregaRetroalimentacionForm(request.POST or None, request.FILES or None)
                if formulario.is_valid():
                    from .models import Retroalimentacion
                    retroalimentacion = Retroalimentacion.objects.model(
                        id_usuario = alumno,
                        calificacion = formulario.cleaned_data['calificacion'],
                        comentario = formulario.cleaned_data['comentario'],
                        id_estado = estado
                    )
                    retroalimentacion.save()
                    messages.success(request, "Retralimentación agregada")
                    return HttpResponseRedirect(reverse('estadoprofe', args=(estado.id, alumno.id)))
        elif(pk=='15'): #Ingresos fase 4
            js='/js/EstadosFinancieros/ingresos.js'
            from .models import Ingresos, Retroalimentacion
            tabla = IngresosTable(Ingresos.objects.filter(id_estado=estado, id_usuario = alumno.id), per_page_field=5)
            if Retroalimentacion.objects.filter(id_usuario= alumno.id, id_estado = estado.id).exists():
                retroactual = Retroalimentacion.objects.get(id_usuario= alumno.id, id_estado = estado.id)
                formulario = '2'
            else:
                retroactual = '1'
                formulario = AgregaRetroalimentacionForm(request.POST or None, request.FILES or None)
                if formulario.is_valid():
                    from .models import Retroalimentacion
                    retroalimentacion = Retroalimentacion.objects.model(
                        id_usuario = alumno,
                        calificacion = formulario.cleaned_data['calificacion'],
                        comentario = formulario.cleaned_data['comentario'],
                        id_estado = estado
                    )
                    retroalimentacion.save()
                    messages.success(request, "Retralimentación agregada")
                    return HttpResponseRedirect(reverse('estadoprofe', args=(estado.id,alumno.id)))
        elif(pk == '3'): #Caracteristicas del producto fase 1
            js='/js/EstadosFinancieros/materiales.js'
            from .models import Materiales, Retroalimentacion
            tabla = MaterialesTable(Materiales.objects.filter(id_estado=estado, id_usuario = alumno.id), per_page_field=5)
            if Retroalimentacion.objects.filter(id_usuario= alumno.id, id_estado = estado.id).exists():
                retroactual = Retroalimentacion.objects.get(id_usuario= alumno.id, id_estado = estado.id)
                formulario = '2'
            else:
                retroactual = '1'
                formulario = AgregaRetroalimentacionForm(request.POST or None, request.FILES or None)
                if formulario.is_valid():
                    from .models import Retroalimentacion
                    retroalimentacion = Retroalimentacion.objects.model(
                        id_usuario = alumno,
                        calificacion = formulario.cleaned_data['calificacion'],
                        comentario = formulario.cleaned_data['comentario'],
                        id_estado = estado
                    )
                    retroalimentacion.save()
                    messages.success(request, "Retralimentación agregada")
                    return HttpResponseRedirect(reverse('estadoprofe', args=(estado.id,alumno.id)))
        
        elif(pk == '5'): #Inversión necesaria fase 2
            js='/js/EstadosFinancieros/gastosventa.js'
            from .models import GastoVenta, Retroalimentacion
            tabla = GastoVentaTable(GastoVenta.objects.filter(id_estado=estado, id_usuario = alumno.id), per_page_field=5)
            if Retroalimentacion.objects.filter(id_usuario= alumno.id, id_estado = estado.id).exists():
                retroactual = Retroalimentacion.objects.get(id_usuario= alumno.id, id_estado = estado.id)
                formulario = '2'
            else:
                retroactual = '1'
                formulario = AgregaRetroalimentacionForm(request.POST or None, request.FILES or None)
                if formulario.is_valid():
                    from .models import Retroalimentacion
                    retroalimentacion = Retroalimentacion.objects.model(
                        id_usuario = alumno,
                        calificacion = formulario.cleaned_data['calificacion'],
                        comentario = formulario.cleaned_data['comentario'],
                        id_estado = estado
                    )
                    retroalimentacion.save()
                    messages.success(request, "Retroalimentación agregada")
                    return HttpResponseRedirect(reverse('estadoprofe', args=(estado.id,alumno.id)))
        elif(pk == '4'): # presupuesto de mano de obra fase 1
            js='/js/EstadosFinancieros/manoobra.js'
            from .models import ManoObra, Retroalimentacion
            tabla = ManoObraTable(ManoObra.objects.filter(id_estado=estado, id_usuario = alumno.id), per_page_field=5)
            if Retroalimentacion.objects.filter(id_usuario= alumno.id, id_estado = estado.id).exists():
                retroactual = Retroalimentacion.objects.get(id_usuario= alumno.id, id_estado = estado.id)
                formulario = '2'
            else:
                retroactual = '1'
                formulario = AgregaRetroalimentacionForm(request.POST or None, request.FILES or None)
                if formulario.is_valid():
                    from .models import Retroalimentacion
                    retroalimentacion = Retroalimentacion.objects.model(
                        id_usuario = alumno,
                        calificacion = formulario.cleaned_data['calificacion'],
                        comentario = formulario.cleaned_data['comentario'],
                        id_estado = estado
                    )
                    retroalimentacion.save()
                    messages.success(request, "Retroalimentación agregada")
                    return HttpResponseRedirect(reverse('estadoprofe', args=(estado.id,alumno.id)))

    except EstadosFinancieros.DoesNotExist:
        raise Http404("El Estado Financiero no existe")
    context = {'title': estado.nombre_estado,'subtitulo':estado.nombre_estado, 'tabla': tabla, 'form':formulario, 'boton': "Entregar", 'js':js, 'retroactual': retroactual}
    return render(request,'proyecciones/estadoprofe.html', context)
