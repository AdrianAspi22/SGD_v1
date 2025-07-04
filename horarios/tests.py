from django.db import models
import pytest
from django.core.exceptions import ValidationError
from horarios.models import Horario
from instructores.models import Instructor
from datetime import time

@pytest.mark.django_db
def test_horario_valido():
    instructor = Instructor.objects.create(username='instructor1', password='1234')
    horario = Horario(
        dia='Lunes',
        hora_inicio=time(8, 0),
        hora_fin=time(10, 0),
        instructor=instructor
    )
    # No debe lanzar error
    horario.clean()

@pytest.mark.django_db
def test_horario_invalido_hora_inicio_mayor():
    instructor = Instructor.objects.create(username='instructor2', password='1234')
    horario = Horario(
        dia='Martes',
        hora_inicio=time(10, 0),
        hora_fin=time(8, 0),
        instructor=instructor
    )
    with pytest.raises(ValidationError):
        horario.clean()

