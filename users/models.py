"""
Modelos para gestión de roles y permisos configurables.
"""

from django.contrib.auth.models import Group, Permission
from django.db import models


class Role(models.Model):
    """
    Rol configurable con permisos personalizados.
    Sincroniza con Django Groups para compatibilidad con el sistema de auth.
    """

    name = models.CharField(
        max_length=150,
        unique=True,
        verbose_name="Nombre del rol",
    )
    description = models.TextField(
        blank=True,
        verbose_name="Descripción",
    )
    permissions = models.ManyToManyField(
        Permission,
        blank=True,
        verbose_name="Permisos",
        related_name="roles",
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Activo",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Rol"
        verbose_name_plural = "Roles"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)

        if is_new:
            Group.objects.get_or_create(name=self.name)

        group, _ = Group.objects.get_or_create(name=self.name)
        group.permissions.set(self.permissions.all())
        group.name = self.name
        group.save()

    def delete(self):
        self.is_active = False
        self.save()

        try:
            group = Group.objects.get(name=self.name)
            group.delete()
        except Group.DoesNotExist:
            pass

    def hard_delete(self):
        super().delete()
        try:
            group = Group.objects.get(name=self.name)
            group.delete()
        except Group.DoesNotExist:
            pass

    @classmethod
    def sync_all_with_groups(cls):
        """Sincroniza todos los roles activos con sus grupos correspondientes."""
        for role in cls.objects.filter(is_active=True):
            role.save()

    @classmethod
    def get_all_permissions(cls):
        """Devuelve todos los permisos disponibles agrupados por modelo."""
        from orders.models import (
            CashRegister, DispatchArea, FoodRecipe, FoodRecipeItem,
            Ingredient, IngredientMovement, Invoice, InvoiceItem,
            Order, OrderItem, Product, ProductCategory, ProductIngredient,
            Table, Warehouse
        )

        app_models = {
            "orders": [
                ("Table", ["view_table", "add_table", "change_table", "delete_table"]),
                ("ProductCategory", ["view_productcategory", "add_productcategory", "change_productcategory", "delete_productcategory"]),
                ("DispatchArea", ["view_dispatcharea", "add_dispatcharea", "change_dispatcharea", "delete_dispatcharea"]),
                ("Warehouse", ["view_warehouse", "add_warehouse", "change_warehouse", "delete_warehouse"]),
                ("Product", ["view_product", "add_product", "change_product", "delete_product"]),
                ("Ingredient", ["view_ingredient", "add_ingredient", "change_ingredient", "delete_ingredient"]),
                ("ProductIngredient", ["view_productingredient", "add_productingredient", "change_productingredient", "delete_productingredient"]),
                ("IngredientMovement", ["view_ingredientmovement", "add_ingredientmovement", "change_ingredientmovement", "delete_ingredientmovement"]),
                ("Order", ["view_order", "add_order", "change_order", "delete_order"]),
                ("OrderItem", ["view_orderitem", "add_orderitem", "change_orderitem", "delete_orderitem"]),
                ("Invoice", ["view_invoice", "add_invoice", "change_invoice", "delete_invoice"]),
                ("InvoiceItem", ["view_invoiceitem", "add_invoiceitem", "change_invoiceitem", "delete_invoiceitem"]),
                ("CashRegister", ["view_cashregister", "add_cashregister", "change_cashregister", "delete_cashregister"]),
                ("FoodRecipe", ["view_foodrecipe", "add_foodrecipe", "change_foodrecipe", "delete_foodrecipe"]),
                ("FoodRecipeItem", ["view_foodrecipeitem", "add_foodrecipeitem", "change_foodrecipeitem", "delete_foodrecipeitem"]),
            ],
            "auth": [
                ("User", ["view_user", "add_user", "change_user", "delete_user"]),
                ("Group", ["view_group", "add_group", "change_group", "delete_group"]),
            ],
        }

        all_permissions = {}
        for app_label, models_list in app_models.items():
            for model_name, codenames in models_list:
                perms = []
                for codename in codenames:
                    try:
                        perm = Permission.objects.get(codename=codename, content_type__app_label=app_label)
                        perms.append(perm)
                    except Permission.DoesNotExist:
                        pass
                if perms:
                    all_permissions[f"{app_label}.{model_name}"] = perms

        return all_permissions
