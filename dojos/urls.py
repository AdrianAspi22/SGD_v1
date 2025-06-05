# dojos/urls.py
from django.urls import path
from . import views
from alumnos import views as alumnos_views  # Importamos las vistas de la app alumnos

urlpatterns = [
    path('crear/', views.crear_dojo, name='crear_dojo'),
    path('dashboard/', views.dashboard_dojo, name='dashboard'),
        # URLs para gestionar alumnos (en la app alumnos)
    path('alumnos/', alumnos_views.listar_alumnos, name='listar_alumnos'),
    path('alumnos/crear/', alumnos_views.crear_alumno, name='crear_alumno'),
    path('alumnos/editar/<int:pk>/', alumnos_views.editar_alumno, name='editar_alumno'),
    path('alumnos/eliminar/<int:pk>/', alumnos_views.eliminar_alumno, name='eliminar_alumno'),
]
