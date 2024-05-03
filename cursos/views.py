from django.shortcuts import render, redirect

from .models import *
from datetime import date
from .forms.curso_form import CursoForm

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse

from django.db.models import Q


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
            "imagen": curso.imagen.url,
        }
        cursos_destacados_data.append(curso_data)

    context = {
        "num_cursos": num_cursos,
        "num_estudiantes": num_estudiantes,
        "proximo_curso": proximo_curso,
        "cursos_destacados": cursos_destacados_data,
    }

    return render(request, "cursos/home.html", context)


def curso_list(request):
    cursos = Curso.objects.select_related("categoria").filter(estado="publicado")

    cursos_data = []
    for curso in cursos:
        curso_data = {
            "id": curso.id,
            "nombre": curso.nombre,
            "descripcion": curso.descripcion,
            "precio": curso.precio,
            "fecha_publicacion": curso.fecha_publicacion,
            "categoria": curso.categoria.nombre,
            "duracion": curso.duracion,
            "num_estudiantes": curso.estudiantes.count(),
            "imagen": curso.imagen.url,
        }
        cursos_data.append(curso_data)

    context = {"cursos": cursos_data}
    return render(request, "cursos/curso_list.html", context=context)


def curso_detail(request, curso_id):
    curso = (
        Curso.objects.prefetch_related("estudiantes")
        .prefetch_related("instructor")
        .get(id=curso_id)
    )

    curso_data = {
        "id": curso.id,
        "nombre": curso.nombre,
        "descripcion": curso.descripcion,
        "precio": curso.precio,
        "fecha_publicacion": curso.fecha_publicacion,
        "categoria": curso.categoria.nombre,
        "duracion": curso.duracion,
        "num_estudiantes": curso.estudiantes.count(),
        "imagen": curso.imagen.url,
        "estado": curso.estado,
        "instructor": curso.instructor,
        "imagen_instructor": curso.instructor.avatar.url,
        "contenido": curso.contenido,
    }

    if request.user.is_superuser:
        has_access = True
    else:
        try:
            instructor = Instructor.objects.get(user=request.user.id)
            has_access = Curso.objects.filter(instructor=instructor).exists()
        except Instructor.DoesNotExist:
            has_access = False

    context = {
        "curso": curso_data,
        "has_access": has_access,
    }
    return render(request, "cursos/curso_detail.html", context=context)


def create_curso(request):
    if request.method == "POST":
        form = CursoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("curso_list")
    else:  # Método GET
        form = CursoForm()

    context = {"titulo": "Nuevo Curso", "form": form, "submit": "Crear Curso"}
    return render(request, "cursos/curso_form.html", context)


@login_required
def update_curso(request, curso_id):
    curso = Curso.objects.get(id=curso_id)
    if request.method == "POST":
        form = CursoForm(request.POST, request.FILES, instance=curso)
        if form.is_valid():
            form.save()
            return redirect("curso_detail", curso_id=curso_id)
    else:  # Método GET
        form = CursoForm(instance=curso)

    context = {"titulo": "Editar Curso", "form": form, "submit": "Actualizar Curso"}
    return render(request, "cursos/curso_form.html", context)


@login_required
def delete_curso(request, curso_id):
    curso = Curso.objects.get(id=curso_id)
    curso.delete()
    return redirect("curso_list")


@login_required
def hide_curso(request, curso_id):
    curso = Curso.objects.get(id=curso_id)
    curso.estado = "archivado"
    curso.save()
    return redirect("curso_list")


@login_required
def hidden_cursos(request):
    cursos = Curso.objects.select_related("categoria").filter(estado="archivado")

    cursos_data = []
    for curso in cursos:
        curso_data = {
            "id": curso.id,
            "nombre": curso.nombre,
            "descripcion": curso.descripcion,
            "precio": curso.precio,
            "fecha_publicacion": curso.fecha_publicacion,
            "categoria": curso.categoria.nombre,
            "duracion": curso.duracion,
            "num_estudiantes": curso.estudiantes.count(),
            "imagen": curso.imagen.url,
        }
        cursos_data.append(curso_data)

    context = {"cursos": cursos_data}
    return render(request, "cursos/curso_list.html", context=context)


@login_required
def restore_curso(request, curso_id):
    curso = Curso.objects.get(id=curso_id)
    curso.estado = "publicado"
    curso.save()
    return redirect("hidden_cursos")


def login_view(request):
    # Paramétros de ruta para redirección
    next_url = request.GET.get("next")

    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("home"))

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if next_url:
                return redirect(next_url)
            return redirect("home")
        else:
            return render(
                request,
                "cursos/login.html",
                {"error": "Nombre de usuario o contraseña incorrectos"},
            )
    else:  # Método GET
        return render(request, "cursos/login.html")


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))


def search_view(request):
    query = request.GET.get("query", "")
    if query:
        cursos = Curso.objects.filter(
            Q(nombre__icontains=query)
            | Q(contenido__icontains=query)
            | Q(descripcion__icontains=query),
            estado="publicado",
        )
    else:
        cursos = Curso.objects.none()  # No hay resultados si no hay consulta

    return render(
        request, "cursos/search_results.html", {"cursos": cursos, "query": query}
    )
