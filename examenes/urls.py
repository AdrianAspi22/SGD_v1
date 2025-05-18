# examenes/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('examenes/', views.listar_examenes, name='listar_examenes'),  # Para listar los exámenes
    path('examenes/nuevo/', views.crear_examen, name='crear_examen'),  # Para crear un nuevo examen
    path('examenes/editar/<int:pk>/', views.editar_examen, name='editar_examen'),  # Para editar un examen
    path('examenes/eliminar/<int:pk>/', views.eliminar_examen, name='eliminar_examen'),  # Para eliminar un examen

    path('asignaciones/evaluar/<int:pk>/', views.evaluar_examen, name='evaluar_examen'),  # Para evaluar un examen
    path('examenes/<int:examen_id>/asignaciones/', views.asignaciones_por_examen, name='asignaciones_por_examen'),  # Para ver asignaciones por examen

    path('asignaciones/', views.listar_asignaciones, name='listar_asignaciones'),  # Para listar las asignaciones
    path('asignaciones/nuevo/', views.asignar_examen, name='asignar_examen'),  # Para asignar un examen a un alumno
    path('asignaciones/editar/<int:pk>/', views.editar_asignacion, name='editar_asignacion'),  # Para editar asignación
    path('asignaciones/eliminar/<int:pk>/', views.eliminar_asignacion, name='eliminar_asignacion'),  # Para eliminar asignación

    path('reporte-instructores/', views.reporte_instructores, name='reporte_instructores'),
]
