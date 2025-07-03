from django.shortcuts import render, redirect, get_object_or_404
from .models import Alumno
from django.db.models import OuterRef, Subquery, F, CharField, Value
from django.db.models.functions import Concat
from grados.models import Grado, HistorialGrado
from .forms import AlumnoForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse


@login_required
def listar_alumnos(request):
    query = request.GET.get('q', '')
    per_page = int(request.GET.get('per_page', 10))

    # Filtros iniciales
    filtros = Q(dojo=request.user.dojo)

    filtro_matricula = request.GET.get('matricula')
    filtro_grupo = request.GET.get('grupo')
    filtro_cinturon = request.GET.get('cinturon')
    filtro_estado = request.GET.get('estado')

    if query:
        filtros &= Q(nombre__icontains=query) | Q(apellido__icontains=query)

    if filtro_matricula:
        filtros &= Q(matricula=filtro_matricula)

    if filtro_grupo:
        filtros &= Q(grupo=filtro_grupo)

    if filtro_estado:
        filtros &= Q(estado=filtro_estado)

    ultimos_grados = HistorialGrado.objects.filter(
        alumno=OuterRef('pk')
    ).order_by('-create_at')

    alumnos_qs = Alumno.objects.filter(filtros).annotate(
        grado_nivel=Subquery(ultimos_grados.values('grado__nivel')[:1]),
        grado_tipo=Subquery(ultimos_grados.values('grado__tipo')[:1]),
        grado_color=Subquery(ultimos_grados.values('grado__color')[:1]),
        grado_actual=Concat(
            F('grado_nivel'),
            Value('.º '),
            F('grado_tipo'),
            Value(': '),
            F('grado_color'),
            output_field=CharField()
        )
    ).order_by('id')

    if filtro_cinturon:
        alumnos_qs = alumnos_qs.filter(grado_actual__iexact=filtro_cinturon)

    paginator = Paginator(alumnos_qs, per_page)
    page_number = request.GET.get('page')
    alumnos = paginator.get_page(page_number)

    colores_grado_qs = Grado.objects.values('color', 'nivel', 'tipo').distinct()

    colores_grado = [
        f"{item['nivel']}.º {item['tipo'].capitalize()}: {item['color']}"
        for item in colores_grado_qs
    ]

    total_resultados = alumnos_qs.count()

    return render(request, 'alumnos/listar_alumnos.html', {
        'alumnos': alumnos,
        'query': query,
        'result_count': total_resultados,
        'per_page': per_page,
        'filtro_matricula': filtro_matricula,
        'filtro_grupo': filtro_grupo,
        'filtro_cinturon': filtro_cinturon,
        'filtro_estado': filtro_estado,
        'colores_grado': colores_grado,
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
    alumno = get_object_or_404(Alumno, pk=pk)
    form = AlumnoForm(request.POST or None, instance=alumno)

    if form.is_valid():
        form.save()
        return redirect('listar_alumnos')  # Redirige a la lista de alumnos

    return render(request, 'alumnos/editar_alumno.html', {'form': form, 'alumno': alumno})

# Vista para eliminar un alumno
@login_required
def eliminar_alumno(request, pk):
    alumno = get_object_or_404(Alumno, pk=pk, dojo=request.user.dojo)
    alumno.delete()
    return redirect('listar_alumnos')