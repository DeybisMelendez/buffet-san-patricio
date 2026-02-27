"""
Migración para actualizar permisos según las nuevas especificaciones:
- Supervisor: sin acceso a Gestión del Menú (Productos, Categorías, Áreas de Despacho)
- Cajero: acceso limitado a mesas, comandas, pagos, ingresos de ingredientes y reportes
- Cocinero: acceso a mesas (solo ver comandas), inventario (solo ver)
- Administrador: mantiene todos los permisos
"""

from django.db import migrations


def update_group_permissions(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    Permission = apps.get_model("auth", "Permission")

    # Definición de permisos por grupo (codename sin app)
    group_permissions = {
        "Supervisor": [
            # Inventario completo
            "view_ingredient",
            "change_ingredient",
            "view_ingredientmovement",
            "add_ingredientmovement",
            "change_ingredientmovement",
            "delete_ingredientmovement",
            # Productos (solo ver, no gestionar)
            "view_product",
            "view_productcategory",
            "view_dispatcharea",
            "view_warehouse",
            "view_productingredient",
            # Órdenes y mesas
            "view_table",
            "view_order",
            "view_orderitem",
            "add_order",
            "change_order",
            "delete_order",
            "add_orderitem",
            "change_orderitem",
            "delete_orderitem",
        ],
        "Cocinero": [
            # Mesas y órdenes (solo ver)
            "view_table",
            "view_order",
            "view_orderitem",
            # Productos e ingredientes (solo ver)
            "view_product",
            "view_productcategory",
            "view_dispatcharea",
            "view_warehouse",
            "view_ingredient",
            "view_productingredient",
            "view_ingredientmovement",
        ],
        "Cajero": [
            # Mesas y órdenes
            "view_table",
            "add_order",
            "change_order",  # Para marcar como pagado
            "view_order",
            "view_orderitem",
            # Productos (para crear órdenes y reportes)
            "view_product",
            # Ingredientes (solo registrar ingresos)
            "view_ingredient",
            "add_ingredientmovement",
            "view_ingredientmovement",
        ],
        # Nota: Servicio y Administrador mantienen permisos actuales
    }

    # Actualizar permisos para cada grupo especificado
    for group_name, perm_codenames in group_permissions.items():
        try:
            group = Group.objects.get(name=group_name)
        except Group.DoesNotExist:
            continue

        permissions = []
        for codename in perm_codenames:
            # Determinar app_label
            if codename in [
                "add_user",
                "change_user",
                "delete_user",
                "view_user",
                "add_group",
                "change_group",
                "delete_group",
                "view_group",
            ]:
                app_label = "auth"
            else:
                app_label = "orders"
            try:
                perm = Permission.objects.get(
                    codename=codename, content_type__app_label=app_label
                )
                permissions.append(perm)
            except Permission.DoesNotExist:
                # Si no existe el permiso, ignorar
                pass

        group.permissions.set(permissions)
        group.save()


def reverse_update(apps, schema_editor):
    """Revierte a los permisos originales (no implementado completamente)."""
    # En una reversión completa, se restaurarían los permisos originales
    # Pero como no tenemos backup, dejamos vacío o podríamos recargar desde 0002
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_update_groups_permissions"),
    ]

    operations = [
        migrations.RunPython(update_group_permissions, reverse_update),
    ]
