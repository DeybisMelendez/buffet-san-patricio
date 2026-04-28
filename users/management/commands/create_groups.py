"""
Comando de gestión para crear los grupos de usuarios y sincronizar roles.
"""

from django.core.management.base import BaseCommand

from users.models import Role
from users.permissions import ALL_GROUPS, GROUP_PERMISSIONS, create_groups_with_permissions


class Command(BaseCommand):
    help = "Crea los grupos de usuarios y sincroniza los Roles con sus permisos"

    def add_arguments(self, parser):
        parser.add_argument(
            "--with-roles",
            action="store_true",
            help="También crea roles en el modelo Role basado en los grupos hardcoded",
        )

    def handle(self, *args, **options):
        self.stdout.write("Creando grupos de usuarios...")
        create_groups_with_permissions()
        self.stdout.write(
            self.style.SUCCESS("Grupos creados exitosamente")
        )

        if options["with_roles"]:
            self.stdout.write("Sincronizando Roles...")
            self._sync_roles()
            self.stdout.write(
                self.style.SUCCESS("Roles sincronizados exitosamente")
            )

    def _sync_roles(self):
        """Crea o actualiza Roles basándose en los grupos hardcoded."""
        for group_name in ALL_GROUPS:
            perms_codenames = GROUP_PERMISSIONS.get(group_name, [])

            role, created = Role.objects.get_or_create(
                name=group_name,
                defaults={"description": f"Rol sincronizado desde {group_name}"}
            )

            from django.contrib.auth.models import Permission
            from django.db.models import Q

            query = Q()
            for perm_codename in perms_codenames:
                if perm_codename in ["view_user", "add_user", "change_user", "delete_user",
                                     "view_group", "add_group", "change_group", "delete_group"]:
                    query |= Q(codename=perm_codename, content_type__app_label="auth")
                else:
                    query |= Q(codename=perm_codename, content_type__app_label="orders")

            permissions = Permission.objects.filter(query)
            role.permissions.set(permissions)
            role.save()

            action = "Creado" if created else "Actualizado"
            self.stdout.write(f"  {action} rol: {group_name} ({permissions.count()} permisos)")
