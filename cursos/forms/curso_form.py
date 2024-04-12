from django import forms
from ..models import Curso, Instructor, Categoria


class CursoForm(forms.ModelForm):
    instructor = forms.ModelChoiceField(
        queryset=Instructor.objects.all(),
        required=False,
        empty_label="Seleccione el profesor",
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    categoria = forms.ModelChoiceField(
        queryset=Categoria.objects.all(),
        required=False,
        empty_label="Seleccione la categoría",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    class Meta:
        model = Curso
        fields = [
            "nombre",
            "descripcion",
            "precio",
            "fecha_publicacion",
            "instructor",
            "categoria",
            "duracion",
            "estado",
            "destacado",
            "imagen",
        ]
        labels = {
            "nombre": "Nombre del curso",
            "descripcion": "Descripción",
            "precio": "Precio",
            "fecha_publicacion": "Fecha de publicación",
            "instructor": "Instructor",
            "categoria": "Categoría",
            "duracion": "Duración",
            "estado": "Estado",
            "destacado": "Destacado",
            "imagen": "Imagen del curso",
        }
        widgets = {
            "nombre": forms.TextInput(
                attrs={
                    "placeholder": "Ingrese nombre del curso",
                    "class": "form-control",
                }
            ),
            "descripcion": forms.Textarea(
                attrs={"placeholder": "Ingrese la descripción", "class": "form-control"}
            ),
            "precio": forms.NumberInput(
                attrs={"placeholder": "Ingrese el precio", "class": "form-control"}
            ),
            "fecha_publicacion": forms.NumberInput(
                attrs={
                    "type": "date",
                    "placeholder": "Ingrese la fecha",
                    "class": "form-control",
                }
            ),
            "duracion": forms.TimeInput(
                attrs={"placeholder": "Ingrese la duración", "class": "form-control"}
            ),
            "estado": forms.Select(attrs={"class": "form-control"}),
            "destacado": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "imagen": forms.FileInput(attrs={"class": "form-control"}),
        }
