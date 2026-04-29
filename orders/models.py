from decimal import Decimal

from django.db import models
from django.utils import timezone


class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class AllObjectsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()


class SoftDeleteModel(models.Model):
    is_deleted = models.BooleanField(default=False, verbose_name="Eliminado")
    deleted_at = models.DateTimeField(
        null=True, blank=True, verbose_name="Fecha de eliminación"
    )

    objects = SoftDeleteManager()
    all_objects = AllObjectsManager()

    def soft_delete(self):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()

    def restore(self):
        self.is_deleted = False
        self.deleted_at = None
        self.save()

    class Meta:
        abstract = True


class Table(SoftDeleteModel):
    name = models.CharField(max_length=100, unique=True, verbose_name="Nombre")

    def __str__(self):
        return f"Mesa {self.name}"


class ProductCategory(SoftDeleteModel):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class DispatchArea(SoftDeleteModel):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Warehouse(SoftDeleteModel):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Product(SoftDeleteModel):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(
        ProductCategory, on_delete=models.SET_NULL, null=True, blank=True
    )
    dispatch_area = models.ForeignKey(
        DispatchArea, on_delete=models.SET_NULL, null=True, blank=True
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class Ingredient(SoftDeleteModel):
    INGREDIENT_TYPES = [
        ("MATERIA_PRIMA", "Materia Prima"),
        ("PROCESADO", "Procesado"),
    ]

    UNITS = [
        ("oz", "Onzas"),
        ("lb", "Libras"),
        ("g", "Gramos"),
        ("kg", "Kilogramos"),
        ("ml", "Mililitros"),
        ("l", "Litros"),
        ("und", "Unidades"),
    ]

    name = models.CharField(max_length=255, unique=True, verbose_name="Nombre")
    ingredient_type = models.CharField(
        max_length=20,
        choices=INGREDIENT_TYPES,
        default="MATERIA_PRIMA",
        verbose_name="Tipo",
    )
    stock_quantity = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, verbose_name="Cantidad"
    )
    unit = models.CharField(
        max_length=10, choices=UNITS, default="und", verbose_name="Unidad"
    )
    warehouse = models.ForeignKey(
        Warehouse, on_delete=models.SET_NULL, null=True, blank=True
    )

    def add_stock(self, amount):
        self.stock_quantity += Decimal(amount)
        self.save()

    def __str__(self):
        return f"{self.name} ({self.stock_quantity} {self.unit})"

    def name_with_unit(self):
        return f"{self.name} ({self.unit})"


