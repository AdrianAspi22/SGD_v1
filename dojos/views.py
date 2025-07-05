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
from alumnos.models import Alumno  # Asegúrate de tener el modelo Alumno
from django.db.models import F, ExpressionWrapper, DurationField
from django.db.models import Count, IntegerField
from django.db.models.functions import ExtractYear

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
def dashboard_grado(request):
    alumnos = Alumno.objects.filter(estado='Activo')

    alumno_id = request.GET.get('alumno_id')
    historial = []

    if alumno_id:
        historial = HistorialGrado.objects.filter(
            alumno_id=alumno_id
        ).select_related('grado').order_by('fecha_obtencion')

    fechas = [registro.fecha_obtencion.strftime('%Y-%m-%d') for registro in historial]
    niveles = [registro.grado.nivel for registro in historial]

    #segundo grafico

    ultimos_grados = HistorialGrado.objects.filter(
        alumno__in=alumnos
    ).values('alumno').annotate(
        ultima_fecha=Max('fecha_obtencion')
    )

    grados_alumnos = HistorialGrado.objects.filter(
        alumno__in=alumnos,
        fecha_obtencion__in=[g['ultima_fecha'] for g in ultimos_grados]
    ).select_related('grado')

    from collections import Counter
    conteo_grados = Counter([registro.grado.nivel for registro in grados_alumnos])

    niveles = list(conteo_grados.keys())
    cantidades = list(conteo_grados.values())

    #tercer grafico
    # historial con diferencia de tiempo
    historial = HistorialGrado.objects.filter(
        alumno__in=alumnos,
        fecha_obtencion__gte=F('alumno__create_at')  # Solo grados después de inscripción
    ).select_related('alumno', 'grado').annotate(
        dias_para_grado=ExpressionWrapper(
            F('fecha_obtencion') - F('alumno__create_at'),
            output_field=DurationField()
        )
    )

    from collections import defaultdict
    conteo_promedios = defaultdict(list)

    for registro in historial:
        conteo_promedios[registro.grado.nivel].append(registro.dias_para_grado.days)

    niveles_tiempo = []
    tiempos_promedio = []

    for nivel, tiempos in conteo_promedios.items():
        promedio = sum(tiempos) / len(tiempos)
        niveles_tiempo.append(nivel)
        tiempos_promedio.append(round(promedio, 1))

    #cuarto grafico
    historial_4 = HistorialGrado.objects.filter(
        alumno__in=alumnos
    ).annotate(
        anio=ExtractYear(F('fecha_obtencion'), function='YEAR', output_field=IntegerField())
    ).values('anio', 'grado__nivel').annotate(
        cantidad=Count('id')
    ).order_by('anio', 'grado__nivel')

    from collections import defaultdict

    datos_por_anio = defaultdict(lambda: defaultdict(int))

    for registro in historial_4:
        anio = registro['anio']
        nivel = registro['grado__nivel']
        cantidad = registro['cantidad']
        datos_por_anio[anio][nivel] = cantidad

    anios = list(datos_por_anio.keys())
    niveles = sorted({nivel for anio_data in datos_por_anio.values() for nivel in anio_data.keys()})

    datasets = []
    for nivel in niveles:
        data = [datos_por_anio[anio].get(nivel, 0) for anio in anios]
        datasets.append({'label': f'Grado {nivel}', 'data': data})

    return render(request, 'dojos/dashboard_grado.html', {
        'alumnos': alumnos,
        'fechas': fechas,
        'niveles': niveles,
        'alumno_id': alumno_id,
        'niveles': niveles,
        'cantidades': cantidades,
        'niveles_tiempo': niveles_tiempo,
        'tiempos_promedio': tiempos_promedio,
        'anios': anios,
        'datasets': datasets,
    })



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
