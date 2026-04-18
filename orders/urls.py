from django.urls import path

from . import views


def gridjs_demo(request):
    """Vista de demostración para Grid.js."""
    from django.shortcuts import render

    return render(request, "gridjs_demo.html")


urlpatterns = [
    # ==========================
    # POS - Mesas y Comandas
    # ==========================
    path("pos/", views.table_list, name="table_list"),
    path("pos/table/<int:table_id>/", views.table_orders, name="table_orders"),
    path(
        "pos/table/<int:table_id>/pay/", views.mark_table_paid, name="mark_table_paid"
    ),
    path("pos/table/<int:table_id>/new/", views.create_order, name="create_order"),
    path("pos/order/<int:order_id>/", views.order_detail, name="order_detail"),
    path("pos/order/<int:order_id>/edit/", views.edit_order, name="edit_order"),
    path("pos/order/<int:order_id>/print/", views.print_order, name="print_order"),
    # Alias para compatibilidad
    path("mesa/<int:table_id>/", views.table_orders, name="table_orders_alt"),
    path(
        "mesa/<int:table_id>/pagar/", views.mark_table_paid, name="mark_table_paid_alt"
    ),
    path("mesa/<int:table_id>/nueva/", views.create_order, name="create_order_alt"),
    path("orden/<int:order_id>/", views.order_detail, name="order_detail_alt"),
    path("orden/<int:order_id>/editar/", views.edit_order, name="edit_order_alt"),
    path("orden/<int:order_id>/imprimir/", views.print_order, name="print_order_alt"),
    # ==========================
    # Orders - Historial y Comandas
    # ==========================
    path("orders/history/", views.order_history, name="order_history"),
    path("orders/daily/", views.daily_report, name="daily_report"),
    path("orders/", views.report_orders, name="report_orders"),
    path("orders/csv/", views.export_orders_csv, name="export_orders_csv"),
    # Alias español
    path("historial/", views.order_history, name="order_history_alt"),
    path("reporte/", views.daily_report, name="daily_report_alt"),
    path("reportes/comandas/", views.report_orders, name="report_orders_alt"),
    path(
        "reportes/comandas/csv/", views.export_orders_csv, name="export_orders_csv_alt"
    ),
    # ==========================
    # Menu - Productos, Categorías, Áreas
    # ==========================
    path("menu/products/", views.product_list, name="product_list"),
    path("menu/products/new/", views.product_create, name="product_create"),
    path(
        "menu/products/<int:product_id>/edit/", views.product_edit, name="product_edit"
    ),
    path(
        "menu/products/<int:product_id>/delete/",
        views.product_delete,
        name="product_delete",
    ),
    path(
        "menu/products/<int:product_id>/recipes/",
        views.product_recipes,
        name="product_recipes",
    ),
    path("menu/categories/", views.category_list, name="category_list"),
    path("menu/categories/new/", views.category_create, name="category_create"),
    path(
        "menu/categories/<int:category_id>/edit/",
        views.category_edit,
        name="category_edit",
    ),
    path(
        "menu/categories/<int:category_id>/delete/",
        views.category_delete,
        name="category_delete",
    ),
    path("menu/dispatch-areas/", views.dispatch_area_list, name="dispatch_area_list"),
    path(
        "menu/dispatch-areas/new/",
        views.dispatch_area_create,
        name="dispatch_area_create",
    ),
    path(
        "menu/dispatch-areas/<int:area_id>/edit/",
        views.dispatch_area_edit,
        name="dispatch_area_edit",
    ),
    path(
        "menu/dispatch-areas/<int:area_id>/delete/",
        views.dispatch_area_delete,
        name="dispatch_area_delete",
    ),
    # Alias español
    path("productos/", views.product_list, name="product_list_alt"),
    path("productos/nuevo/", views.product_create, name="product_create_alt"),
    path(
        "productos/<int:product_id>/editar/",
        views.product_edit,
        name="product_edit_alt",
    ),
    path(
        "productos/<int:product_id>/eliminar/",
        views.product_delete,
        name="product_delete_alt",
    ),
    path(
        "productos/<int:product_id>/recetas/",
        views.product_recipes,
        name="product_recipes_alt",
    ),
    path("categorias/", views.category_list, name="category_list_alt"),
    path("categorias/nueva/", views.category_create, name="category_create_alt"),
    path(
        "categorias/<int:category_id>/editar/",
        views.category_edit,
        name="category_edit_alt",
    ),
    path(
        "categorias/<int:category_id>/eliminar/",
        views.category_delete,
        name="category_delete_alt",
    ),
    path("areas-despacho/", views.dispatch_area_list, name="dispatch_area_list_alt"),
    path(
        "areas-despacho/nueva/",
        views.dispatch_area_create,
        name="dispatch_area_create_alt",
    ),
    path(
        "areas-despacho/<int:area_id>/editar/",
        views.dispatch_area_edit,
        name="dispatch_area_edit_alt",
    ),
    path(
        "areas-despacho/<int:area_id>/eliminar/",
        views.dispatch_area_delete,
        name="dispatch_area_delete_alt",
    ),
    # ==========================
    # 🍽️ GESTIÓN DE MESAS
    # ==========================
    path("menu/tables/", views.table_management_list, name="table_management_list"),
    path(
        "menu/tables/new/",
        views.table_management_create,
        name="table_management_create",
    ),
    path(
        "menu/tables/<int:table_id>/",
        views.table_management_detail,
        name="table_management_detail",
    ),
    path(
        "menu/tables/<int:table_id>/edit/",
        views.table_management_edit,
        name="table_management_edit",
    ),
    path(
        "menu/tables/<int:table_id>/delete/",
        views.table_management_delete,
        name="table_management_delete",
    ),
    path(
        "menu/tables/<int:table_id>/restore/",
        views.table_management_restore,
        name="table_management_restore",
    ),
    # Alias español
    path("mesas/", views.table_management_list, name="table_management_list_alt"),
    path(
        "mesas/nueva/",
        views.table_management_create,
        name="table_management_create_alt",
    ),
    path(
        "mesas/<int:table_id>/",
        views.table_management_detail,
        name="table_management_detail_alt",
    ),
    path(
        "mesas/<int:table_id>/editar/",
        views.table_management_edit,
        name="table_management_edit_alt",
    ),
    path(
        "mesas/<int:table_id>/eliminar/",
        views.table_management_delete,
        name="table_management_delete_alt",
    ),
    path(
        "mesas/<int:table_id>/restaurar/",
        views.table_management_restore,
        name="table_management_restore_alt",
    ),
    # ==========================
    # Inventory - Ingredientes y Movimientos
    # ==========================
    path("inventory/ingredients/", views.ingredient_list, name="ingredient_list"),
    path(
        "inventory/ingredients/new/", views.ingredient_create, name="ingredient_create"
    ),
    path(
        "inventory/ingredients/<int:ingredient_id>/edit/",
        views.ingredient_edit,
        name="ingredient_edit",
    ),
    path(
        "inventory/ingredients/<int:ingredient_id>/delete/",
        views.ingredient_delete,
        name="ingredient_delete",
    ),
    path("inventory/adjust/", views.inventory_movement, name="inventory_movement"),
    path(
        "inventory/purchase/", views.purchase_ingredients, name="purchase_ingredients"
    ),
    # Alias español
    path("ingredientes/", views.ingredient_list, name="ingredient_list_alt"),
    path("ingredientes/nuevo/", views.ingredient_create, name="ingredient_create_alt"),
    path(
        "ingredientes/<int:ingredient_id>/editar/",
        views.ingredient_edit,
        name="ingredient_edit_alt",
    ),
    path(
        "ingredientes/<int:ingredient_id>/eliminar/",
        views.ingredient_delete,
        name="ingredient_delete_alt",
    ),
    path(
        "ingredientes/movimientos/",
        views.inventory_movement,
        name="inventory_movement_alt",
    ),
    path(
        "ingredientes/compras/",
        views.purchase_ingredients,
        name="purchase_ingredients_alt",
    ),
    # ==========================
    # Reports - Reportes
    # ==========================
    path("reports/", views.reports_index, name="reports_index"),
    path("reports/inventory/", views.report_inventory, name="report_inventory"),
    path(
        "reports/inventory/print/",
        views.print_inventory_report,
        name="print_inventory_report",
    ),
    path(
        "reports/inventory/csv/",
        views.export_inventory_csv,
        name="export_inventory_csv",
    ),
    path("reports/movements/", views.report_movements, name="report_movements"),
    path(
        "reports/movements/csv/",
        views.export_movements_csv,
        name="export_movements_csv",
    ),
    path(
        "reports/sales-by-product/",
        views.sales_report_by_product,
        name="sales_report_by_product",
    ),
    path(
        "reports/sales-by-product/csv/",
        views.export_sales_by_product_csv,
        name="export_sales_by_product_csv",
    ),
    # Alias español
    path(
        "reportes/saldo-ingredientes/",
        views.report_inventory,
        name="report_inventory_alt",
    ),
    path(
        "reportes/saldo-ingredientes/imprimir/",
        views.print_inventory_report,
        name="print_inventory_report_alt",
    ),
    path(
        "reportes/saldo-ingredientes/csv/",
        views.export_inventory_csv,
        name="export_inventory_csv_alt",
    ),
    path(
        "reportes/movimiento-ingredientes/",
        views.report_movements,
        name="report_movements_alt",
    ),
    path(
        "reportes/movimiento-ingredientes/csv/",
        views.export_movements_csv,
        name="export_movements_csv_alt",
    ),
    path(
        "reportes/ventas-producto/",
        views.sales_report_by_product,
        name="sales_report_by_product_alt",
    ),
    path(
        "reportes/ventas-producto/csv/",
        views.export_sales_by_product_csv,
        name="export_sales_by_product_csv_alt",
    ),
    # ==========================
    # Settings - Configuración
    # ==========================
    path("settings/company/", views.company_settings, name="company_settings"),
    # Alias español
    path("empresa/configuracion/", views.company_settings, name="company_settings_alt"),
    # ==========================
    # Dashboard (raíz)
    # ==========================
    path("dashboard/", views.dashboard, name="dashboard"),
    path("", views.table_list, name="table_list_default"),
    # ==========================
    # API Grid.js - Endpoints JSON
    # ==========================
    path("api/ingredients/", views.api_ingredients, name="api_ingredients"),
    path("api/products/", views.api_products, name="api_products"),
    path("api/categories/", views.api_categories, name="api_categories"),
    path("api/dispatch-areas/", views.api_dispatch_areas, name="api_dispatch_areas"),
    path("api/tables/", views.api_tables, name="api_tables"),
    path("api/orders/", views.api_orders, name="api_orders"),
    path("api/movements/", views.api_movements, name="api_movements"),
    path("api/inventory/", views.api_inventory, name="api_inventory"),
    path("api/sales-today/", views.api_sales_today, name="api_sales_today"),
    path(
        "api/sales-by-product/", views.api_sales_by_product, name="api_sales_by_product"
    ),
    path("api/orders-report/", views.api_orders_report, name="api_orders_report"),
    # ==========================
    # 🧾 FACTURACIÓN
    # ==========================
    path(
        "pos/table/<int:table_id>/invoice/", views.invoice_table, name="invoice_table"
    ),
    path("invoices/", views.invoice_list, name="invoice_list"),
    path("invoices/<int:invoice_id>/print/", views.print_invoice, name="print_invoice"),
    path("api/invoices/", views.api_invoices, name="api_invoices"),
    # ==========================
    # 💰 ARQUEO DE CAJA
    # ==========================
    path("cash/", views.cash_register_list, name="cash_register_list"),
    path("cash/open/", views.cash_register_open, name="cash_register_open"),
    path(
        "cash/<int:register_id>/",
        views.cash_register_detail,
        name="cash_register_detail",
    ),
    path(
        "cash/<int:register_id>/close/",
        views.cash_register_close,
        name="cash_register_close",
    ),
    path(
        "cash/status/", views.api_cash_register_status, name="api_cash_register_status"
    ),
    # ==========================
    # Demo Grid.js
    # ==========================
    path("demo/gridjs/", gridjs_demo, name="gridjs_demo"),
]
