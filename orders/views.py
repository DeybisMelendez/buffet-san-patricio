import csv
from datetime import datetime, time, timedelta
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import Count, F, Q, Sum
from django.forms import modelformset_factory
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from users.utils import (
    has_valid_role,
    user_can_add_inventory_movement,
    user_can_manage_inventory_full,
    user_can_manage_menu,
    user_can_mark_paid,
    user_can_view_inventory,
    user_can_view_reports,
    user_can_view_sales_report,
)

from .forms import ProductIngredientForm, TableForm
from .models import (
    CashRegister,
    Company,
    DispatchArea,
    Ingredient,
    IngredientMovement,
    Invoice,
    InvoiceItem,
    Order,
    OrderItem,
    Product,
    ProductCategory,
    ProductIngredient,
    Table,
    Warehouse,
)

# ==========================
# 🔐 UTILIDADES Y PERMISOS
# ==========================


def parse_date_range(request):
    """Obtiene el rango de fechas desde GET o usa el día actual."""
    date_format = "%Y-%m-%dT%H:%M"
    start_str = request.GET.get("start")
    end_str = request.GET.get("end")

    if start_str and end_str:
        start = datetime.strptime(start_str, date_format)
        end = datetime.strptime(end_str, date_format)
    else:
        today = datetime.today().date()
        start = datetime.combine(today, time.min)
        end = datetime.combine(today, time.max)
    return start, end


# ==========================
# 🪑 MESAS Y COMANDAS
# ==========================


@login_required
@user_passes_test(has_valid_role)
def table_list(request):
    """Muestra todas las mesas y su total pendiente."""
    tables = Table.objects.all().order_by("name")
    table_data = []
    for table in tables:
        total_due = (
            Order.objects.filter(table=table, is_paid=False)
            .annotate(
                order_total=Sum(
                    F("orderitem__quantity") * F("orderitem__product__price")
                )
            )
            .aggregate(total=Sum("order_total"))["total"]
            or 0
        )
        table_data.append({"table": table, "total_due": total_due})

    return render(request, "pos/table_list.html", {"table_data": table_data})


@login_required
@user_passes_test(has_valid_role)
def table_orders(request, table_id):
    """Lista de comandas activas de una mesa."""
    table = get_object_or_404(Table, id=table_id)
    orders = (
        Order.objects.filter(table=table, is_paid=False)
        .prefetch_related("orderitem_set__product")
        .order_by("-created_at")
    )
    return render(request, "pos/table_orders.html", {"table": table, "orders": orders})


@login_required
@user_passes_test(user_can_mark_paid)
def mark_table_paid(request, table_id):
    """Marca todas las órdenes no pagadas de una mesa como pagadas y genera factura."""
    table = get_object_or_404(Table, id=table_id)
    orders = Order.objects.filter(table=table, is_paid=False).prefetch_related(
        "orderitem_set__product"
    )

    if not orders.exists():
        messages.info(request, f" No hay comandas pendientes para {table.name}.")
        return redirect("table_list")

    with transaction.atomic():
        subtotal = Decimal("0")
        items_data = []

        for order in orders:
            for item in order.orderitem_set.all():
                line_total = item.quantity * item.product.price
                subtotal += line_total
                items_data.append(
                    {
                        "product": item.product,
                        "quantity": item.quantity,
                        "unit_price": item.product.price,
                        "total": line_total,
                    }
                )

        if not items_data:
            messages.warning(request, " No hay productos para facturar.")
            return redirect("table_orders", table_id=table.id)

        active_register = CashRegister.get_active()
        if not active_register:
            messages.error(
                request,
                " No hay una caja abierta. Abre un turno en 'Caja' antes de facturar.",
            )
            return redirect("table_orders", table_id=table.id)

        cashier = active_register.user

        invoice = Invoice.objects.create(
            table=table,
            user=request.user,
            cashier=cashier,
            subtotal=subtotal,
            total=subtotal,
            payment_method="CONTADO",
        )

        for item_data in items_data:
            InvoiceItem.objects.create(
                invoice=invoice,
                product=item_data["product"],
                quantity=item_data["quantity"],
                unit_price=item_data["unit_price"],
                total=item_data["total"],
            )

        orders.update(is_paid=True)

        active_register.total_contado += subtotal
        active_register.total_sales += subtotal
        active_register.save()

    messages.success(
        request,
        f" Factura #{invoice.invoice_number} generada por C$ {subtotal:.2f}",
    )

    return redirect("table_list")


# ==========================
# 🍽️ CREACIÓN Y DETALLE DE COMANDAS
# ==========================


@login_required
@user_passes_test(has_valid_role)
def create_order(request, table_id):
    """Crea una nueva comanda para una mesa."""
    table = get_object_or_404(Table, id=table_id)
    products = Product.objects.all().order_by("category__name", "name")
    categories = ProductCategory.objects.all().order_by("name")
    context = {"table": table, "products": products, "categories": categories}

    if request.method == "POST":
        order = Order.objects.create(table=table, user=request.user)
        created_items = 0

        for key, value in request.POST.items():
            if key.startswith("product_") and value.isdigit() and int(value) > 0:
                product = get_object_or_404(Product, id=key.split("_")[1])
                OrderItem.objects.create(
                    order=order, product=product, quantity=int(value)
                )
                created_items += 1

        if created_items:
            messages.success(
                request, f" Comanda #{order.id} creada con {created_items} productos."
            )
            context["order"] = order
            return render(request, "pos/create_order.html", context)

        order.delete()
        messages.warning(request, " No se seleccionaron productos.")
        return redirect("create_order", table_id=table.id)

    return render(request, "pos/create_order.html", context)


@login_required
@user_passes_test(has_valid_role)
def order_detail(request, order_id):
    """Muestra el detalle de una comanda."""
    order = get_object_or_404(Order, id=order_id)
    items = order.orderitem_set.select_related("product")

    if request.method == "POST" and request.POST.get("action") == "mark_paid":
        if not order.is_paid:
            order.is_paid = True
            order.save()
            messages.success(request, f" Comanda #{order.id} marcada como pagada.")
        else:
            messages.info(request, f" La comanda #{order.id} ya estaba pagada.")
        return redirect("table_list")

    return render(
        request,
        "pos/order_detail.html",
        {"order": order, "items": items, "total": order.get_total()},
    )


@login_required
@user_passes_test(user_can_mark_paid)
def edit_order(request, order_id):
    """Permite editar una comanda (mesa, usuario, pagada)."""
    order = get_object_or_404(Order, id=order_id)
    tables = Table.objects.all().order_by("name")
    users = User.objects.all().order_by("username")

    if request.method == "POST":
        order.table_id = request.POST.get("table") or None
        order.user_id = request.POST.get("user") or None
        order.is_paid = request.POST.get("is_paid") == "on"
        order.save()
        messages.success(request, f" Comanda #{order.id} actualizada correctamente.")
        return redirect("order_detail", order_id=order.id)

    return render(
        request,
        "pos/edit_order.html",
        {"order": order, "tables": tables, "users": users},
    )


@login_required
@user_passes_test(has_valid_role)
def print_order(request, order_id):
    """Vista de impresión de comanda."""
    order = get_object_or_404(Order, id=order_id)
    items = order.orderitem_set.select_related("product").all()

    if not items.exists():
        messages.warning(request, f" La comanda #{order.id} no tiene productos.")

    return render(
        request,
        "pos/print_order.html",
        {"order": order, "items": items, "total": order.get_total()},
    )


# ==========================
# 🕒 HISTORIAL Y REPORTES
# ==========================


@login_required
@user_passes_test(has_valid_role)
def order_history(request):
    """Muestra comandas de un día específico."""
    days_ago = int(request.GET.get("days_ago", 0))
    target_date = datetime.now() - timedelta(days=days_ago)

    orders = (
        Order.objects.filter(created_at__date=target_date)
        .select_related("table", "user")
        .order_by("-created_at")
    )

    return render(
        request,
        "orders/order_history.html",
        {
            "orders": orders,
            "target_date": target_date,
            "days_ago": days_ago,
            "prev_days_ago": days_ago + 1,
            "next_days_ago": max(days_ago - 1, 0),
        },
    )


