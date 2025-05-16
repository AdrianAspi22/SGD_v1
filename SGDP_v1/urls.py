"""
URL configuration for SGDP_v1 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from usuarios import views as usuario_views
from dojos import views as dojo_views
from alumnos import views as alumno_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', usuario_views.login_view, name='login'),  # Ruta para el login
    path('logout/', usuario_views.logout_view, name='logout'),  # Ruta para logout
    path('', lambda request: redirect('login')),  # Redirige a login desde la raíz
    path('dojos/', include('dojos.urls')),
    path('crear_dojo/', dojo_views.crear_dojo, name='crear_dojo'),  # Asegúrate de tener esta vista
    path('dashboard_general/', dojo_views.dashboard_general, name='dashboard_general'),
    path('dashboard_dojo/', dojo_views.dashboard_dojo, name='dashboard_dojo'),  # Vista para el dojo
    path('examenes/', include('examenes.urls')),  # URLs para la app exámenes
    path('pagos/', include('pagos.urls')), # URLs para la app pagos
    #path('instructores/', include('instructores.urls')),  # URLs para la app instructores
    path('grados/', include('grados.urls')),  # URLs para la app grados
    #path('horarios/', include('horarios.urls')),  # URLs para la app horarios
]
