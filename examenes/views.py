# examenes/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Examen, AlumnoExamen
from .forms import ExamenForm, AlumnoExamenForm, EvaluarExamenForm
from grados.models import HistorialGrado
from grados.services import promover_si_corresponde

# Vista para listar los exámenes
@login_required
def listar_examenes(request):
    dojo = request.user.dojo  # Asumiendo que el usuario es instructor y tiene dojo
    examenes = Examen.objects.filter(instructor__dojo=dojo)
    return render(request, 'examenes/listar_examenes.html', {'examenes': examenes})


# Vista para crear un nuevo examen
@login_required
def crear_examen(request):
    if request.method == 'POST':
        form = ExamenForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_examenes')  # Redirigir a la lista de exámenes
    else:
        form = ExamenForm()
    return render(request, 'examenes/crear_examen.html', {'form': form})

# Vista para editar un examen
@login_required
def editar_examen(request, pk):
    examen = get_object_or_404(Examen, pk=pk)
    if request.method == 'POST':
        form = ExamenForm(request.POST, instance=examen)
        if form.is_valid():
            form.save()
            return redirect('listar_examenes')  # Redirigir a la lista de exámenes
    else:
        form = ExamenForm(instance=examen)
    return render(request, 'examenes/editar_examen.html', {'form': form})

# Vista para eliminar un examen
@login_required
def eliminar_examen(request, pk):
    examen = get_object_or_404(Examen, pk=pk)
    if request.method == 'POST':
        examen.delete()
        return redirect('listar_examenes')  # Redirigir a la lista de exámenes
    return render(request, 'examenes/eliminar_examen.html', {'examen': examen})

# Vista para listar asignaciones
@login_required
def listar_asignaciones(request):
    asignaciones = AlumnoExamen.objects.all()
    return render(request, 'examenes/listar_asignaciones.html', {'asignaciones': asignaciones})

# Vista para asignar un examen a un alumno
@login_required
def asignar_examen(request):
    if request.method == 'POST':
        form = AlumnoExamenForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_examenes')  # Redirigir a la lista de asignaciones
    else:
        form = AlumnoExamenForm()
    return render(request, 'examenes/asignar_examen.html', {'form': form})

# Vista para editar una asignación de examen
@login_required
def editar_asignacion(request, pk):
    asignacion = get_object_or_404(AlumnoExamen, pk=pk)
    if request.method == 'POST':
        form = AlumnoExamenForm(request.POST, instance=asignacion)
        if form.is_valid():
            form.save()
            return redirect('listar_examenes')  # Redirigir a la lista de asignaciones
    else:
        form = AlumnoExamenForm(instance=asignacion)
    return render(request, 'examenes/editar_asignacion.html', {'form': form})

# Vista para eliminar una asignación de examen
@login_required
def eliminar_asignacion(request, pk):
    asignacion = get_object_or_404(AlumnoExamen, pk=pk)
    asignacion.delete()
    return redirect('asignaciones_por_examen', examen_id=asignacion.examen.id)

@login_required
def evaluar_examen(request, pk):
    asignacion = get_object_or_404(AlumnoExamen, pk=pk)
    if request.method == 'POST':
        form = EvaluarExamenForm(request.POST, instance=asignacion)
        if form.is_valid():
            form.save()
            if asignacion.nota >= asignacion.examen.nota_aprobacion:
                asignacion.aprobado = True
                promover_si_corresponde(asignacion.alumno, asignacion.observaciones)
            else:
                asignacion.aprobado = False
            asignacion.save()

            return redirect('asignaciones_por_examen', examen_id=asignacion.examen.id)
    else:
        form = EvaluarExamenForm(instance=asignacion)
    return render(request, 'examenes/evaluar_examen.html', {'form': form, 'asignacion': asignacion})

@login_required
def asignaciones_por_examen(request, examen_id):
    examen = get_object_or_404(Examen, pk=examen_id)
    asignaciones = AlumnoExamen.objects.filter(examen=examen, estado=True).select_related('alumno')
    return render(request, 'examenes/asignaciones_por_examen.html', {
        'examen': examen,
        'asignaciones': asignaciones,
    })