@login_required
@user_passes_test(user_can_view_sales_report)
def daily_report(request):
    """Reporte diario de ventas."""
    days_ago = int(request.GET.get("days_ago", 0))
    target_date = timezone.now().date() - timedelta(days=days_ago)

    orders = Order.objects.filter(
        created_at__date=target_date, is_paid=True
    ).prefetch_related("orderitem_set__product")
    summary, total_sales = {}, Decimal("0")

    for order in orders:
        for item in order.orderitem_set.all():
            name, price = item.product.name, item.product.price
            subtotal = item.quantity * price
            total_sales += subtotal

            summary.setdefault(name, {"qty": 0, "price": price, "subtotal": 0})
            summary[name]["qty"] += item.quantity
            summary[name]["subtotal"] += subtotal

    messages.info(request, f" Ventas del {target_date}: {total_sales:.2f} total.")
    return render(
        request,
        "orders/daily_report.html",
        {
            "orders": orders,
            "product_summary": summary,
            "target_date": target_date,
            "days_ago": days_ago,
            "prev_days_ago": days_ago + 1,
            "next_days_ago": max(days_ago - 1, 0),
            "total_sales": total_sales,
        },
    )


# ==========================
# 🧾 INVENTARIO Y MOVIMIENTOS
# ==========================


@login_required
@user_passes_test(user_can_add_inventory_movement)
def inventory_movement(request):
    """Ajustes de inventario físico."""
    ingredients = Ingredient.objects.all().order_by("warehouse", "name")

    if request.method == "POST":
        note = request.POST.get("note", "").strip()
        count = 0
        with transaction.atomic():
            for ing in ingredients:
                found_str = request.POST.get(f"found_{ing.id}")
                if not found_str:
                    continue
                try:
                    found_qty = Decimal(found_str)
                except Exception:
                    messages.error(request, f" Valor inválido para {ing.name}.")
                    continue
                diff = found_qty - ing.stock_quantity
                if diff != 0:
                    IngredientMovement.objects.create(
                        ingredient=ing,
                        quantity=diff,
                        user=request.user,
                        reason=f"Ajuste por inventario físico. {note}",
                    )
                    count += 1
        if count:
            messages.success(request, f" {count} ajustes aplicados.")
        else:
            messages.info(request, " No se realizaron ajustes.")
    return render(request, "inventory/inventory.html", {"ingredients": ingredients})


@login_required
@user_passes_test(user_can_add_inventory_movement)
def purchase_ingredients(request):
    """Registra compras de ingredientes."""
    ingredients = Ingredient.objects.all().order_by("warehouse", "name")

    if request.method == "POST":
        count = 0
        with transaction.atomic():
            for ing in ingredients:
                qty_str = request.POST.get(f"purchase_{ing.id}")
                if not qty_str:
                    continue
                try:
                    qty = Decimal(qty_str)
                except Exception:
                    messages.error(request, f" Cantidad inválida para {ing.name}.")
                    continue
                if qty > 0:
                    IngredientMovement.objects.create(
                        ingredient=ing,
                        quantity=qty,
                        user=request.user,
                        reason="Compra de ingredientes",
                    )
                    count += 1
        (
            messages.success(request, f" {count} compras registradas.")
            if count
            else messages.info(request, " No se registró ninguna compra.")
        )
        return redirect("purchase_ingredients")

    return render(
        request, "inventory/purchase_ingredients.html", {"ingredients": ingredients}
    )


@login_required
@user_passes_test(user_can_view_reports)
def reports_index(request):
    """Página principal de reportes."""
    return render(request, "reports/index.html")


@login_required
@user_passes_test(user_can_view_inventory)
def report_inventory(request):
    """Muestra el estado actual del inventario."""
    ingredients = Ingredient.objects.all().order_by("name")
    total = ingredients.count()
    context = {"ingredients": ingredients, "total_items": total}
    if request.method == "GET" and request.GET.get("print") == "true":
        context["print"] = True
    return render(request, "reports/report_inventory.html", context)


@login_required
@user_passes_test(user_can_view_inventory)
def print_inventory_report(request):
    ingredients = Ingredient.objects.all().order_by("name")
    total = ingredients.count()
    today = timezone.now()
    return render(
        request,
        "reports/print_inventory_report.html",
        {"ingredients": ingredients, "total_items": total, "today": today},
    )


@login_required
@user_passes_test(user_can_view_inventory)
def export_inventory_csv(request):
    """Exporta el inventario actual a CSV."""
    ingredients = Ingredient.objects.all().order_by("name")

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = (
        f'attachment; filename="inventario_{datetime.now():%Y%m%d_%H%M}.csv"'
    )

    writer = csv.writer(response)
    writer.writerow(["Ingrediente", "Cantidad", "Unidad"])
    for i in ingredients:
        writer.writerow([i.name, i.stock_quantity, getattr(i, "unit", "—")])
    return response


# ==========================
# 💾 REPORTES CSV
# ==========================


@login_required
@user_passes_test(user_can_view_reports)
def report_orders(request):
    """Reporte de comandas por rango de fechas."""
    start, end = parse_date_range(request)
    table = request.GET.get("table", None)
    items = None
    if table:
        items = OrderItem.objects.filter(
            order__created_at__range=(start, end), order__table=table
        ).select_related("order", "product", "order__table", "order__user")
    else:
        items = OrderItem.objects.filter(
            order__created_at__range=(start, end)
        ).select_related("order", "product", "order__table", "order__user")
    total = sum((i.get_total() or 0) for i in items)
    items = items.order_by("-id")
    tables = Table.objects.all()
    return render(
        request,
        "orders/report_orders.html",
        {
            "order_items": items,
            "start": start,
            "end": end,
            "tables": tables,
            "table": table,
            "total": total,
        },
    )


@login_required
@user_passes_test(user_can_view_reports)
def export_orders_csv(request):
    """Exporta las comandas a CSV."""
    start, end = parse_date_range(request)
    table = request.GET.get("table")
    items = None
    if table:
        items = OrderItem.objects.filter(
            order__created_at__range=(start, end), order__table=table
        ).select_related("order", "product", "order__table", "order__user")
    else:
        items = OrderItem.objects.filter(
            order__created_at__range=(start, end)
        ).select_related("order", "product", "order__table", "order__user")

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = (
        f'attachment; filename="comandas_{datetime.now():%Y%m%d_%H%M}.csv"'
    )

    writer = csv.writer(response)
    writer.writerow(
        [
            "Fecha",
            "Comanda",
            "Servicio",
            "Mesa",
            "Cantidad",
            "Producto",
            "Precio",
            "Total",
        ]
    )
    for i in items:
        writer.writerow(
            [
                i.order.created_at.strftime("%Y-%m-%d %H:%M"),
                i.order.id,
                i.order.user.username if i.order.user else "—",
                i.order.table.name if i.order.table else "—",
                i.quantity,
                i.product.name,
                i.product.price,
                i.get_total(),
            ]
        )
    return response


@login_required
@user_passes_test(user_can_view_inventory)
def report_movements(request):
    """Lista los movimientos de inventario."""
    start, end = parse_date_range(request)

    moves = IngredientMovement.objects.filter(
        created_at__range=(start, end)
    ).select_related("ingredient")

    # --- Búsqueda ---
    search = request.GET.get("search")
    if search:
        moves = moves.filter(
            Q(reason__icontains=search) | Q(ingredient__name__icontains=search)
        )

    return render(
        request,
        "reports/report_movements.html",
        {
            "movements": moves,
            "start": start,
            "end": end,
            "search": search,
            "api_url": f"/api/movements/?start={start.strftime('%Y-%m-%dT%H:%M')}&end={end.strftime('%Y-%m-%dT%H:%M')}&search={search or ''}",
        },
    )


@login_required
@user_passes_test(user_can_view_inventory)
def export_movements_csv(request):
    """Exporta los movimientos de inventario a CSV."""
    start, end = parse_date_range(request)

    moves = IngredientMovement.objects.filter(
        created_at__range=(start, end)
    ).select_related("ingredient")

    # --- Filtro de búsqueda (igual que la vista principal) ---
    search = request.GET.get("search")
    if search:
        moves = moves.filter(
            Q(reason__icontains=search) | Q(ingredient__name__icontains=search)
        )

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = (
        f'attachment; filename="movimientos_{datetime.now():%Y%m%d_%H%M}.csv"'
    )

    writer = csv.writer(response)
    writer.writerow(["Fecha", "Cantidad", "Ingrediente", "Razón", "Usuario"])

    for m in moves:
        writer.writerow(
            [
                m.created_at.strftime("%Y-%m-%d %H:%M"),
                m.quantity,
                m.ingredient.name,
                m.reason or "—",
                m.user.username if m.user else "—",
            ]
        )

    return response


