"""
Comando de gestión para crear los grupos de usuarios con sus permisos.
"""

from django.core.management.base import BaseCommand

from users.permissions import create_groups_with_permissions


class Command(BaseCommand):
    help = "Crea los grupos de usuarios y les asigna los permisos predefinidos"

    def handle(self, *args, **options):
        self.stdout.write("Creando grupos de usuarios...")
        create_groups_with_permissions()
        self.stdout.write(
            self.style.SUCCESS("Grupos creados exitosamente")
        )
