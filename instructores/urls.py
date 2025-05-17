from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_instructores, name='listar_instructores'),
    path('crear/', views.crear_instructor, name='crear_instructor'),
    path('editar/<int:pk>/', views.editar_instructor, name='editar_instructor'),
    path('eliminar/<int:pk>/', views.eliminar_instructor, name='eliminar_instructor'),
]