@login_required
@user_passes_test(user_can_view_sales_report)
def sales_report_by_product(request):
    """Reporte de ventas por producto (filtrable por fecha)."""
    start, end = parse_date_range(request)

    # Filtramos solo órdenes pagadas en el rango seleccionado
    items = (
        OrderItem.objects.filter(
            order__is_paid=True, order__created_at__range=(start, end)
        )
        .select_related(
            "product",
        )
        .values("product__name", "product__dispatch_area__name")
        .annotate(
            total_qty=Sum("quantity"),
            total_sales=Sum(F("quantity") * F("product__price")),
            price=F("product__price"),
        )
        .order_by("product__dispatch_area__name", "product__name")
    )

    # Total general del rango
    total_sales = sum((i["total_sales"] or 0) for i in items)

    totals_by_dispatch_area = (
        OrderItem.objects.filter(
            order__is_paid=True, order__created_at__range=(start, end)
        )
        .values("product__dispatch_area__name")
        .annotate(
            area_total_qty=Sum("quantity"),
            area_total_sales=Sum(F("quantity") * F("product__price")),
        )
        .order_by("product__dispatch_area__name")
    )

    context = {
        "items": items,
        "total_sales": total_sales,
        "start": start,
        "end": end,
        "totals_by_dispatch_area": totals_by_dispatch_area,
        "api_url": f"/api/sales-by-product/?start={start.strftime('%Y-%m-%dT%H:%M')}&end={end.strftime('%Y-%m-%dT%H:%M')}",
    }
    return render(request, "reports/sales_report_by_product.html", context)


@login_required
@user_passes_test(user_can_view_sales_report)
def export_sales_by_product_csv(request):
    """Exporta el reporte de ventas por producto a CSV."""
    start, end = parse_date_range(request)
    items = (
        OrderItem.objects.filter(
            order__is_paid=True, order__created_at__range=(start, end)
        )
        .select_related("product")
        .values("product__name", "product__dispatch_area__name")
        .annotate(
            total_qty=Sum("quantity"),
            total_sales=Sum(F("quantity") * F("product__price")),
            price=F("product__price"),
        )
        .order_by("product__dispatch_area__name", "product__name")
    )

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = (
        f'attachment; filename="ventas_por_producto_{datetime.now():%Y%m%d_%H%M}.csv"'
    )

    writer = csv.writer(response)
    writer.writerow(["Producto", "Precio Unitario", "Cantidad", "Total"])
    for i in items:
        writer.writerow(
            [i["product__name"], i["price"], i["total_qty"], i["total_sales"]]
        )

    return response


# ==========================
#  APIs JSON PARA REPORTES
# ==========================


@login_required
@user_passes_test(user_can_view_sales_report)
def api_sales_today(request):
    """API JSON: Ventas del día actual."""
    today = datetime.today().date()
    start = datetime.combine(today, time.min)
    end = datetime.combine(today, time.max)

    items = (
        OrderItem.objects.filter(
            order__is_paid=True, order__created_at__range=(start, end)
        )
        .select_related("product", "order")
        .values(
            "product__name",
            "product__dispatch_area__name",
            "product__price",
        )
        .annotate(
            total_qty=Sum("quantity"),
            total_sales=Sum(F("quantity") * F("product__price")),
        )
        .order_by("product__dispatch_area__name", "product__name")
    )

    data = [
        {
            "dispatch_area": i["product__dispatch_area__name"] or "Sin área",
            "product": i["product__name"],
            "price": float(i["product__price"]),
            "quantity": i["total_qty"],
            "total": float(i["total_sales"] or 0),
        }
        for i in items
    ]
    return JsonResponse(data, safe=False)


@login_required
@user_passes_test(user_can_view_reports)
def api_orders(request):
    """API JSON: Lista de comandas."""
    orders = (
        Order.objects.all()
        .select_related("table", "user")
        .order_by("-created_at")[:100]
    )

    data = [
        {
            "id": o.id,
            "table": o.table.name if o.table else "Sin mesa",
            "total": float(o.get_total()),
            "status": o.get_status_display(),
            "created_at": o.created_at.strftime("%d/%m/%Y %H:%M"),
            "user": o.user.username if o.user else "—",
        }
        for o in orders
    ]
    return JsonResponse(data, safe=False)


@login_required
@user_passes_test(user_can_view_inventory)
def api_inventory(request):
    """API JSON: Inventario actual con paginación."""
    queryset = Ingredient.objects.select_related("warehouse").order_by("name")

    search = request.GET.get("search", "").strip()
    if search:
        queryset = queryset.filter(name__icontains=search)

    sort = request.GET.get("sort", "")
    if sort:
        try:
            field, direction = sort.split(",")
            if direction == "desc":
                field = f"-{field}"
            queryset = queryset.order_by(field)
        except ValueError:
            pass

    try:
        page = int(request.GET.get("page", 1))
        limit = int(request.GET.get("limit", 25))
    except ValueError:
        page = 1
        limit = 25

    if limit == 0:
        items = list(
            queryset.values("id", "name", "stock_quantity", "unit", "warehouse__name")
        )
        data = [
            {
                "id": i["id"],
                "name": i["name"],
                "stock": float(i["stock_quantity"]),
                "unit": dict(Ingredient.UNITS).get(i["unit"], i["unit"]),
                "warehouse": i["warehouse__name"] or "—",
            }
            for i in items
        ]
        return JsonResponse({"count": len(data), "results": data}, safe=False)

    total = queryset.count()
    start = (page - 1) * limit
    end = start + limit
    items = list(
        queryset.values("id", "name", "stock_quantity", "unit", "warehouse__name")[
            start:end
        ]
    )

    data = [
        {
            "id": i["id"],
            "name": i["name"],
            "stock": float(i["stock_quantity"]),
            "unit": dict(Ingredient.UNITS).get(i["unit"], i["unit"]),
            "warehouse": i["warehouse__name"] or "—",
        }
        for i in items
    ]

    return JsonResponse({"count": total, "results": data}, safe=False)


@login_required
@user_passes_test(user_can_view_inventory)
def api_movements(request):
    """API JSON: Movimientos de inventario con paginación."""
    start, end = parse_date_range(request)

    queryset = IngredientMovement.objects.filter(
        created_at__range=(start, end)
    ).select_related("ingredient", "user")

    search = request.GET.get("search", "").strip()
    if search:
        queryset = queryset.filter(
            Q(reason__icontains=search) | Q(ingredient__name__icontains=search)
        )

    sort = request.GET.get("sort", "")
    if sort:
        try:
            field, direction = sort.split(",")
            if direction == "desc":
                field = f"-{field}"
            queryset = queryset.order_by(field)
        except ValueError:
            queryset = queryset.order_by("-created_at")
    else:
        queryset = queryset.order_by("-created_at")

    try:
        page = int(request.GET.get("page", 1))
        limit = int(request.GET.get("limit", 25))
    except ValueError:
        page = 1
        limit = 25

    if limit == 0:
        items = list(
            queryset.values(
                "id",
                "created_at",
                "ingredient__name",
                "quantity",
                "reason",
                "user__username",
            )
        )
        data = [
            {
                "id": i["id"],
                "date": i["created_at"].strftime("%d/%m/%Y %H:%M"),
                "ingredient": i["ingredient__name"],
                "quantity": float(i["quantity"]),
                "reason": i["reason"] or "—",
                "user": i["user__username"] or "—",
            }
            for i in items
        ]
        return JsonResponse({"count": len(data), "results": data}, safe=False)

    total = queryset.count()
    start = (page - 1) * limit
    end = start + limit
    items = list(
        queryset.values(
            "id",
            "created_at",
            "ingredient__name",
            "quantity",
            "reason",
            "user__username",
        )[start:end]
    )

    data = [
        {
            "id": i["id"],
            "date": i["created_at"].strftime("%d/%m/%Y %H:%M"),
            "ingredient": i["ingredient__name"],
            "quantity": float(i["quantity"]),
            "reason": i["reason"] or "—",
            "user": i["user__username"] or "—",
        }
        for i in items
    ]

    return JsonResponse({"count": total, "results": data}, safe=False)


