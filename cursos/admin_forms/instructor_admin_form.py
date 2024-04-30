from django import forms
from django.contrib.auth.models import User
from ..models import Instructor


class InstructorAdminForm(forms.ModelForm):
    username = forms.CharField(required=True, label="Usuario")
    email = forms.EmailField(required=True, label="Email")
    firstname = forms.CharField(required=False, label="Nombre")
    lastname = forms.CharField(required=False, label="Apellido")
    password = forms.CharField(
        required=False,
        label="Contraseña",
        widget=forms.PasswordInput,
        help_text="La contraseña no se muestra por seguridad",
    )
    # avatar = forms.ImageField(required=False, label="Avatar")

    def __init__(self, *args, **kwargs):
        super(InstructorAdminForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk and self.instance.user:
            self.fields["username"].initial = self.instance.user.username
            self.fields["email"].initial = self.instance.user.email
            self.fields["firstname"].initial = self.instance.user.first_name
            self.fields["lastname"].initial = self.instance.user.last_name
            self.fields["password"].required = False

    class Meta:
        model = Instructor
        fields = ["bio", "avatar"]

    def save(self, commit=True):
        instructor = super(InstructorAdminForm, self).save(commit=False)

        username = self.cleaned_data["username"]
        email = self.cleaned_data["email"]
        first_name = self.cleaned_data["firstname"]
        last_name = self.cleaned_data["lastname"]
        password = self.cleaned_data["password"]

        if self.instance.pk:  # Verifica si es una actualización
            user = self.instance.user

            # Intentar actualizar el nombre de usuario
            if user.username != username:
                # Comprobar si el nuevo nombre de usuario ya existe
                if User.objects.filter(username=username).exists():
                    self.add_error("username", "Este nombre de usuario ya está en uso.")
                    return None
                else:
                    user.username = username
            user.email = email
            user.first_name = first_name
            user.last_name = last_name
            if password:
                user.set_password(password)
            user.save()

            instructor.user = user
            if commit:
                instructor.save()
            return instructor
        else:
            # Comprobar si el nombre de usuario ya existe
            if User.objects.filter(username=username).exists():
                self.add_error("username", "Este nombre de usuario ya está en uso.")
                return None
            else:
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                )
                user.set_password(password)

                instructor.user = user
                if commit:
                    instructor.save()
                return instructor