class ProductIngredient(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = [["product", "ingredient"]]
        verbose_name = "Receta"
        verbose_name_plural = "Recetas"

    def __str__(self):
        return (
            f"{self.quantity} {self.ingredient.unit} de {self.ingredient.name} "
            f"para {self.product.name}"
        )


class FoodRecipe(SoftDeleteModel):
    name = models.CharField(max_length=255, unique=True, verbose_name="Nombre")
    description = models.TextField(blank=True, default="", verbose_name="Descripción")
    is_active = models.BooleanField(default=True, verbose_name="Activo")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Receta de Conversión"
        verbose_name_plural = "Recetas de Conversión"

    def __str__(self):
        return self.name


class FoodRecipeItem(models.Model):
    recipe = models.ForeignKey(
        FoodRecipe, on_delete=models.CASCADE, related_name="items"
    )
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    is_input = models.BooleanField(
        default=True,
        verbose_name="Es entrada",
        help_text="Si marcada = consumo (salida de inventario). Si desmarcada = producto procesado (entrada a inventario).",
    )

    class Meta:
        verbose_name = "Ingrediente de Receta"
        verbose_name_plural = "Ingredientes de Receta"

    def __str__(self):
        tipo = "Entrada" if self.is_input else "Salida"
        return f"{self.quantity} {self.ingredient.unit} {self.ingredient.name} ({tipo})"


class RecipeExecutionReport(models.Model):
    recipe = models.ForeignKey(
        "FoodRecipe", on_delete=models.SET_NULL, null=True, blank=True
    )
    is_manual = models.BooleanField(default=False, verbose_name="Conversión manual")
    quantity_produced = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, verbose_name="Cantidad producida"
    )
    raw_materials_used = models.JSONField(
        default=list, verbose_name="Materiales consumidos"
    )
    products_created = models.JSONField(
        default=list, verbose_name="Productos creados"
    )
    notes = models.TextField(blank=True, default="", verbose_name="Notas")
    created_by = models.ForeignKey(
        "auth.User", on_delete=models.SET_NULL, null=True, related_name="conversions"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Reporte de Conversión"
        verbose_name_plural = "Reportes de Conversión"
        ordering = ["-created_at"]

    def __str__(self):
        recipe_name = self.recipe.name if self.recipe else "Manual"
        return f"Conversión #{self.id} - {recipe_name} ({self.created_at.strftime('%d/%m/%Y %H:%M')})"


class IngredientMovement(models.Model):
    ingredient = models.ForeignKey("Ingredient", on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    reason = models.CharField(max_length=255, blank=True, null=True)
    user = models.ForeignKey(
        "auth.User", on_delete=models.SET_NULL, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def apply_movement(self):
        self.ingredient.add_stock(self.quantity)

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new:
            self.apply_movement()

    def __str__(self):
        tipo = "Ingreso" if self.quantity >= 0 else "Salida"
        return (
            f"{tipo}: {self.quantity} {self.ingredient.unit} de {self.ingredient.name}"
        )


class Order(models.Model):
    table = models.ForeignKey(Table, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey("auth.User", on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)

    def get_status_display(self):
        return "Pagada" if self.is_paid else "Pendiente"

    def get_total(self):
        return sum(item.get_total() for item in self.orderitem_set.all())

    def __str__(self):
        return f"Orden {self.id} - {self.table.name if self.table else 'Sin mesa'}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def get_total(self):
        return self.quantity * self.product.price

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        for prod_ing in ProductIngredient.objects.filter(product=self.product):
            total_required = prod_ing.quantity * Decimal(self.quantity)

            IngredientMovement.objects.create(
                ingredient=prod_ing.ingredient,
                quantity=-total_required,
                user=self.order.user,
                reason=f"Uso en {self.product.name}, Comanda #{self.order.id}",
            )

    def __str__(self):
        return f"{self.quantity} x {self.product.name} (Comanda #{self.order.id})"


# ==========================
# 🧾 FACTURACIÓN
# ==========================


class Invoice(models.Model):
    PAYMENT_TYPES = [
        ("EFECTIVO", "Efectivo"),
        ("TARJETA_CREDITO", "Tarjeta Crédito"),
        ("TARJETA_DEBITO", "Tarjeta Débito"),
        ("TRANSFERENCIA", "Transferencia"),
        ("OTRO", "Otro"),
        ("PENDIENTE", "Pendiente"),
    ]

    invoice_number = models.PositiveIntegerField(unique=True)
    table = models.ForeignKey(Table, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(
        "auth.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="invoices_created",
    )
    cashier = models.ForeignKey(
        "auth.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="invoices_cashed",
    )
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_type = models.CharField(
        max_length=20, choices=PAYMENT_TYPES, default="PENDIENTE"
    )
    amount_received = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Monto recibido",
    )
    payment_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Fecha de pago",
    )
    notes = models.TextField(
        blank=True,
        default="",
        verbose_name="Notas",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.invoice_number:
            last_invoice = Invoice.objects.order_by("-invoice_number").first()
            self.invoice_number = (
                (last_invoice.invoice_number + 1) if last_invoice else 1
            )
        super().save(*args, **kwargs)

    @property
    def change_amount(self):
        if self.payment_type == "EFECTIVO" and self.amount_received is not None:
            return self.amount_received - self.total
        return None

    def get_items(self):
        return self.invoiceitem_set.select_related("product")

    def __str__(self):
        return f"Factura #{self.invoice_number}"


class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        self.total = self.quantity * self.unit_price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"


# ==========================
# 💰 ARQUEO DE CAJA
# ==========================


class CashRegister(models.Model):
    user = models.ForeignKey("auth.User", on_delete=models.SET_NULL, null=True)
    date = models.DateField(auto_now_add=True)
    opening_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    closing_amount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    total_sales = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_contado = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_tarjeta_credito = models.DecimalField(
        max_digits=10, decimal_places=2, default=0
    )
    total_tarjeta_debito = models.DecimalField(
        max_digits=10, decimal_places=2, default=0
    )
    total_transferencia = models.DecimalField(
        max_digits=10, decimal_places=2, default=0
    )
    total_otros = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_pendiente = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    closing_time = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def get_status_display(self):
        return "Cerrado" if self.closing_time else "Abierto"

    def get_expected_cash(self):
        if self.closing_time:
            return self.opening_amount + self.total_contado
        return None

    def get_difference(self):
        if self.closing_amount is not None:
            expected = self.opening_amount + self.total_contado
            return self.closing_amount - expected
        return None

    @staticmethod
    def get_active():
        return CashRegister.objects.filter(closing_time__isnull=True).first()

    def __str__(self):
        return f"Arqueo #{self.id} - {self.date} ({self.get_status_display()})"


# ==========================
# 🛒 COMPRAS DE INGREDIENTES
# ==========================


class Supplier(SoftDeleteModel):
    name = models.CharField(max_length=255, unique=True, verbose_name="Nombre")
    contact_name = models.CharField(
        max_length=255, blank=True, default="", verbose_name="Persona de contacto"
    )
    phone = models.CharField(
        max_length=20, blank=True, default="", verbose_name="Teléfono"
    )
    email = models.EmailField(blank=True, default="", verbose_name="Correo electrónico")
    address = models.TextField(blank=True, default="", verbose_name="Dirección")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Purchase(models.Model):
    PURCHASE_TYPE_CHOICES = [
        ("CREDIT", "Crédito"),
        ("CASH", "Contado"),
    ]
    STATUS_CHOICES = [
        ("ACTIVE", "Activa"),
        ("COMPLETED", "Completada"),
        ("CANCELED", "Cancelada"),
    ]

    supplier = models.ForeignKey(
        Supplier, on_delete=models.PROTECT, verbose_name="Proveedor"
    )
    warehouse = models.ForeignKey(
        Warehouse, on_delete=models.PROTECT, verbose_name="Bodega"
    )
    purchase_type = models.CharField(
        max_length=10,
        choices=PURCHASE_TYPE_CHOICES,
        default="CASH",
        verbose_name="Tipo de compra",
    )
    order_date = models.DateField(null=True, blank=True, verbose_name="Fecha de orden")
    reference_number = models.CharField(
        max_length=50, blank=True, default="", verbose_name="Número de referencia"
    )
    subtotal = models.DecimalField(
        max_digits=12, decimal_places=2, default=0, verbose_name="Subtotal"
    )
    total_amount = models.DecimalField(
        max_digits=12, decimal_places=2, default=0, verbose_name="Total"
    )
    notes = models.TextField(blank=True, default="", verbose_name="Notas")
    status = models.CharField(
        max_length=15, choices=STATUS_CHOICES, default="ACTIVE", verbose_name="Estado"
    )
    created_by = models.ForeignKey(
        "auth.User",
        on_delete=models.SET_NULL,
        null=True,
        related_name="purchases_created",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Compra"
        verbose_name_plural = "Compras"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Compra #{self.id} - {self.supplier.name} ({self.order_date})"

    def mark_as_completed(self):
        self.status = "COMPLETED"
        self.save()

    def cancel(self):
        self.status = "CANCELED"
        self.save()


class PurchaseItem(models.Model):
    purchase = models.ForeignKey(
        Purchase, on_delete=models.CASCADE, related_name="items"
    )
    ingredient = models.ForeignKey(Ingredient, on_delete=models.PROTECT)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    class Meta:
        verbose_name = "Ítem de Compra"
        verbose_name_plural = "Ítems de Compra"

    def save(self, *args, **kwargs):
        self.subtotal = self.quantity * self.unit_cost
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantity} x {self.ingredient.name} @ C${self.unit_cost}"