@login_required
@user_passes_test(user_can_view_sales_report)
def api_sales_by_product(request):
    """API JSON: Ventas por producto con paginación."""
    start, end = parse_date_range(request)

    queryset = (
        OrderItem.objects.filter(
            order__is_paid=True, order__created_at__range=(start, end)
        )
        .select_related("product", "product__dispatch_area")
        .values("product__name", "product__dispatch_area__name", "product__price")
        .annotate(
            total_qty=Sum("quantity"),
            total_sales=Sum(F("quantity") * F("product__price")),
            price=F("product__price"),
        )
    )

    search = request.GET.get("search", "").strip()
    if search:
        queryset = queryset.filter(product__name__icontains=search)

    sort = request.GET.get("sort", "")
    if sort:
        try:
            field, direction = sort.split(",")
            sort_field = field
            if field == "dispatch_area":
                sort_field = "product__dispatch_area__name"
            elif field == "product":
                sort_field = "product__name"
            elif field == "price":
                sort_field = "product__price"
            elif field == "quantity":
                sort_field = "total_qty"
            elif field == "total":
                sort_field = "total_sales"
            if direction == "desc":
                sort_field = f"-{sort_field}"
            queryset = queryset.order_by(sort_field)
        except ValueError:
            queryset = queryset.order_by(
                "product__dispatch_area__name", "product__name"
            )
    else:
        queryset = queryset.order_by("product__dispatch_area__name", "product__name")

    try:
        page = int(request.GET.get("page", 1))
        limit = int(request.GET.get("limit", 25))
    except ValueError:
        page = 1
        limit = 25

    if limit == 0:
        items = list(queryset)
        data = [
            {
                "dispatch_area": i["product__dispatch_area__name"] or "Sin área",
                "product": i["product__name"],
                "price": float(i["price"]),
                "quantity": i["total_qty"],
                "total": float(i["total_sales"] or 0),
            }
            for i in items
        ]
        return JsonResponse({"count": len(data), "results": data}, safe=False)

    total = queryset.count()
    start_idx = (page - 1) * limit
    end_idx = start_idx + limit
    items = list(queryset[start_idx:end_idx])

    data = [
        {
            "dispatch_area": i["product__dispatch_area__name"] or "Sin área",
            "product": i["product__name"],
            "price": float(i["price"]),
            "quantity": i["total_qty"],
            "total": float(i["total_sales"] or 0),
        }
        for i in items
    ]

    return JsonResponse({"count": total, "results": data}, safe=False)


@login_required
@user_passes_test(user_can_view_reports)
def api_orders_report(request):
    """API JSON: Reporte de comandas con paginación."""
    start, end = parse_date_range(request)
    table_id = request.GET.get("table")

    queryset = (
        OrderItem.objects.filter(order__created_at__range=(start, end))
        .select_related("order", "product", "order__table", "order__user")
        .order_by("-order__created_at", "-id")
    )

    if table_id:
        queryset = queryset.filter(order__table_id=table_id)

    search = request.GET.get("search", "").strip()
    if search:
        queryset = queryset.filter(
            Q(product__name__icontains=search)
            | Q(order__table__name__icontains=search)
            | Q(order__user__username__icontains=search)
        )

    sort = request.GET.get("sort", "")
    if sort:
        try:
            field, direction = sort.split(",")
            sort_field = field
            if field == "date":
                sort_field = "order__created_at"
            elif field == "order_id":
                sort_field = "order__id"
            elif field == "user":
                sort_field = "order__user__username"
            elif field == "table":
                sort_field = "order__table__name"
            elif field == "quantity":
                sort_field = "quantity"
            elif field == "product":
                sort_field = "product__name"
            elif field == "price":
                sort_field = "product__price"
            elif field == "total":
                sort_field = "order__id"
            if direction == "desc":
                sort_field = f"-{sort_field}"
            queryset = queryset.order_by(sort_field)
        except ValueError:
            pass

    try:
        page = int(request.GET.get("page", 1))
        limit = int(request.GET.get("limit", 25))
    except ValueError:
        page = 1
        limit = 25

    if limit == 0:
        items = list(queryset)
        data = [
            {
                "id": i.id,
                "date": (
                    i.order.created_at.strftime("%d/%m/%Y %H:%M") if i.order else "—"
                ),
                "order_id": i.order.id if i.order else None,
                "user": i.order.user.username if i.order and i.order.user else "—",
                "table": i.order.table.name if i.order and i.order.table else "—",
                "quantity": i.quantity,
                "product": i.product.name,
                "price": float(i.product.price),
                "total": float(i.get_total() or 0),
            }
            for i in items
        ]
        return JsonResponse({"count": len(data), "results": data}, safe=False)

    total = queryset.count()
    start_idx = (page - 1) * limit
    end_idx = start_idx + limit
    items = list(queryset[start_idx:end_idx])

    data = [
        {
            "id": i.id,
            "date": i.order.created_at.strftime("%d/%m/%Y %H:%M") if i.order else "—",
            "order_id": i.order.id if i.order else None,
            "user": i.order.user.username if i.order and i.order.user else "—",
            "table": i.order.table.name if i.order and i.order.table else "—",
            "quantity": i.quantity,
            "product": i.product.name,
            "price": float(i.product.price),
            "total": float(i.get_total() or 0),
        }
        for i in items
    ]

    return JsonResponse({"count": total, "results": data}, safe=False)


# ==========================
# 📦 GESTIÓN DE PRODUCTOS
# ==========================


@login_required
@user_passes_test(user_can_manage_menu)
def product_list(request):
    """Lista todos los productos."""
    products = (
        Product.objects.all()
        .select_related("category", "dispatch_area")
        .order_by("name")
    )
    return render(request, "menu/product_list.html", {"products": products})


@login_required
@user_passes_test(user_can_manage_menu)
def product_create(request):
    """Crea un nuevo producto."""
    categories = ProductCategory.objects.all().order_by("name")
    dispatch_areas = DispatchArea.objects.all().order_by("name")

    if request.method == "POST":
        name = request.POST.get("name")
        category_id = request.POST.get("category") or None
        dispatch_area_id = request.POST.get("dispatch_area") or None
        price = request.POST.get("price")

        if not name or not price:
            messages.error(request, " Nombre y precio son obligatorios.")
        else:
            try:
                product = Product.objects.create(
                    name=name,
                    category_id=category_id,
                    dispatch_area_id=dispatch_area_id,
                    price=Decimal(price),
                )
                messages.success(
                    request, f" Producto '{product.name}' creado exitosamente."
                )
                return redirect("product_list")
            except Exception as e:
                messages.error(request, f" Error al crear producto: {e}")

    return render(
        request,
        "menu/product_form.html",
        {
            "categories": categories,
            "dispatch_areas": dispatch_areas,
            "title": "Crear Producto",
        },
    )


@login_required
@user_passes_test(user_can_manage_menu)
def product_edit(request, product_id):
    """Edita un producto existente."""
    product = get_object_or_404(Product, id=product_id)
    categories = ProductCategory.objects.all().order_by("name")
    dispatch_areas = DispatchArea.objects.all().order_by("name")

    if request.method == "POST":
        name = request.POST.get("name")
        category_id = request.POST.get("category") or None
        dispatch_area_id = request.POST.get("dispatch_area") or None
        price = request.POST.get("price")

        if not name or not price:
            messages.error(request, " Nombre y precio son obligatorios.")
        else:
            try:
                product.name = name
                product.category_id = category_id
                product.dispatch_area_id = dispatch_area_id
                product.price = Decimal(price)
                product.save()
                messages.success(
                    request, f" Producto '{product.name}' actualizado exitosamente."
                )
                return redirect("product_list")
            except Exception as e:
                messages.error(request, f" Error al actualizar producto: {e}")

    return render(
        request,
        "menu/product_form.html",
        {
            "product": product,
            "categories": categories,
            "dispatch_areas": dispatch_areas,
            "title": "Editar Producto",
        },
    )


@login_required
@user_passes_test(user_can_manage_menu)
def product_delete(request, product_id):
    """Elimina un producto (soft delete)."""
    product = get_object_or_404(Product, id=product_id)

    if request.method == "POST":
        try:
            product_name = product.name
            product.soft_delete()
            messages.success(
                request, f" Producto '{product_name}' eliminado exitosamente."
            )
            return redirect("product_list")
        except Exception as e:
            messages.error(request, f" Error al eliminar producto: {e}")
            return redirect("product_list")

    return render(request, "menu/product_confirm_delete.html", {"product": product})


@login_required
@user_passes_test(user_can_manage_menu)
def product_restore(request, product_id):
    """Restaura un producto eliminado."""
    product = get_object_or_404(Product.all_objects, id=product_id)
    if not product.is_deleted:
        messages.warning(request, " El producto no está eliminado.")
        return redirect("product_list")
    product.restore()
    messages.success(request, f" Producto '{product.name}' restaurado exitosamente.")
    return redirect("product_list")


