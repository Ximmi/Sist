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
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)