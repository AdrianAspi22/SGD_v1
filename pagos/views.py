# pagos/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Pago
from .forms import PagoForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Vista para listar los pagos
@login_required
def listar_pagos(request):
    pagos = Pago.objects.filter(dojo=request.user.dojo)
    return render(request, 'pagos/listar_pagos.html', {'pagos': pagos})

# Vista para crear un nuevo pago
@login_required
def crear_pago(request):
    if request.method == 'POST':
        form = PagoForm(request.POST)
        if form.is_valid():
            pago = form.save(commit=False)
            pago.dojo = request.user.dojo
            pago.save()
            messages.success(request, 'Pago creado con éxito.')
            return redirect('listar_pagos')
    else:
        form = PagoForm()
    return render(request, 'pagos/crear_pago.html', {'form': form})

# En la vista de editar_pago
@login_required
def editar_pago(request, pk):
    dojo = request.user.dojo  # Accedemos al dojo del usuario
    pago = get_object_or_404(Pago, id=pk, dojo=dojo)

    if request.method == 'POST':
        form = PagoForm(request.POST, instance=pago)
        if form.is_valid():
            pago = form.save(commit=False)
            pago.dojo = dojo  # Aseguramos que el dojo se mantenga correctamente
            pago.save()
            messages.success(request, 'Pago actualizado con éxito')
            return redirect('listar_pagos')
    else:
        form = PagoForm(instance=pago)

    return render(request, 'pagos/editar_pago.html', {'form': form})


# Vista para eliminar un pago existente
@login_required
def eliminar_pago(request, pago_id):
    dojo = request.user.dojo
    pago = get_object_or_404(Pago, id=pago_id, dojo=dojo)

    if request.method == 'POST':
        pago.delete()
        messages.success(request, 'Pago eliminado con éxito.')
        return redirect('listar_pagos')

    return render(request, 'pagos/eliminar_pago.html', {'pago': pago})
