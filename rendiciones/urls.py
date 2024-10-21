from django.urls import path
from . import views
from django.contrib.auth import views as auth_views  # Importar LoginView de Django

urlpatterns = [
    path('', views.index, name='index'),  # Ruta raíz
    path('login/', auth_views.LoginView.as_view(), name='login'),  # Ruta para el login
    path('redirect_user/', views.redirect_user, name='redirect_user'),
    path('jefe_dashboard/', views.jefe_dashboard, name='jefe_dashboard'),  # Ruta para jefe de obra
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),  # Ruta para admin
    path('proyectos/', views.lista_proyectos, name='lista_proyectos'),  # Listar proyectos
    path('proyectos/crear/', views.crear_proyecto, name='crear_proyecto'),
    path('rendiciones/subir/', views.subir_rendicion, name='subir_rendicion'),
    path('rendiciones/', views.subir_rendicion, name='lista_rendiciones'),
    path('rendiciones/eliminar/<int:rendicion_id>/', views.eliminar_rendicion, name='eliminar_rendicion'),
]
