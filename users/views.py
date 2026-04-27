"""
Vistas para gestión de usuarios y roles.
"""

from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group, User
from django.shortcuts import get_object_or_404, redirect, render

from users.forms import RoleAssignForm, UserCreateForm, UserEditForm
from users.permissions import ALL_GROUPS
from users.utils import is_admin


@login_required
@user_passes_test(is_admin)
def role_list(request):
    """Lista todos los roles con sus permisos y usuarios asignados."""
    groups_data = []
    for group_name in ALL_GROUPS:
        group = Group.objects.filter(name=group_name).first()
        if group:
            users = User.objects.filter(groups=group).order_by("username")
            permissions = group.permissions.all().order_by("codename")
            groups_data.append(
                {
                    "group": group,
                    "users": users,
                    "user_count": users.count(),
                    "permissions": permissions,
                }
            )
    return render(request, "users/role_list.html", {"groups_data": groups_data})


@login_required
@user_passes_test(is_admin)
def role_assign(request):
    """Asigna usuarios a roles."""
    if request.method == "POST":
        form = RoleAssignForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data["user"]
            roles = form.cleaned_data["roles"]
            user.groups.set(roles)
            role_names = ", ".join([r.name for r in roles])
            messages.success(
                request, f"✅ Usuario '{user.username}' asignado a roles: {role_names}."
            )
            return redirect("role_list")
    else:
        form = RoleAssignForm()

    return render(
        request,
        "users/role_assign.html",
        {"form": form, "title": "Asignar Roles a Usuario"},
    )


@login_required
@user_passes_test(is_admin)
def user_list(request):
    """Lista todos los usuarios con sus grupos."""
    users = User.objects.all().order_by("username").prefetch_related("groups")
    return render(request, "users/user_list.html", {"users": users})


@login_required
@user_passes_test(is_admin)
def user_create(request):
    """Crea un nuevo usuario."""
    if request.method == "POST":
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(
                request, f"✅ Usuario '{user.username}' creado exitosamente."
            )
            return redirect("user_list")
    else:
        form = UserCreateForm()

    return render(
        request,
        "users/user_form.html",
        {"form": form, "title": "Crear Usuario", "submit_label": "Crear Usuario"},
    )


@login_required
@user_passes_test(is_admin)
def user_edit(request, user_id):
    """Edita un usuario existente."""
    user = get_object_or_404(User, id=user_id)

    if request.method == "POST":
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save()
            messages.success(
                request, f"✅ Usuario '{user.username}' actualizado exitosamente."
            )
            return redirect("user_list")
    else:
        form = UserEditForm(instance=user)

    return render(
        request,
        "users/user_form.html",
        {
            "form": form,
            "title": "Editar Usuario",
            "submit_label": "Guardar Cambios",
            "user": user,
        },
    )
