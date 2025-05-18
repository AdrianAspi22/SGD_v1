from .models import HistorialGrado, Grado
from datetime import date

def promover_si_corresponde(alumno, observacion=None):
    historial_actual = (
        HistorialGrado.objects
        .filter(alumno=alumno, estado=True)
        .order_by('-create_at')
        .first()
    )

    if not historial_actual:
        return

    grado_actual = historial_actual.grado
    siguiente_id = grado_actual.id + 1
    print (f"Grado actual: {grado_actual.id}, id siguiente: {siguiente_id}")

    try:
        siguiente_grado = Grado.objects.get(id=siguiente_id)
    except Grado.DoesNotExist:
        print(f"❌ No existe un grado con id = {siguiente_id}")
        return

    # Verificar que no esté duplicado
    if HistorialGrado.objects.filter(alumno=alumno, grado=siguiente_grado).exists():
        print("⚠️ Ya existe ese grado en el historial")
        return

    # Crear nuevo historial
    HistorialGrado.objects.create(
        alumno=alumno,
        grado=siguiente_grado,
        fecha_obtencion=date.today(),
        observaciones=observacion or 'Promoción automática'
    )

    print(f"✅ Historial creado para grado id = {siguiente_id}")
