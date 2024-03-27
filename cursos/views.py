from django.shortcuts import render

from .models import *
from datetime import date


# Create your views here.
def home(request):
    num_cursos = Curso.objects.filter(estado="publicado").count()
    num_estudiantes = Inscripcion.objects.values("estudiante").count()

    proximo_curso = (
        Curso.objects.filter(estado="publicado", fecha_publicacion__gt=date.today())
        .order_by("fecha_publicacion")
        .first()
    )

    cursos_destacados = Curso.objects.filter(estado="publicado", destacado=True)[:3]

    cursos_destacados_data = []
    for curso in cursos_destacados:
        curso_data = {
            "id": curso.id,
            "nombre": curso.nombre,
            "descripcion": curso.descripcion,
            "imagen": f"img/{curso.categoria.color}.png",
        }
        cursos_destacados_data.append(curso_data)

    context = {
        "num_cursos": num_cursos,
        "num_estudiantes": num_estudiantes,
        "proximo_curso": proximo_curso,
        "cursos_destacados": cursos_destacados_data,
    }

    return render(request, "cursos/home.html", context)