# ==========================
# 🏷️ GESTIÓN DE CATEGORÍAS DE PRODUCTOS
# ==========================


@login_required
@user_passes_test(user_can_manage_menu)
def category_list(request):
    """Lista todas las categorías de productos."""
    categories = ProductCategory.objects.all().order_by("name")
    return render(request, "menu/category_list.html", {"categories": categories})


@login_required
@user_passes_test(user_can_manage_menu)
def category_create(request):
    """Crea una nueva categoría de producto."""
    if request.method == "POST":
        name = request.POST.get("name")

        if not name:
            messages.error(request, " El nombre de la categoría es obligatorio.")
        else:
            try:
                category = ProductCategory.objects.create(name=name)
                messages.success(
                    request, f" Categoría '{category.name}' creada exitosamente."
                )
                return redirect("category_list")
            except Exception as e:
                messages.error(request, f" Error al crear categoría: {e}")

    return render(request, "menu/category_form.html", {"title": "Crear Categoría"})


@login_required
@user_passes_test(user_can_manage_menu)
def category_edit(request, category_id):
    """Edita una categoría existente."""
    category = get_object_or_404(ProductCategory, id=category_id)

    if request.method == "POST":
        name = request.POST.get("name")

        if not name:
            messages.error(request, " El nombre de la categoría es obligatorio.")
        else:
            try:
                category.name = name
                category.save()
                messages.success(
                    request, f" Categoría '{category.name}' actualizada exitosamente."
                )
                return redirect("category_list")
            except Exception as e:
                messages.error(request, f" Error al actualizar categoría: {e}")

    return render(
        request,
        "category_form.html",
        {"category": category, "title": "Editar Categoría"},
    )


@login_required
@user_passes_test(user_can_manage_menu)
def category_delete(request, category_id):
    """Elimina una categoría (soft delete)."""
    category = get_object_or_404(ProductCategory, id=category_id)

    # Verificar si hay productos usando esta categoría
    products_using_category = Product.objects.filter(category=category).count()

    if request.method == "POST":
        try:
            category_name = category.name
            category.soft_delete()
            messages.success(
                request, f" Categoría '{category_name}' eliminada exitosamente."
            )
            return redirect("category_list")
        except Exception as e:
            messages.error(request, f" Error al eliminar categoría: {e}")
            return redirect("category_list")

    return render(
        request,
        "menu/category_confirm_delete.html",
        {
            "category": category,
            "products_using_category": products_using_category,
        },
    )


@login_required
@user_passes_test(user_can_manage_menu)
def category_restore(request, category_id):
    """Restaura una categoría eliminada."""
    category = get_object_or_404(ProductCategory.all_objects, id=category_id)
    if not category.is_deleted:
        messages.warning(request, " La categoría no está eliminada.")
        return redirect("category_list")
    category.restore()
    messages.success(request, f" Categoría '{category.name}' restaurada exitosamente.")
    return redirect("category_list")


# ==========================
# 🚚 GESTIÓN DE ÁREAS DE DESPACHO
# ==========================


@login_required
@user_passes_test(user_can_manage_menu)
def dispatch_area_list(request):
    """Lista todas las áreas de despacho."""
    areas = DispatchArea.objects.all().order_by("name")
    return render(request, "menu/dispatch_area_list.html", {"areas": areas})


@login_required
@user_passes_test(user_can_manage_menu)
def dispatch_area_create(request):
    """Crea una nueva área de despacho."""
    if request.method == "POST":
        name = request.POST.get("name")

        if not name:
            messages.error(
                request, " El nombre del área de despacho es obligatorio."
            )  # noqa: E501
        else:
            try:
                area = DispatchArea.objects.create(name=name)
                messages.success(
                    request,
                    f" Área de despacho '{area.name}' creada exitosamente.",
                )
                return redirect("dispatch_area_list")
            except Exception as e:
                messages.error(
                    request, f" Error al crear área de despacho: {e}"
                )  # noqa: E501

    return render(
        request,
        "menu/dispatch_area_form.html",
        {"title": "Crear Área de Despacho"},
    )


@login_required
@user_passes_test(user_can_manage_menu)
def dispatch_area_edit(request, area_id):
    """Edita un área de despacho existente."""
    area = get_object_or_404(DispatchArea, id=area_id)

    if request.method == "POST":
        name = request.POST.get("name")

        if not name:
            messages.error(
                request, " El nombre del área de despacho es obligatorio."
            )  # noqa: E501
        else:
            try:
                area.name = name
                area.save()
                messages.success(
                    request,
                    f" Área de despacho '{area.name}' actualizada exitosamente.",
                )
                return redirect("dispatch_area_list")
            except Exception as e:
                messages.error(
                    request, f" Error al actualizar área de despacho: {e}"
                )  # noqa: E501

    return render(
        request,
        "menu/dispatch_area_form.html",
        {"area": area, "title": "Editar Área de Despacho"},
    )


@login_required
@user_passes_test(user_can_manage_menu)
def dispatch_area_delete(request, area_id):
    """Elimina un área de despacho (soft delete)."""
    area = get_object_or_404(DispatchArea, id=area_id)

    # Verificar si hay productos usando esta área
    products_using_area = Product.objects.filter(dispatch_area=area).count()

    if request.method == "POST":
        try:
            area_name = area.name
            area.soft_delete()
            messages.success(
                request,
                f" Área de despacho '{area_name}' eliminada exitosamente.",
            )
            return redirect("dispatch_area_list")
        except Exception as e:
            messages.error(request, f" Error al eliminar área de despacho: {e}")
            return redirect("dispatch_area_list")

    return render(
        request,
        "menu/dispatch_area_confirm_delete.html",
        {
            "area": area,
            "products_using_area": products_using_area,
        },
    )


@login_required
@user_passes_test(user_can_manage_menu)
def dispatch_area_restore(request, area_id):
    """Restaura un área de despacho eliminada."""
    area = get_object_or_404(DispatchArea.all_objects, id=area_id)
    if not area.is_deleted:
        messages.warning(request, " El área de despacho no está eliminada.")
        return redirect("dispatch_area_list")
    area.restore()
    messages.success(
        request, f" Área de despacho '{area.name}' restaurada exitosamente."
    )
    return redirect("dispatch_area_list")


# ==========================
# 🍽️ GESTIÓN DE MESAS
# ==========================


@login_required
@user_passes_test(has_valid_role)
def table_management_list(request):
    """Lista todas las mesas activas."""
    tables = Table.objects.all().order_by("name")
    return render(request, "tables/table_list.html", {"tables": tables})


@login_required
@user_passes_test(has_valid_role)
def table_management_create(request):
    """Crea una nueva mesa."""
    if request.method == "POST":
        form = TableForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, " Mesa creada exitosamente.")
            return redirect("table_management_list")
        else:
            messages.error(request, f" Error: {form.errors}")
    else:
        form = TableForm()
    return render(
        request, "tables/table_form.html", {"form": form, "title": "Crear Mesa"}
    )


@login_required
@user_passes_test(has_valid_role)
def table_management_detail(request, table_id):
    """Muestra el detalle de una mesa."""
    table = get_object_or_404(Table, id=table_id)
    return render(request, "tables/table_detail.html", {"table": table})


@login_required
@user_passes_test(has_valid_role)
def table_management_edit(request, table_id):
    """Edita una mesa existente."""
    table = get_object_or_404(Table, id=table_id)
    if request.method == "POST":
        form = TableForm(request.POST, instance=table)
        if form.is_valid():
            form.save()
            messages.success(request, f" Mesa '{table.name}' actualizada exitosamente.")
            return redirect("table_management_list")
        else:
            messages.error(request, f" Error: {form.errors}")
    else:
        form = TableForm(instance=table)
    return render(
        request,
        "tables/table_form.html",
        {"form": form, "table": table, "title": "Editar Mesa"},
    )


@login_required
@user_passes_test(has_valid_role)
def table_management_delete(request, table_id):
    """Elimina una mesa (soft delete)."""
    table = get_object_or_404(Table, id=table_id)
    if request.method == "POST":
        table.soft_delete()
        messages.success(request, f" Mesa '{table.name}' eliminada exitosamente.")
        return redirect("table_management_list")
    return render(request, "tables/table_confirm_delete.html", {"table": table})


