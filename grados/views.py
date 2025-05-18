from django.shortcuts import render, redirect, get_object_or_404
from .models import Grado, HistorialGrado
from .forms import GradoForm, HistorialGradoForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator

# Listar grados
@login_required
def listar_grado(request):
    grados = Grado.objects.all()
    return render(request, 'grados/listar_grados.html', {'grados': grados})

# Crear nuevo grado
@login_required
def crear_grado(request):
    if request.method == 'POST':
        form = GradoForm(request.POST)
        if form.is_valid():
            grado = form.save(commit=False)
            grado.dojo = request.user.dojo  # Asociar al dojo del usuario
            grado.save()
            form.save()
            return redirect('listar_grados')
    else:
        form = GradoForm()
    return render(request, 'grados/crear_grado.html', {'form': form})

# Editar grado
@login_required
def editar_grado(request, pk):
    grado = get_object_or_404(Grado, pk=pk)
    if request.method == 'POST':
        form = GradoForm(request.POST, instance=grado)
        if form.is_valid():
            form.save()
            return redirect('listar_grados')
    else:
        form = GradoForm(instance=grado)
    return render(request, 'grados/editar_grado.html', {'form': form})

# Eliminar grado
@login_required
def eliminar_grado(request, pk):
    grado = get_object_or_404(Grado, pk=pk)
    if request.method == 'POST':
        grado.delete()
        return redirect('listar_grados')
    return render(request, 'grados/eliminar_grado.html', {'grado': grado})


@login_required
def listar_historial_grados(request):
    historial_grados = HistorialGrado.objects.all()
    return render(request, 'HistorialGrado/listar_historial_grados.html', {'historial_grados': historial_grados})

# Crear nuevo grado
@login_required
def crear_historial_grado(request):
    if request.method == 'POST':
        form = HistorialGradoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_historial_grados')
    else:
        form = HistorialGradoForm()
    return render(request, 'HistorialGrado/crear_historial_grado.html', {'form': form})

# Editar grado
@login_required
def editar_historial_grado(request, pk):
    historial_grado = get_object_or_404(Grado, pk=pk)
    if request.method == 'POST':
        form = HistorialGradoForm(request.POST, instance=historial_grado)
        if form.is_valid():
            form.save()
            return redirect('listar_historial_grados')
    else:
        form = HistorialGradoForm(instance=historial_grado)
    return render(request, 'HistorialGrado/editar_historial_grado.html', {'form': form})

# Eliminar grado
@login_required
def eliminar_historial_grado(request, pk):
    historial_grado = get_object_or_404(Grado, pk=pk)
    if request.method == 'POST':
        historial_grado.delete()
        return redirect('listar_grados')
    return render(request, 'HistorialGrado/eliminar_grado.html', {'historial_grado': historial_grado})
