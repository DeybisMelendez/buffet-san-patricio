"""
Formularios para gestión de usuarios y roles.
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group, Permission, User

from users.models import Role


class RoleForm(forms.ModelForm):
    """Formulario para crear/editar un rol con sus permisos."""

    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.none(),
        required=False,
        label="Permisos",
        widget=forms.CheckboxSelectMultiple,
        help_text="Seleccione los permisos que tendrá este rol",
    )

    class Meta:
        model = Role
        fields = ["name", "description", "is_active", "permissions"]
        labels = {
            "name": "Nombre del rol",
            "description": "Descripción",
            "is_active": "Rol activo",
        }
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        all_perms = Role.get_all_permissions()
        grouped = []
        for model_label, perms in all_perms.items():
            model_name = model_label.split(".")[1]
            for perm in perms:
                grouped.append((perm.id, f"{model_name} - {perm.name} ({perm.codename})"))

        self.fields["permissions"].queryset = Permission.objects.filter(
            id__in=[p[0] for p in grouped]
        ).order_by("content_type__app_label", "content_type__model", "codename")

        for field_name, field in self.fields.items():
            if field_name == "is_active":
                field.widget.attrs.update({"class": "form-check-input"})
            elif field_name == "permissions":
                continue
            else:
                field.widget.attrs.update({"class": "form-control"})
                if field_name == "name":
                    field.widget.attrs.update({"placeholder": "Nombre del rol"})
                elif field_name == "description":
                    field.widget.attrs.update({"placeholder": "Descripción opcional del rol"})

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if name:
            name = name.strip()
            existing = Role.objects.filter(name__iexact=name)
            if self.instance.pk:
                existing = existing.exclude(pk=self.instance.pk)
            if existing.exists():
                raise forms.ValidationError("Ya existe un rol con este nombre.")
        return name

    def save(self, commit=True):
        role = super().save(commit=False)
        if commit:
            role.save()
            self.save_m2m()
        return role


class RoleAssignForm(forms.Form):
    """Formulario para asignar múltiples roles a un usuario."""

    user = forms.ModelChoiceField(
        queryset=User.objects.all().order_by("username"),
        required=True,
        label="Usuario",
        help_text="Seleccione el usuario al que desea asignar roles",
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    roles = forms.ModelMultipleChoiceField(
        queryset=Role.objects.filter(is_active=True).order_by("name"),
        required=True,
        label="Roles",
        widget=forms.CheckboxSelectMultiple,
        help_text="Seleccione uno o más roles para el usuario",
    )

    def save(self):
        user = self.cleaned_data["user"]
        roles = self.cleaned_data["roles"]
        user.groups.clear()
        for role in roles:
            group, _ = Group.objects.get_or_create(name=role.name)
            user.groups.add(group)
        return user


class UserCreateForm(UserCreationForm):
    """Formulario para crear un nuevo usuario."""

    first_name = forms.CharField(
        max_length=30,
        required=True,
        label="Nombre",
        widget=forms.TextInput(attrs={"placeholder": "Nombre", "class": "form-control"}),
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        label="Apellido",
        widget=forms.TextInput(attrs={"placeholder": "Apellido", "class": "form-control"}),
    )
    groups = forms.ModelChoiceField(
        queryset=Role.objects.filter(is_active=True).order_by("name"),
        required=True,
        label="Rol",
        help_text="Seleccione el rol del usuario",
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "groups",
            "password1",
            "password2",
        ]
        labels = {
            "username": "Nombre de usuario",
        }
        widgets = {
            "username": forms.TextInput(attrs={"placeholder": "Nombre de usuario", "class": "form-control"}),
            "password1": forms.PasswordInput(attrs={"class": "form-control"}),
            "password2": forms.PasswordInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
            role = self.cleaned_data["groups"]
            group, _ = Group.objects.get_or_create(name=role.name)
            user.groups.clear()
            user.groups.add(group)
        return user


class UserEditForm(forms.ModelForm):
    """Formulario para editar un usuario existente."""

    first_name = forms.CharField(max_length=30, required=True, label="Nombre")
    last_name = forms.CharField(max_length=30, required=True, label="Apellido")
    roles = forms.ModelMultipleChoiceField(
        queryset=Role.objects.filter(is_active=True).order_by("name"),
        required=True,
        label="Roles",
        widget=forms.CheckboxSelectMultiple,
    )
    password1 = forms.CharField(
        label="Nueva contraseña",
        widget=forms.PasswordInput,
        required=False,
        help_text="Deje vacío si no desea cambiar la contraseña.",
    )
    password2 = forms.CharField(
        label="Confirmar nueva contraseña",
        widget=forms.PasswordInput,
        required=False,
        help_text="Repita la nueva contraseña.",
    )

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "roles"]
        labels = {
            "username": "Nombre de usuario",
        }
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control", "readonly": "readonly"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            current_roles = Role.objects.filter(is_active=True, name__in=self.instance.groups.values_list("name", flat=True))
            self.initial["roles"] = list(current_roles)

        for field_name, field in self.fields.items():
            if field_name in ["roles"]:
                continue
            field.widget.attrs.update({"class": "form-control"})

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 or password2:
            if password1 != password2:
                raise forms.ValidationError("Las contraseñas no coinciden.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]

        password = self.cleaned_data.get("password1")
        if password:
            user.set_password(password)

        if commit:
            user.save()
            user.groups.clear()
            for role in self.cleaned_data["roles"]:
                group, _ = Group.objects.get_or_create(name=role.name)
                user.groups.add(group)
        return user
