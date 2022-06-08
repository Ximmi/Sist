from django.urls import path
from . import views

from django.conf import settings
from django.contrib.staticfiles.urls import static
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('nosotros', views.nosotros, name='nosotros'),
    path('contacto', views.contacto, name='contacto'),
    path('registro', views.registro, name='registro'),
    path('terminos', views.terminos, name='terminos'),
    path('politicas', views.politicas, name='politicas'),
    path('productos', views.productos, name='productos'),
    path('inicio_sesion', views.inicio_sesion, name='inicio_sesion'),
    path('cerrar_sesion', views.cerrar_sesion, name='cerrar_sesion'),
    path('editar_perfil', views.editar_perfil, name='editar_perfil'),
     path('cambiar_contraseña', auth_views.PasswordChangeView.as_view(
        template_name='usuarios/editar_perfil.html',
        success_url='/'), name='userChangePassword'),
    path('consulta_grupo', views.consulta_grupo, name='consulta_grupo'),
    path('crea_grupo', views.crea_grupo, name='crea_grupo'),
    path('consulta_temas', views.consulta_temas, name='consulta_temas'),
    path('consulta_estados', views.consulta_estados, name='consulta_estados'),
    path('consulta_graficas', views.consulta_graficas, name='consulta_graficas'),
    path('consulta_escenarios', views.consulta_escenarios, name='consulta_escenarios'),
    path('genera_prediccion', views.genera_prediccion, name='genera_prediccion'),
    path('consulta_planes/<pk>/', views.consulta_planes, name='consulta_planes'),
    path('ver_grupo/<id_grupo>/', views.ver_grupo, name='ver_grupo'),
    path('estado/<pk>/', views.estado, name='estado'),
    path('edita_ingreso/<pk>/', views.edita_ingreso, name='edita_ingreso'),
    path('elimina_ingreso/<pk>/', views.elimina_ingreso, name='elimina_ingreso'),
    path('edita_materiales/<pk>/', views.edita_materiales, name='edita_materiales'),
    path('elimina_materiales/<pk>/', views.elimina_materiales, name='elimina_materiales'),
    path('edita_envase/<pk>/', views.edita_envase, name='edita_envase'),
    path('elimina_envase/<pk>/', views.elimina_envase, name='elimina_envase'),
    path('edita_gastoadministracion/<pk>/', views.edita_gastoadministracion, name='edita_gastoadministracion'),
    path('elimina_gastoadministracion/<pk>/', views.elimina_gastoadministracion, name='elimina_gastoadministracion'),
    path('edita_gastoventa/<pk>/', views.edita_gastoventa, name='edita_gastoventa'),
    path('elimina_gastoventa/<pk>/', views.elimina_gastoventa, name='elimina_gastoventa'),
    path('edita_manoobra/<pk>/', views.edita_manoobra, name='edita_manoobra'),
    path('elimina_manoobra/<pk>/', views.elimina_manoobra, name='elimina_manoobra'),
    path('tema0_1',views.tema0_1, name='tema0_1'),
    path('tema1_1',views.tema1_1, name='tema1_1'),
    path('tema1_2',views.tema1_2, name='tema1_2'),
    path('tema1_3',views.tema1_3, name='tema1_3'),
    path('tema1_4',views.tema1_4, name='tema1_4'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)