@login_required
@user_passes_test(has_valid_role)
def table_management_restore(request, table_id):
    """Restaura una mesa eliminada."""
    table = get_object_or_404(Table, id=table_id)
    if not table.is_deleted:
        messages.warning(request, " La mesa no está eliminada.")
        return redirect("table_management_list")
    table.restore()
    messages.success(request, f" Mesa '{table.name}' restaurada exitosamente.")
    return redirect("table_management_list")


# ==========================
# 📋 GESTIÓN DE RECETAS
# ==========================


@login_required
@user_passes_test(user_can_manage_menu)
def product_recipes(request, product_id):
    """Gestiona todos los ingredientes de un producto usando formsets."""
    product = get_object_or_404(Product, id=product_id)

    # Crear formset para ProductIngredient
    ProductIngredientFormSet = modelformset_factory(
        ProductIngredient,
        form=ProductIngredientForm,
        extra=1,  # 1 formulario vacío inicial para agregar nuevos ingredientes dinámicamente
        can_delete=True,
    )

    # Queryset solo para este producto
    queryset = ProductIngredient.objects.filter(product=product).order_by(
        "ingredient__name"
    )

    if request.method == "POST":
        formset = ProductIngredientFormSet(
            request.POST,
            queryset=queryset,
            form_kwargs={"product": product},  # Pasar producto para validación
        )

        if formset.is_valid():
            try:
                with transaction.atomic():
                    instances = formset.save(commit=False)

                    # Validar que no haya ingredientes duplicados en el formset
                    ingredient_ids = []
                    for instance in instances:
                        if not instance.id:  # Nueva instancia
                            instance.product = product

                        # Verificar duplicados dentro del formset
                        if instance.ingredient_id in ingredient_ids:
                            messages.error(
                                request,
                                f" El ingrediente '{instance.ingredient.name}' está duplicado.",
                            )
                            return redirect("product_recipes", product_id=product.id)
                        ingredient_ids.append(instance.ingredient_id)

                    # Guardar todas las instancias
                    for instance in instances:
                        instance.save()

                    # Eliminar las marcadas para borrar
                    for obj in formset.deleted_objects:
                        obj.delete()

                    messages.success(request, " Receta actualizada exitosamente.")
                    return redirect("product_recipes", product_id=product.id)

            except Exception as e:
                messages.error(request, f" Error al guardar receta: {e}")
        else:
            messages.error(request, " Corrige los errores en el formulario.")
    else:
        formset = ProductIngredientFormSet(
            queryset=queryset,
            form_kwargs={"product": product},
        )

    return render(
        request,
        "menu/product_recipes.html",
        {
            "product": product,
            "formset": formset,
        },
    )


# ==========================
# 🧂 GESTIÓN DE INGREDIENTES
# ==========================


@login_required
@user_passes_test(user_can_manage_inventory_full)
def ingredient_list(request):
    """Lista todos los ingredientes."""
    ingredients = Ingredient.objects.all().select_related("warehouse").order_by("name")
    return render(
        request, "inventory/ingredient_list.html", {"ingredients": ingredients}
    )


@login_required
@user_passes_test(user_can_manage_inventory_full)
def ingredient_create(request):
    """Crea un nuevo ingrediente."""
    warehouses = Warehouse.objects.all().order_by("name")

    if request.method == "POST":
        name = request.POST.get("name")
        unit = request.POST.get("unit")
        warehouse_id = request.POST.get("warehouse") or None

        if not name or not unit:
            messages.error(request, " Nombre y unidad son obligatorios.")
        else:
            try:
                ingredient = Ingredient.objects.create(
                    name=name,
                    unit=unit,
                    warehouse_id=warehouse_id,
                )
                messages.success(
                    request, f" Ingrediente '{ingredient.name}' creado exitosamente."
                )
                return redirect("ingredient_list")
            except Exception as e:
                messages.error(request, f" Error al crear ingrediente: {e}")

    return render(
        request,
        "inventory/ingredient_form.html",
        {
            "warehouses": warehouses,
            "units": Ingredient.UNITS,
            "title": "Crear Ingrediente",
        },
    )


@login_required
@user_passes_test(user_can_manage_inventory_full)
def ingredient_edit(request, ingredient_id):
    """Edita un ingrediente existente."""
    ingredient = get_object_or_404(Ingredient, id=ingredient_id)
    warehouses = Warehouse.objects.all().order_by("name")

    if request.method == "POST":
        name = request.POST.get("name")
        unit = request.POST.get("unit")
        warehouse_id = request.POST.get("warehouse") or None

        if not name or not unit:
            messages.error(request, " Nombre y unidad son obligatorios.")
        else:
            try:
                ingredient.name = name
                ingredient.unit = unit
                ingredient.warehouse_id = warehouse_id
                ingredient.save()
                messages.success(
                    request,
                    f" Ingrediente '{ingredient.name}' actualizado exitosamente.",
                )
                return redirect("ingredient_list")
            except Exception as e:
                messages.error(request, f" Error al actualizar ingrediente: {e}")

    return render(
        request,
        "inventory/ingredient_form.html",
        {
            "ingredient": ingredient,
            "warehouses": warehouses,
            "units": Ingredient.UNITS,
            "title": "Editar Ingrediente",
        },
    )


@login_required
@user_passes_test(user_can_manage_inventory_full)
def ingredient_delete(request, ingredient_id):
    """Elimina un ingrediente (soft delete)."""
    ingredient = get_object_or_404(Ingredient, id=ingredient_id)

    # Verificar si hay movimientos o recetas usando este ingrediente
    movements_count = IngredientMovement.objects.filter(ingredient=ingredient).count()
    recipes_count = ProductIngredient.objects.filter(ingredient=ingredient).count()

    if request.method == "POST":
        try:
            ingredient_name = ingredient.name
            ingredient.soft_delete()
            messages.success(
                request, f" Ingrediente '{ingredient_name}' eliminado exitosamente."
            )
            return redirect("ingredient_list")
        except Exception as e:
            messages.error(request, f" Error al eliminar ingrediente: {e}")
            return redirect("ingredient_list")

    return render(
        request,
        "inventory/ingredient_confirm_delete.html",
        {
            "ingredient": ingredient,
            "movements_count": movements_count,
            "recipes_count": recipes_count,
        },
    )


@login_required
@user_passes_test(user_can_manage_inventory_full)
def ingredient_restore(request, ingredient_id):
    """Restaura un ingrediente eliminado."""
    ingredient = get_object_or_404(Ingredient.all_objects, id=ingredient_id)
    if not ingredient.is_deleted:
        messages.warning(request, " El ingrediente no está eliminado.")
        return redirect("ingredient_list")
    ingredient.restore()
    messages.success(
        request, f" Ingrediente '{ingredient.name}' restaurado exitosamente."
    )
    return redirect("ingredient_list")


# ==========================
# 🏢 CONFIGURACIÓN DE EMPRESA
# ==========================


@login_required
@user_passes_test(user_can_manage_menu)
def company_settings(request):
    """Vista para configurar los datos de la empresa (solo una instancia)."""
    # Obtener la única instancia de Company, si existe
    company = Company.objects.first()

    if request.method == "POST":
        # Si ya existe, actualizar; si no, crear nueva
        if company:
            company.name = request.POST.get("name", "").strip()
            company.ruc = request.POST.get("ruc", "").strip()
            company.address = request.POST.get("address", "").strip()
            company.phone = request.POST.get("phone", "").strip()
            company.email = request.POST.get("email", "").strip()
            company.slogan = request.POST.get("slogan", "").strip()

            # Manejar archivo de logo
            if "logo" in request.FILES:
                company.logo = request.FILES["logo"]
        else:
            company = Company(
                name=request.POST.get("name", "").strip(),
                ruc=request.POST.get("ruc", "").strip(),
                address=request.POST.get("address", "").strip(),
                phone=request.POST.get("phone", "").strip(),
                email=request.POST.get("email", "").strip(),
                slogan=request.POST.get("slogan", "").strip(),
            )
            if "logo" in request.FILES:
                company.logo = request.FILES["logo"]

        try:
            company.save()
            messages.success(
                request, " Configuración de empresa guardada exitosamente."
            )
            return redirect("company_settings")
        except Exception as e:
            messages.error(request, f" Error al guardar configuración: {e}")

    return render(request, "settings/company_settings.html", {"company": company})


# ==========================
#  DASHBOARD
# ==========================


