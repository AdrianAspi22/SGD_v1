from django.shortcuts import render, redirect, get_object_or_404
from .models import Instructor
from .forms import InstructorForm
from django.contrib.auth.decorators import login_required


# Listar instructores del dojo del usuario
@login_required
def listar_instructores(request):
    instructores = Instructor.objects.filter(dojo=request.user.dojo)
    return render(request, 'instructores/listar_instructores.html', {'instructores': instructores})


# Crear instructor (asignando el dojo automáticamente)
@login_required
def crear_instructor(request):
    if request.method == 'POST':
        form = InstructorForm(request.POST)
        if form.is_valid():
            instructor = form.save(commit=False)
            instructor.dojo = request.user.dojo  # Asigna el dojo actual
            instructor.save()
            return redirect('listar_instructores')
    else:
        form = InstructorForm()
    return render(request, 'instructores/crear_instructor.html', {'form': form})

# Editar instructor solo si pertenece al dojo del usuario
@login_required
def editar_instructor(request, pk):
    instructor = get_object_or_404(Instructor, pk=pk, dojo=request.user.dojo)
    if request.method == 'POST':
        form = InstructorForm(request.POST, instance=instructor)
        if form.is_valid():
            form.save()
            return redirect('listar_instructores')
    else:
        form = InstructorForm(instance=instructor)
    return render(request, 'instructores/editar_instructor.html', {'form': form})

# Eliminar instructor solo si pertenece al dojo del usuario
@login_required
def eliminar_instructor(request, pk):
    instructor = get_object_or_404(Instructor, pk=pk, dojo=request.user.dojo)
    if request.method == 'POST':
        instructor.delete()
        return redirect('listar_instructores')
    return render(request, 'instructores/confirmar_eliminar_instructor.html', {'instructor': instructor})
