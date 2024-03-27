from django.contrib import admin

from .models import Curso, Instructor, Estudiante, Categoria, Inscripcion


@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "precio", "fecha_publicacion", "categoria", "instructor")
    search_fields = ("nombre", "descripcion", "categoria__nombre", "instructor__nombre")
    list_filter = ("categoria", "estado", "fecha_publicacion")
    ordering = ("nombre", "precio", "fecha_publicacion")
    fieldsets = (
        (
            "Información general",
            {"fields": ("nombre", "descripcion", "precio", "fecha_publicacion")},
        ),
        (
            "Detalles del curso",
            {"fields": ("categoria", "instructor", "duracion", "estado")},
        ),
    )


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "color")
    search_fields = ("nombre",)


@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ("nombre", "bio")
    search_fields = ("nombre",)


@admin.register(Estudiante)
class EstudianteAdmin(admin.ModelAdmin):
    list_display = ("nombre", "email")
    search_fields = ("nombre", "email")
    ordering = ("nombre", "email")
    fieldsets = (
        (
            "Información general",
            {"fields": ("nombre", "email")},
        ),
    )


admin.site.register(Inscripcion)
