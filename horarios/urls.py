from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_grado, name='listar_horarios'),
    path('crear/', views.crear_horario, name='crear_horario'),
    path('editar/<int:pk>/', views.editar_horario, name='editar_horario'),
    path('eliminar/<int:pk>/', views.eliminar_horario, name='eliminar_horario'),


]