from django.contrib import admin

from .models import (CashRegister, DispatchArea, FoodRecipe, FoodRecipeItem,
                     Ingredient, IngredientMovement, Invoice, InvoiceItem,
                     Order, OrderItem, Product, ProductCategory,
                     ProductIngredient, Purchase, PurchaseItem, RecipeExecutionReport,
                     Supplier, Table, Warehouse)


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(DispatchArea)
class DispatchAreaAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


class ProductIngredientInline(admin.TabularInline):
    model = ProductIngredient
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "dispatch_area", "price")
    search_fields = ("name",)
    list_filter = ("category",)
    inlines = [ProductIngredientInline]


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ("name", "stock_quantity", "unit")
    list_filter = ("unit",)
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(ProductIngredient)
class ProductIngredientAdmin(admin.ModelAdmin):
    list_display = ("product", "ingredient", "quantity")
    list_filter = ("product", "ingredient")
    search_fields = ("product__name", "ingredient__name")


@admin.register(IngredientMovement)
class IngredientMovementAdmin(admin.ModelAdmin):
    list_display = ("ingredient", "quantity", "reason", "user", "created_at")
    list_filter = ("ingredient", "user", "created_at")
    search_fields = ("ingredient__name", "reason", "user__username")
    ordering = ("-created_at",)
    readonly_fields = ("created_at",)

    def save_model(self, request, obj, form, change):
        """Asigna automáticamente el usuario que realiza el movimiento."""
        if not obj.user:
            obj.user = request.user
        super().save_model(request, obj, form, change)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "table", "is_paid", "created_at", "get_total_display")
    list_filter = ("is_paid", "created_at", "table")
    date_hierarchy = "created_at"
    inlines = [OrderItemInline]

    def get_total_display(self, obj):
        return f"C${obj.get_total():,.2f}"

    get_total_display.short_description = "Total"


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("order", "product", "quantity", "get_total_display")
    list_filter = ("order__is_paid", "product")
    search_fields = ("product__name", "order__id")

    def get_total_display(self, obj):
        return f"C${obj.get_total():,.2f}"

    get_total_display.short_description = "Subtotal"


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ("name", "contact_name", "phone", "is_deleted")
    search_fields = ("name", "contact_name", "phone")
    list_filter = ("is_deleted",)


class PurchaseItemInline(admin.TabularInline):
    model = PurchaseItem
    extra = 1


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "supplier",
        "warehouse",
        "purchase_type",
        "total_amount",
        "status",
        "created_at",
    )
    search_fields = ("supplier__name", "reference_number")
    list_filter = ("status", "purchase_type", "created_at")
    inlines = [PurchaseItemInline]
    readonly_fields = ("created_at",)


class FoodRecipeItemInline(admin.TabularInline):
    model = FoodRecipeItem
    extra = 1


@admin.register(FoodRecipe)
class FoodRecipeAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "is_active", "created_at")
    search_fields = ("name", "description")
    list_filter = ("is_active",)
    inlines = [FoodRecipeItemInline]
    readonly_fields = ("created_at",)


@admin.register(FoodRecipeItem)
class FoodRecipeItemAdmin(admin.ModelAdmin):
    list_display = ("recipe", "ingredient", "quantity", "is_input")
    list_filter = ("recipe", "is_input")
    search_fields = ("recipe__name", "ingredient__name")


@admin.register(RecipeExecutionReport)
class RecipeExecutionReportAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "recipe",
        "quantity_produced",
        "is_manual",
        "created_by",
        "created_at",
    )
    list_filter = ("is_manual", "created_at", "recipe")
    search_fields = ("notes",)
    readonly_fields = ("created_at",)


class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
    extra = 1


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = (
        "invoice_number",
        "table",
        "total",
        "payment_type",
        "cashier",
        "payment_date",
        "is_active",
        "created_at",
    )
    list_filter = ("payment_type", "is_active", "created_at", "table")
    date_hierarchy = "created_at"
    search_fields = ("invoice_number", "table__name")
    inlines = [InvoiceItemInline]
    readonly_fields = ("created_at",)


@admin.register(InvoiceItem)
class InvoiceItemAdmin(admin.ModelAdmin):
    list_display = ("invoice", "product", "quantity", "unit_price", "total")
    list_filter = ("product",)
    search_fields = ("invoice__invoice_number", "product__name")


@admin.register(CashRegister)
class CashRegisterAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "date",
        "opening_amount",
        "total_sales",
        "total_contado",
        "get_status_display",
        "get_difference_display",
        "closing_time",
    )
    list_filter = ("date", "closing_time")
    date_hierarchy = "created_at"
    search_fields = ("user__username",)
    readonly_fields = (
        "created_at",
        "total_sales",
        "total_contado",
        "total_tarjeta_credito",
        "total_tarjeta_debito",
        "total_transferencia",
        "total_otros",
        "total_pendiente",
    )

    def get_difference_display(self, obj):
        diff = obj.get_difference()
        if diff is None:
            return "-"
        return f"C${diff:,.2f}"

    get_difference_display.short_description = "Diferencia"
