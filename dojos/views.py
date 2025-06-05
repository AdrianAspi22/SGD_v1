# dojos/views.py
from django.shortcuts import render, redirect
from django.db.models import Avg
from django.contrib.auth.decorators import login_required
from .forms import DojoForm
from django.contrib import messages
from dojos.models import Dojo  # Asegúrate de tener el modelo Dojo
from examenes.models import AlumnoExamen  # importa desde la app examen

from grados.models import HistorialGrado  # Ajusta si tu app tiene otro nombre
from django.db.models import Max, Q
from collections import Counter



@login_required
def crear_dojo(request):
    if request.user.tipo != 'dojo':
        return redirect('dashboard_general')  # Si no es un admin dojo, redirigir

    if request.method == 'POST':
        form = DojoForm(request.POST)
        if form.is_valid():
            dojo = form.save(commit=False)
            dojo.usuario = request.user  # Asignar el dojo al usuario logueado
            dojo.save()
            messages.success(request, 'Dojo creado exitosamente.')
            return redirect('dashboard_dojo')  # Redirigir a la vista del dojo

    else:
        form = DojoForm()

    return render(request, 'dojos/crear_dojo.html', {'form': form})

@login_required
def dashboard_dojo(request):
    try:
        dojo = Dojo.objects.get(usuario=request.user)

        # Datos para gráfico de aprobados vs no aprobados
        aprobados = AlumnoExamen.objects.filter(aprobado=True, alumno__dojo=dojo).count()
        no_aprobados = AlumnoExamen.objects.filter(aprobado=False, alumno__dojo=dojo).count()

        context = {
            'dojo': dojo,
            'message': f'Bienvenido al Dashboard de tu Dojo: {dojo.nombre}',
            'aprobados': aprobados,
            'no_aprobados': no_aprobados,
        }

        # Promedio de notas por instructor
        promedios = (
            AlumnoExamen.objects
            .filter(nota__isnull=False, examen__instructor__isnull=False, alumno__dojo=dojo)
            .values('examen__instructor__nombres')
            .annotate(promedio=Avg('nota'))
        )


        # Promedio de notas por alumno
        promedios_alumnos = (
            AlumnoExamen.objects
            .filter(nota__isnull=False, alumno__dojo=dojo)
            .values('alumno__nombre', 'alumno__apellido')  # o 'alumno__nombre_completo' si tienes uno
            .annotate(promedio=Avg('nota'))
            .order_by('alumno__nombre')
        )

        labels_alumnos = [
            f"{item['alumno__nombre']} {item['alumno__apellido']}" for item in promedios_alumnos
        ]
        data_promedios_alumnos = [float(item['promedio']) for item in promedios_alumnos]

        context.update({
            'labels_alumnos': labels_alumnos,
            'data_promedios_alumnos': data_promedios_alumnos,
        })

        labels_instructores = [item['examen__instructor__nombres'] for item in promedios]
        data_promedios = [float(item['promedio']) for item in promedios]

        context.update({
            'labels_instructores': labels_instructores,
            'data_promedios': data_promedios,
        })

        # Últimos grados por alumno
        subquery = (
            HistorialGrado.objects
            .filter(estado=True, alumno__dojo=dojo)
            .values('alumno')
            .annotate(ultima_fecha=Max('fecha_obtencion'))
        )
  
        # Construir Q dinámico
        condiciones = Q()
        for item in subquery:
            condiciones |= Q(alumno_id=item['alumno'], fecha_obtencion=item['ultima_fecha'])

        ultimos_grados = (
            HistorialGrado.objects
            .filter(estado=True, alumno__dojo=dojo)
            .filter(condiciones)
            .select_related('grado')
        )

        contador_colores = Counter([h.grado.color for h in ultimos_grados])
        labels_grados = list(contador_colores.keys())
        data_grados = list(contador_colores.values())

        context.update({
            'labels_grados': labels_grados,
            'data_grados': data_grados,
        })

    except Dojo.DoesNotExist:
        context = {
            'message': 'No tienes un dojo asignado.',
            'aprobados': 0,
            'no_aprobados': 0,
        }

    return render(request, 'dojos/dashboard_dojo.html', context)

@login_required
def dashboard_general(request):
    # Aquí puedes agregar datos que desees mostrar en el dashboard del admin general
    # Ejemplo: estadísticas, listado de dojos, etc.
    
    # Para este ejemplo, agregamos un mensaje de bienvenida
    context = {
        'user': request.user,
        'message': 'Bienvenido al Dashboard General.',
    }

    return render(request, 'general/dashboard_general.html', context)
