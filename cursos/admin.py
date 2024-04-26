from django.contrib import admin

from .models import Curso, Instructor, Estudiante, Categoria, Inscripcion
from tinymce.widgets import TinyMCE
from django.db.models import TextField
from django.utils.html import strip_tags
from .admin_forms import InstructorAdminForm
from django.template.defaultfilters import truncatechars
import html


@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "precio", "fecha_publicacion", "categoria", "instructor")
    search_fields = ("nombre", "descripcion", "categoria__nombre", "instructor__nombre")
    list_filter = ("categoria", "estado", "fecha_publicacion")
    ordering = ("nombre", "precio", "fecha_publicacion")
    fieldsets = (
        (
            "Información general",
            {
                "fields": (
                    "nombre",
                    "descripcion",
                    "precio",
                    "fecha_publicacion",
                    "contenido",
                )
            },
        ),
        (
            "Detalles del curso",
            {
                "fields": (
                    "categoria",
                    "instructor",
                    "duracion",
                    "estado",
                    "destacado",
                    "imagen",
                    "requisitos",
                )
            },
        ),
    )
    formfield_overrides = {
        TextField: {"widget": TinyMCE()},
    }


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "color")
    search_fields = ("nombre",)


@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    form = InstructorAdminForm

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # Reordenar los campos
        form.base_fields = dict(
            [
                ("username", form.base_fields["username"]),
                ("email", form.base_fields["email"]),
                ("firstname", form.base_fields["firstname"]),
                ("lastname", form.base_fields["lastname"]),
                ("password", form.base_fields["password"]),
            ]
            + list(form.base_fields.items())
        )
        return form

    list_display = (
        "get_username",
        "get_firstname",
        "get_lastname",
        "get_email",
        "get_truncated_bio",
    )

    def get_username(self, obj):
        return obj.user.username if obj.user else None

    get_username.short_description = "Nombre de usuario"

    def get_firstname(self, obj):
        return obj.user.first_name if obj.user else None

    get_firstname.short_description = "Nombre"

    def get_lastname(self, obj):
        return obj.user.last_name if obj.user else None

    get_lastname.short_description = "Apellido"

    def get_email(self, obj):
        return obj.user.email if obj.user else None

    get_email.short_description = "Email"

    def get_truncated_bio(self, obj):
        text = strip_tags(obj.bio)
        # Convertir entidades HTML a texto
        text = html.unescape(text)
        # Truncar a 50 caracteres
        return truncatechars(text, 50)

    get_truncated_bio.short_description = "Biografía"

    search_fields = (
        "user__username",
        "user__first_name",
        "user__last_name",
        "user__email",
    )
    list_filter = ("user__is_active",)
    ordering = (
        "user__username",
        "user__first_name",
        "user__last_name",
        "user__email",
    )


@admin.register(Estudiante)
class EstudianteAdmin(admin.ModelAdmin):
    list_display = ("nombre", "email")
    search_fields = ("nombre", "email")
    ordering = ("nombre", "email")
    fieldsets = (
        (
            "Información general",
            {"fields": ("nombre", "email", "avatar")},
        ),
    )


admin.site.register(Inscripcion)
