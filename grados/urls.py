from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_grado, name='listar_grados'),
    path('crear/', views.crear_grado, name='crear_grado'),
    path('editar/<int:pk>/', views.editar_grado, name='editar_grado'),
    path('eliminar/<int:pk>/', views.eliminar_grado, name='eliminar_grado'),
    path('historial_grado/listar', views.listar_historial_grados, name='listar_historial_grados'),
    path('historial_grado/crear', views.crear_historial_grado, name='crear_historial_grado' ),
    path('historial_grado/editar/<int:pk>', views.editar_historial_grado, name='editar_historial_grado'),
    path('historial_grado/eliminar/<int:pk>', views.eliminar_historial_grado, name='eliminar_historial_grado')
]