@login_required
@user_passes_test(has_valid_role)
def dashboard(request):
    """Dashboard principal con gráficos adaptados al grupo del usuario."""
    from users.utils import (
        is_administrador,
        is_cajero,
        is_cocinero,
        is_servicio,
        is_supervisor,
        user_can_view_inventory,
        user_can_view_sales_report,
    )

    # Obtener fecha actual
    today = timezone.now().date()
    start_of_day = timezone.make_aware(datetime.combine(today, time.min))
    end_of_day = timezone.make_aware(datetime.combine(today, time.max))

    # Datos disponibles para todos los grupos
    context = {
        "is_admin": is_administrador(request.user),
        "is_supervisor": is_supervisor(request.user),
        "is_cajero": is_cajero(request.user),
        "is_cocinero": is_cocinero(request.user),
        "is_servicio": is_servicio(request.user),
    }

    # Ventas del día (si puede ver reporte de ventas)
    if user_can_view_sales_report(request.user):
        # Total ventas hoy
        sales_today = OrderItem.objects.filter(
            order__is_paid=True, order__created_at__range=(start_of_day, end_of_day)
        ).aggregate(total=Sum(F("quantity") * F("product__price")))
        context["sales_today"] = sales_today["total"] or 0

        # Ventas por área de despacho hoy
        sales_by_area = (
            OrderItem.objects.filter(
                order__is_paid=True,
                order__created_at__range=(start_of_day, end_of_day),
                product__dispatch_area__name__isnull=False,
            )
            .values("product__dispatch_area__name")
            .annotate(total=Sum(F("quantity") * F("product__price")))
            .order_by("product__dispatch_area__name")
        )
        sales_by_area_list = list(sales_by_area)
        context["sales_by_area"] = sales_by_area_list
        # Preparar datos para gráfico de áreas
        area_labels = [
            item["product__dispatch_area__name"] for item in sales_by_area_list
        ]
        area_data = [float(item["total"] or 0) for item in sales_by_area_list]
        context["area_labels"] = area_labels
        context["area_data"] = area_data

        # Ventas últimos 7 días
        sales_labels = []
        sales_data = []
        for i in range(6, -1, -1):
            day = today - timedelta(days=i)
            start = timezone.make_aware(datetime.combine(day, time.min))
            end = timezone.make_aware(datetime.combine(day, time.max))
            daily_sales = OrderItem.objects.filter(
                order__is_paid=True, order__created_at__range=(start, end)
            ).aggregate(total=Sum(F("quantity") * F("product__price")))
            sales_labels.append(day.strftime("%d/%m"))
            sales_data.append(float(daily_sales["total"] or 0))
        context["sales_labels"] = sales_labels
        context["sales_data"] = sales_data

    # Inventario (si puede ver inventario)
    if user_can_view_inventory(request.user):
        # Ingredientes con stock bajo (menor a 5 unidades)
        low_stock_qs = Ingredient.objects.filter(stock_quantity__lt=5)
        context["low_stock_count"] = low_stock_qs.count()

        # Top 10 ingredientes con menor stock para el gráfico
        low_stock = low_stock_qs.values("name", "stock_quantity", "unit").order_by(
            "stock_quantity"
        )[:10]
        low_stock_list = list(low_stock)
        context["low_stock"] = low_stock_list
        # Preparar datos para gráfico de stock
        stock_labels = [item["name"] for item in low_stock_list]
        stock_data = [float(item["stock_quantity"]) for item in low_stock_list]
        context["stock_labels"] = stock_labels
        context["stock_data"] = stock_data

    # Órdenes pendientes (si puede ver órdenes)
    if request.user.has_perm("orders.view_order"):

        pending_orders = Order.objects.filter(is_paid=False).count()
        context["pending_orders"] = pending_orders

        # Órdenes pendientes por mesa
        pending_by_table = (
            Order.objects.filter(is_paid=False, table__name__isnull=False)
            .values("table__name")
            .annotate(count=Count("id"))
            .order_by("table__name")
        )
        pending_by_table_list = list(pending_by_table)
        context["pending_by_table"] = pending_by_table_list
        # Preparar datos para gráfico de órdenes pendientes
        orders_labels = [item["table__name"] for item in pending_by_table_list]
        orders_data = [item["count"] for item in pending_by_table_list]
        context["orders_labels"] = orders_labels
        context["orders_data"] = orders_data

    return render(request, "dashboard.html", context)


# ==========================
# 📡 API GRIDJS - ENDPOINTS JSON
# ==========================


@login_required
def api_ingredients(request):
    """API endpoint que retorna lista de ingredientes en formato JSON para Grid.js."""
    ingredients = Ingredient.objects.select_related("warehouse").order_by("name")
    data = [
        {
            "id": i.id,
            "name": i.name,
            "unit": i.get_unit_display(),
            "warehouse": i.warehouse.name if i.warehouse else None,
            "stock_quantity": float(i.stock_quantity),
        }
        for i in ingredients
    ]
    return JsonResponse(data, safe=False)


@login_required
def api_products(request):
    """API endpoint que retorna lista de productos en formato JSON para Grid.js."""
    products = Product.objects.select_related("category", "dispatch_area").order_by(
        "name"
    )
    data = [
        {
            "id": p.id,
            "name": p.name,
            "category": p.category.name if p.category else None,
            "dispatch_area": p.dispatch_area.name if p.dispatch_area else None,
            "price": float(p.price),
        }
        for p in products
    ]
    return JsonResponse(data, safe=False)


@login_required
def api_categories(request):
    """API endpoint que retorna lista de categorías en formato JSON para Grid.js."""
    categories = ProductCategory.objects.all().order_by("name")
    data = [
        {
            "id": c.id,
            "name": c.name,
        }
        for c in categories
    ]
    return JsonResponse(data, safe=False)


@login_required
def api_dispatch_areas(request):
    """API endpoint que retorna lista de áreas de despacho en formato JSON para Grid.js."""
    areas = DispatchArea.objects.all().order_by("name")
    data = [
        {
            "id": a.id,
            "name": a.name,
        }
        for a in areas
    ]
    return JsonResponse(data, safe=False)


@login_required
def api_tables(request):
    """API endpoint que retorna lista de mesas en formato JSON para Grid.js."""
    tables = Table.objects.all().order_by("name")
    data = [
        {
            "id": t.id,
            "name": t.name,
        }
        for t in tables
    ]
    return JsonResponse(data, safe=False)


# ==========================
# 🧾 FACTURACIÓN
# ==========================


def user_can_invoice(user):
    """Verifica si el usuario puede facturar."""
    return user.has_perm("orders.add_invoice") or user.has_perm("orders.change_order")


def user_can_view_invoices(user):
    """Verifica si el usuario puede ver facturas."""
    return user.has_perm("orders.view_invoice")


def user_can_manage_cash_register(user):
    """Verifica si el usuario puede gestionar arqueo de caja."""
    allowed_groups = ["Cajero", "Supervisor", "Administrador"]
    return user.groups.filter(name__in=allowed_groups).exists() or user.is_superuser


def user_can_cashier(user):
    """Verifica si el usuario tiene rol de cajero (puede procesar cobros)."""
    return user.has_perm("orders.add_invoice")


@login_required
def table_send_to_billing(request, table_id):
    """Marca una mesa como pendiente de cobro (la envia a la cola del cajero)."""
    table = get_object_or_404(Table, id=table_id)
    orders = Order.objects.filter(table=table, is_paid=False)

    if not orders.exists():
        messages.info(request, f" No hay comandas pendientes para {table.name}.")
        return redirect("table_orders", table_id=table.id)

    if request.method == "POST":
        table.pending_billing = True
        table.save()
        messages.success(
            request,
            f" Mesa {table.name} enviada a caja para cobro.",
        )
        return redirect("table_list")

    return redirect("table_orders", table_id=table.id)


