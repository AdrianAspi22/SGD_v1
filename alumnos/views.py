from django.shortcuts import render, redirect, get_object_or_404
from .models import Alumno
from .forms import AlumnoForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator

# Vista para listar alumnos con filtros y paginación
@login_required
def listar_alumnos(request):
    query = request.GET.get('q', '')
    per_page = int(request.GET.get('per_page', 10))

    # Filtros individuales
    filtro_matricula = request.GET.get('matricula')
    filtro_grupo = request.GET.get('grupo')
    filtro_cinturon = request.GET.get('cinturon')
    filtro_estado = request.GET.get('estado')

    # Filtro base: alumnos del dojo del usuario
    filtros = Q(dojo=request.user.dojo)

    if query:
        filtros &= Q(nombre__icontains=query) | Q(apellido__icontains=query)

    if filtro_matricula:
        filtros &= Q(matricula=filtro_matricula)

    if filtro_grupo:
        filtros &= Q(grupo=filtro_grupo)

    if filtro_cinturon:
        filtros &= Q(cinturon=filtro_cinturon)

    if filtro_estado:
        filtros &= Q(estado=filtro_estado)

    alumnos_list = Alumno.objects.filter(filtros).order_by('id')

    paginator = Paginator(alumnos_list, per_page)
    page_number = request.GET.get('page')
    alumnos = paginator.get_page(page_number)

    return render(request, 'alumnos/listar_alumnos.html', {
        'alumnos': alumnos,
        'query': query,
        'result_count': alumnos_list.count() if query else None,
        'per_page': per_page,

        # filtros activos para mantener estado en la plantilla
        'filtro_matricula': filtro_matricula,
        'filtro_grupo': filtro_grupo,
        'filtro_cinturon': filtro_cinturon,
        'filtro_estado': filtro_estado,
    })


# Vista para crear un alumno
@login_required
def crear_alumno(request):
    if request.method == 'POST':
        form = AlumnoForm(request.POST)
        if form.is_valid():
            alumno = form.save(commit=False)
            alumno.dojo = request.user.dojo  # Asociar al dojo del usuario
            alumno.save()
            return redirect('listar_alumnos')
    else:
        form = AlumnoForm()
    return render(request, 'alumnos/crear_alumno.html', {'form': form})

# Vista para editar un alumno
@login_required
def editar_alumno(request, pk):
    alumno = get_object_or_404(Alumno, pk=pk, dojo=request.user.dojo)
    if request.method == 'POST':
        form = AlumnoForm(request.POST, instance=alumno)
        if form.is_valid():
            form.save()
            return redirect('listar_alumnos')
    else:
        form = AlumnoForm(instance=alumno)
    return render(request, 'alumnos/editar_alumno.html', {'form': form, 'alumno': alumno})

# Vista para eliminar un alumno
@login_required
def eliminar_alumno(request, pk):
    alumno = get_object_or_404(Alumno, pk=pk, dojo=request.user.dojo)
    alumno.delete()
    return redirect('listar_alumnos')