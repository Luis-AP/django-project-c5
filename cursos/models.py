from django.db import models
from datetime import timedelta
from django.core.exceptions import ValidationError


class Instructor(models.Model):
    nombre = models.CharField(max_length=100)
    bio = models.TextField()

    def __str__(self):
        return self.nombre


class Estudiante(models.Model):
    nombre = models.CharField(max_length=150)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.nombre


class Categoria(models.Model):
    nombre = models.CharField(max_length=50)
    color = models.CharField(max_length=20)

    def __str__(self):
        return self.nombre


def precio_positivo(value):
    if value <= 0:
        raise ValidationError("El precio debe ser un número positivo.")


def duracion_minima(value):
    if value < timedelta(hours=20):
        raise ValidationError("La duración mínima debe ser de 20 horas.")


class Curso(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.IntegerField(validators=[precio_positivo])
    fecha_publicacion = models.DateField(verbose_name="Fecha de publicación")
    categoria = models.ForeignKey(
        Categoria, on_delete=models.SET_NULL, null=True, blank=True
    )
    duracion = models.DurationField(
        default=timedelta(days=0), blank=True, validators=[duracion_minima]
    )
    estado = models.CharField(
        max_length=20,
        choices=[
            ("borrador", "Borrador"),
            ("publicado", "Publicado"),
            ("archivado", "Archivado"),
        ],
        blank=True,
    )
    requisitos = models.TextField(blank=True)
    destacado = models.BooleanField(default=False)
    instructor = models.ForeignKey(
        Instructor, on_delete=models.SET_NULL, null=True, blank=True
    )
    estudiantes = models.ManyToManyField(Estudiante, through="Inscripcion")
    imagen = models.ImageField(
        upload_to="cursos/curso", default="cursos/curso/fallback.png", blank=True
    )

    def __str__(self):
        return self.nombre


class Inscripcion(models.Model):
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    fecha_inscripcion = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = "Inscripción"
        verbose_name_plural = "Inscripciones"
        constraints = [
            models.UniqueConstraint(
                fields=["estudiante", "curso"], name="inscripcion_unicidad"
            )
        ]

    def __str__(self):
        return self.estudiante.nombre + " se incribió en " + self.curso.nombre
