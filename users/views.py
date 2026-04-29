"""
Vistas para gestión de usuarios y roles.
"""

from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group, User
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from users.forms import RoleAssignForm, RoleForm, UserCreateForm, UserEditForm
from users.models import Role
from users.utils import is_admin


@login_required
@user_passes_test(is_admin)
def role_list(request):
    """Lista todos los roles con sus permisos y usuarios asignados."""
    roles = Role.objects.filter(is_active=True).order_by("name")
    roles_data = []
    for role in roles:
        try:
            group = Group.objects.get(name=role.name)
            users = User.objects.filter(groups=group).order_by("username")
            permissions = role.permissions.all().order_by("codename")
        except Group.DoesNotExist:
            users = []
            permissions = []

        roles_data.append(
            {
                "role": role,
                "users": users,
                "user_count": users.count(),
                "permissions": permissions,
            }
        )
    return render(request, "users/role_list.html", {"roles_data": roles_data})


@login_required
@user_passes_test(is_admin)
def role_create(request):
    """Crea un nuevo rol."""
    if request.method == "POST":
        form = RoleForm(request.POST)
        if form.is_valid():
            role = form.save()
            messages.success(request, f"✅ Rol '{role.name}' creado exitosamente.")
            return redirect("role_list")
    else:
        form = RoleForm()

    return render(
        request,
        "users/role_form.html",
        {"form": form, "title": "Crear Rol", "submit_label": "Crear Rol"},
    )


@login_required
@user_passes_test(is_admin)
def role_edit(request, role_id):
    """Edita un rol existente."""
    role = get_object_or_404(Role, id=role_id, is_active=True)

    if request.method == "POST":
        form = RoleForm(request.POST, instance=role)
        if form.is_valid():
            role = form.save()
            messages.success(request, f"✅ Rol '{role.name}' actualizado exitosamente.")
            return redirect("role_list")
    else:
        form = RoleForm(instance=role)

    return render(
        request,
        "users/role_form.html",
        {"form": form, "title": "Editar Rol", "submit_label": "Guardar Cambios", "role": role},
    )


@login_required
@user_passes_test(is_admin)
@require_http_methods(["POST"])
def role_delete(request, role_id):
    """Elimina (soft delete) un rol."""
    role = get_object_or_404(Role, id=role_id, is_active=True)
    role_name = role.name

    user_count = User.objects.filter(groups__name=role.name).count()
    if user_count > 0:
        messages.error(
            request,
            f"⚠️ No se puede eliminar el rol '{role_name}' porque tiene {user_count} usuario(s) asignado(s). "
            f"Primero reasigne los usuarios a otro rol.",
        )
        return redirect("role_list")

    role.delete()
    messages.success(request, f"✅ Rol '{role_name}' eliminado exitosamente.")
    return redirect("role_list")


@login_required
@user_passes_test(is_admin)
def role_assign(request):
    """Asigna usuarios a roles."""
    if request.method == "POST":
        form = RoleAssignForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(
                request, f"✅ Usuario '{user.username}' asignado a roles exitosamente."
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
