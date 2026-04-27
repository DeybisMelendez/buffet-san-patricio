"""
Definición de grupos y permisos fijos para el sistema Boa POS.

Los grupos son fijos (no configurables) y tienen permisos predefinidos.
"""

from django.contrib.auth.models import Permission

# ==========================
# 📋 NOMBRES DE GRUPOS
# ==========================

GROUP_SERVICIO = "Servicio"
GROUP_SUPERVISOR = "Supervisor"
GROUP_ADMINISTRADOR = "Administrador"
GROUP_COCINERO = "Cocinero"
GROUP_CAJERO = "Cajero"

ALL_GROUPS = [
    GROUP_SERVICIO,
    GROUP_SUPERVISOR,
    GROUP_ADMINISTRADOR,
    GROUP_COCINERO,
    GROUP_CAJERO,
]

# ==========================
# 🔐 PERMISOS POR GRUPO
# ==========================

# Permisos de solo lectura (view) para modelos básicos
VIEW_ONLY_PERMS = [
    "view_table",
    "view_productcategory",
    "view_dispatcharea",
    "view_warehouse",
    "view_product",
    "view_ingredient",
    "view_productingredient",
    "view_ingredientmovement",
    "view_order",
    "view_orderitem",
]

# Permisos de gestión completa (add, change, delete, view) para modelos de configuración
FULL_MANAGEMENT_PERMS = [
    "add_table",
    "change_table",
    "delete_table",
    "view_table",
    "add_productcategory",
    "change_productcategory",
    "delete_productcategory",
    "view_productcategory",
    "add_dispatcharea",
    "change_dispatcharea",
    "delete_dispatcharea",
    "view_dispatcharea",
    "add_warehouse",
    "change_warehouse",
    "delete_warehouse",
    "view_warehouse",
    "add_product",
    "change_product",
    "delete_product",
    "view_product",
    "add_ingredient",
    "change_ingredient",
    "delete_ingredient",
    "view_ingredient",
    "add_productingredient",
    "change_productingredient",
    "delete_productingredient",
    "view_productingredient",
    "add_ingredientmovement",
    "change_ingredientmovement",
    "delete_ingredientmovement",
    "view_ingredientmovement",
    "add_order",
    "change_order",
    "delete_order",
    "view_order",
    "add_orderitem",
    "change_orderitem",
    "delete_orderitem",
    "view_orderitem",
    # Facturación
    "add_invoice",
    "change_invoice",
    "delete_invoice",
    "view_invoice",
    "add_invoiceitem",
    "change_invoiceitem",
    "delete_invoiceitem",
    "view_invoiceitem",
    # Arqueo de caja
    "add_cashregister",
    "change_cashregister",
    "delete_cashregister",
    "view_cashregister",
    # Recetas de conversión
    "add_foodrecipe",
    "change_foodrecipe",
    "delete_foodrecipe",
    "view_foodrecipe",
]

# Permisos de usuario y grupo (solo administrador)
USER_GROUP_PERMS = [
    "add_user",
    "change_user",
    "delete_user",
    "view_user",
    "add_group",
    "change_group",
    "delete_group",
    "view_group",
]

# Mapeo de grupos a permisos (nombres de permisos sin la app)
GROUP_PERMISSIONS = {
    GROUP_SERVICIO: [
        "view_table",
        "view_productcategory",
        "view_dispatcharea",
        "view_warehouse",
        "view_product",
        "view_ingredient",
        "view_productingredient",
        "view_ingredientmovement",
        "view_order",
        "view_orderitem",
        "add_order",
        "change_order",
        "add_orderitem",
        "change_orderitem",
    ],
    GROUP_SUPERVISOR: [
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
        # Facturación
        "add_invoice",
        "view_invoice",
        # Arqueo de caja
        "add_cashregister",
        "view_cashregister",
        "change_cashregister",
        # Recetas de conversión
        "add_foodrecipe",
        "change_foodrecipe",
        "view_foodrecipe",
        # Reportes
        # Nota: Los reportes no tienen permisos específicos, se controlan por vistas
    ],
    GROUP_ADMINISTRADOR: FULL_MANAGEMENT_PERMS + USER_GROUP_PERMS,
    GROUP_COCINERO: [
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
        # Recetas de conversión
        "add_foodrecipe",
        "change_foodrecipe",
        "view_foodrecipe",
    ],
    GROUP_CAJERO: [
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
        # Facturación
        "add_invoice",
        "view_invoice",
        # Arqueo de caja
        "add_cashregister",
        "view_cashregister",
        "change_cashregister",
    ],
}

# ==========================
# 🛠️ FUNCIONES DE UTILIDAD
# ==========================


def get_group_permissions(group_name):
    """Devuelve la lista de permisos (nombres completos) para un grupo."""
    perms = GROUP_PERMISSIONS.get(group_name, [])
    # Añadir prefijo 'orders.' para permisos de la app orders
    # (excepto para permisos de auth)
    full_perms = []
    for perm in perms:
        if perm in USER_GROUP_PERMS:
            full_perms.append(f"auth.{perm}")
        else:
            full_perms.append(f"orders.{perm}")
    return full_perms


def create_groups_with_permissions():
    """Crea los grupos y les asigna los permisos definidos."""
    from django.contrib.auth.models import Group

    for group_name in ALL_GROUPS:
        group, created = Group.objects.get_or_create(name=group_name)
        perms = GROUP_PERMISSIONS.get(group_name, [])
        perm_objects = []
        for perm in perms:
            app_label = "auth" if perm in USER_GROUP_PERMS else "orders"
            try:
                perm_obj = Permission.objects.get(
                    codename=perm, content_type__app_label=app_label
                )
                perm_objects.append(perm_obj)
            except Permission.DoesNotExist:
                pass
        group.permissions.set(perm_objects)
        group.save()


def user_in_group(user, group_name):
    """Verifica si el usuario pertenece a un grupo específico."""
    return user.groups.filter(name=group_name).exists()


def user_has_permission(user, perm_codename, app_label="orders"):
    """Verifica si el usuario tiene un permiso específico."""
    if user.is_superuser:
        return True
    full_perm = f"{app_label}.{perm_codename}"
    return user.has_perm(full_perm)