@login_required
@user_passes_test(user_can_invoice)
def invoice_table(request, table_id):
    """Genera una factura para todos los items de una mesa."""
    table = get_object_or_404(Table, id=table_id)
    orders = Order.objects.filter(table=table, is_paid=False).prefetch_related(
        "orderitem_set__product"
    )

    if not orders.exists():
        messages.info(request, f" No hay comandas pendientes para {table.name}.")
        return redirect("table_orders", table_id=table.id)

    consolidated = {}
    for order in orders:
        for item in order.orderitem_set.all():
            key = item.product.id
            if key in consolidated:
                consolidated[key]["quantity"] += item.quantity
                consolidated[key]["total"] += item.quantity * item.product.price
            else:
                consolidated[key] = {
                    "product": item.product,
                    "quantity": item.quantity,
                    "unit_price": item.product.price,
                    "total": item.quantity * item.product.price,
                }

    items_list = list(consolidated.values())
    total = sum(item["total"] for item in items_list)

    is_cashier = user_can_cashier(request.user)
    has_pending_billing = table.pending_billing

    if request.method == "POST":
        if not is_cashier:
            messages.error(request, " Solo un cajero puede procesar el cobro.")
            return redirect("table_orders", table_id=table.id)

        payment_method = request.POST.get("payment_method", "CONTADO")
        amount_received_str = request.POST.get("amount_received", "").strip()

        with transaction.atomic():
            subtotal = Decimal("0")
            items_data = []

            for order in orders:
                for item in order.orderitem_set.all():
                    line_total = item.quantity * item.product.price
                    subtotal += line_total
                    items_data.append(
                        {
                            "product": item.product,
                            "quantity": item.quantity,
                            "unit_price": item.product.price,
                            "total": line_total,
                        }
                    )

            if not items_data:
                messages.warning(request, " No hay productos para facturar.")
                return redirect("table_orders", table_id=table.id)

            active_register = CashRegister.get_active()
            if not active_register:
                messages.error(
                    request,
                    " No hay una caja abierta. Abre un turno en 'Caja' antes de facturar.",
                )
                return redirect("table_orders", table_id=table.id)

            amount_received = None
            if payment_method == "CONTADO":
                try:
                    amount_received = (
                        Decimal(amount_received_str) if amount_received_str else None
                    )
                except Exception:
                    messages.error(request, " Monto recibido inválido.")
                    return render(
                        request,
                        "invoices/invoice_form.html",
                        {
                            "table": table,
                            "items": items_list,
                            "total": total,
                            "is_cashier": is_cashier,
                        },
                    )

            invoice = Invoice.objects.create(
                table=table,
                user=request.user,
                cashier=request.user,
                subtotal=subtotal,
                total=subtotal,
                payment_method=payment_method,
                amount_received=amount_received,
            )

            for item_data in items_data:
                InvoiceItem.objects.create(
                    invoice=invoice,
                    product=item_data["product"],
                    quantity=item_data["quantity"],
                    unit_price=item_data["unit_price"],
                    total=item_data["total"],
                )

            orders.update(is_paid=True)
            table.pending_billing = False
            table.save()

            if active_register:
                if payment_method == "CONTADO":
                    active_register.total_contado += subtotal
                else:
                    active_register.total_credito += subtotal
                active_register.total_sales += subtotal
                active_register.save()

            messages.success(
                request,
                f" Factura #{invoice.invoice_number} generada por C$ {subtotal:.2f}",
            )

            if request.POST.get("print") == "yes":
                return redirect("print_invoice", invoice_id=invoice.id)

            return redirect("table_list")

    return render(
        request,
        "invoices/invoice_form.html",
        {
            "table": table,
            "items": items_list,
            "total": total,
            "is_cashier": is_cashier,
            "has_pending_billing": has_pending_billing,
        },
    )


@login_required
@user_passes_test(user_can_view_invoices)
def invoice_list(request):
    """Lista todas las facturas."""
    invoices = Invoice.objects.select_related("table", "user", "cashier")[:100]
    return render(request, "invoices/invoice_list.html", {"invoices": invoices})


@login_required
@user_passes_test(user_can_view_invoices)
def print_invoice(request, invoice_id):
    """Imprime una factura en formato térmico."""
    invoice = get_object_or_404(Invoice, id=invoice_id)
    items = invoice.get_items()
    company = Company.objects.first()

    return render(
        request,
        "invoices/print_invoice.html",
        {"invoice": invoice, "items": items, "company": company},
    )


@login_required
@user_passes_test(user_can_view_invoices)
def api_invoices(request):
    """API JSON: Lista de facturas."""
    invoices = (
        Invoice.objects.all()
        .select_related("table", "user", "cashier")
        .order_by("-created_at")[:100]
    )

    data = [
        {
            "id": i.id,
            "invoice_number": i.invoice_number,
            "table": i.table.name if i.table else "Sin mesa",
            "user": i.user.username if i.user else "—",
            "cashier": i.cashier.username if i.cashier else "—",
            "total": float(i.total),
            "payment_method": i.payment_method,
            "created_at": i.created_at.strftime("%d/%m/%Y %H:%M"),
        }
        for i in invoices
    ]
    return JsonResponse(data, safe=False)


# ==========================
# 💰 ARQUEO DE CAJA
# ==========================


@login_required
@user_passes_test(user_can_manage_cash_register)
def cash_register_list(request):
    """Lista todos los arqueos de caja."""
    cash_registers = CashRegister.objects.select_related("user")[:50]
    active = CashRegister.get_active()

    pending_tables = []
    for table in Table.objects.filter(pending_billing=True).order_by("name"):
        total_due = (
            Order.objects.filter(table=table, is_paid=False)
            .annotate(
                order_total=Sum(
                    F("orderitem__quantity") * F("orderitem__product__price")
                )
            )
            .aggregate(total=Sum("order_total"))["total"]
            or 0
        )
        pending_tables.append({"table": table, "total_due": total_due})

    return render(
        request,
        "cash/register_list.html",
        {
            "cash_registers": cash_registers,
            "active_register": active,
            "pending_tables": pending_tables,
        },
    )


@login_required
@user_passes_test(user_can_manage_cash_register)
def cash_register_open(request):
    """Abre un nuevo turno de caja."""
    active = CashRegister.get_active()

    if active:
        messages.info(
            request,
            f" Ya hay un turno abierto desde {active.created_at.strftime('%H:%M')}",
        )
        return redirect("cash_register_detail", register_id=active.id)

    if request.method == "POST":
        try:
            opening_amount = Decimal(request.POST.get("opening_amount", "0"))
        except Exception:
            messages.error(request, " Monto de apertura inválido.")
            return redirect("cash_register_open")

        cash_register = CashRegister.objects.create(
            user=request.user,
            opening_amount=opening_amount,
        )

        messages.success(
            request, f" Turno #{cash_register.id} abierto con C$ {opening_amount:.2f}"
        )
        return redirect("cash_register_detail", register_id=cash_register.id)

    return render(request, "cash/register_open.html")


@login_required
@user_passes_test(user_can_manage_cash_register)
def cash_register_detail(request, register_id):
    """Muestra el detalle del arqueo actual."""
    cash_register = get_object_or_404(CashRegister, id=register_id)
    return render(request, "cash/register_detail.html", {"register": cash_register})


@login_required
@user_passes_test(user_can_manage_cash_register)
def cash_register_close(request, register_id):
    """Cierra un turno de caja."""
    cash_register = get_object_or_404(CashRegister, id=register_id)

    if cash_register.closing_time:
        messages.info(request, " Este turno ya está cerrado.")
        return redirect("cash_register_list")

    if request.method == "POST":
        try:
            closing_amount = Decimal(request.POST.get("closing_amount", "0"))
        except Exception:
            messages.error(request, " Monto de cierre inválido.")
            return redirect("cash_register_close", register_id=register_id)

        notes = request.POST.get("notes", "").strip()

        cash_register.closing_amount = closing_amount
        cash_register.closing_time = timezone.now()
        cash_register.notes = notes
        cash_register.save()

        expected = cash_register.opening_amount + cash_register.total_contado
        difference = closing_amount - expected

        if difference == 0:
            messages.success(request, " Turno cerrado. ¡Caja cuadrada!")
        elif difference > 0:
            messages.warning(request, f" Sobran C$ {difference:.2f} en caja.")
        else:
            messages.warning(request, f" Faltan C$ {abs(difference):.2f} en caja.")

        return redirect("cash_register_list")

    expected = cash_register.opening_amount + cash_register.total_contado
    return render(
        request,
        "cash/register_close.html",
        {"register": cash_register, "expected": expected},
    )


@login_required
def api_cash_register_status(request):
    """API: Retorna si hay un turno activo."""
    active = CashRegister.get_active()
    if active:
        data = {
            "active": True,
            "id": active.id,
            "user": active.user.username if active.user else "—",
            "opening_amount": float(active.opening_amount),
            "total_sales": float(active.total_sales),
            "total_contado": float(active.total_contado),
            "total_credito": float(active.total_credito),
            "created_at": active.created_at.strftime("%H:%M"),
        }
    else:
        data = {"active": False}
    return JsonResponse(data)
