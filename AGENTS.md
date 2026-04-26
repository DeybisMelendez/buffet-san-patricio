# Agente - Buffet San Patricio

Documento de referencia rápida para agentes de IA que trabajan en el proyecto Django **Buffet San Patricio**.

---

## Descripción del Proyecto

**Buffet San Patricio** es un sistema de gestión integral para restaurantes tipo buffet. Maneja mesas, comandas, inventario con control de recetas, facturación, arqueo de caja y reportes de ventas.

### Funcionalidades Principales

- **POS (Mesas y Comandas)**: Gestión de mesas, creación de órdenes, impresión de comandas
- **Menú**: Productos, categorías, áreas de despacho, recetas (producto-ingredientes)
- **Inventario**: Ingredientes, movimientos de entrada/salida, ajuste de stock, conversor de alimentos
- **Facturación**: Facturas con múltiples métodos de pago
- **Arqueo de Caja**: Control de turnos y cuadre diario
- **Reportes**: Ventas por producto, inventario, comandas, exportaciones CSV
- **Dashboard**: Panel principal con información adaptiva al rol

---

## Resumen Técnico

| Componente | Tecnología |
|------------|------------|
| Framework | Django 5.2.7 |
| Base de datos | SQLite (`db.sqlite3`) |
| Python | 3.12+ |
| Frontend | HTML + JavaScript puro (vanilla) |
| CSS | Bootstrap 5 (solo clases, sin CSS custom) |
| Tablas | GridJS |
| Iconos | Google Material Icons (CDN) |
| Localización | Español (Nicaragua) |

---

## Filosofía de Desarrollo

- **Código**: Todos los identificadores en inglés (clases, funciones, variables)
- **Documentación**: Comentarios y docstrings en español
- **Interfaz**: Usuario completamente en español
- **Simplicidad**: Priorizar soluciones simples y mantenibles
- **JavaScript**: Puro vanilla JS, sin frameworks (no AlpineJS, no jQuery)
- **CSS**: Bootstrap 5 con clases utilities, evitar CSS personalizado

---

## Estructura del Proyecto

```
buffet-san-patricio/
├── core/                  # Configuración Django
├── orders/                # App principal
│   ├── models.py         # ~380 líneas, 17 modelos
│   ├── views.py          # ~3100 líneas de vistas
│   ├── urls.py           # URLs con aliases inglés/español
│   └── forms.py          # Formularios
├── users/                # App de usuarios
│   ├── permissions.py    # 5 grupos con permisos predefinidos
│   └── utils.py          # Helpers de verificación de roles
├── templates/            # Templates HTML (BAP)
│   ├── layout.html       # Template base
│   ├── pos/              # Mesas y comandas
│   ├── menu/             # Gestión de productos
│   ├── inventory/        # Inventario
│   ├── invoices/          # Facturación
│   ├── cash/             # Arqueo de caja
│   └── reports/          # Reportes
├── static/js/            # JavaScript vanilla
│   ├── global.js         # Utilidades de la app (470 líneas)
│   ├── common.js         # Helpers comunes (42 líneas)
│   ├── grid-utils.js     # Utilities de GridJS (150 líneas)
│   └── grid.js           # Inicialización de GridJS (209 líneas)
└── docs/                 # Documentación
    ├── SYSTEM.md         # Documentación técnica completa
    ├── GRIDJS.md         # Guía de GridJS
    ├── BOOTSTRAP.md      # Guía de Bootstrap
    └── FRONTEND.md       # Directrices frontend
```

---

## Módulos del Sistema

### 1. POS - Mesas y Comandas
- Lista de mesas con totales pendientes
- Crear/editar órdenes por mesa
- Marcar órdenes como pagadas
- Impresión de comandas para cocina
- Cambiar mesa o mesero asignado

### 2. Menú - Productos
- CRUD de productos con categoría y área de despacho
- Gestión de recetas (relación producto-ingrediente)
- CRUD de categorías y áreas de despacho
- Gestión de mesas (CRUD completo)

### 3. Inventario
- CRUD de ingredientes con unidades de medida
- Movimientos de inventario (entradas/salidas)
- Ajuste de inventario físico
- Registro de compras de ingredientes
- CRUD de bodegas/almacenes
- **Recetas de Conversión** (FoodRecipe): Conversión de ingredientes
- **Conversor de Alimentos**: Calculadora de recetas

### 4. Facturación
- Generación de facturas consolidadas por mesa
- Métodos de pago: EFECTIVO, TARJETA_CREDITO, TARJETA_DEBITO, TRANSFERENCIA, OTRO, PENDIENTE
- Cambio para pagos en efectivo
- Facturación de órdenes pendientes
- Actualización de pagos
- Impresión de facturas

### 5. Arqueo de Caja
- Apertura y cierre de turnos
- Control detallado por método de pago (contado, tarjeta crédito, débito, transferencia, otros, pendiente)
- Cálculo de diferencia (sobra/falta)
- Lista de facturas pendientes

### 6. Reportes
- Saldo de inventario
- Movimientos de inventario
- Ventas por producto
- Comandas por período
- Ventas del día
- Exportación CSV

### 7. Dashboard
- Panel principal con información adaptiva al rol
- Gráfico de ventas últimos 7 días
- Ingredientes con stock bajo
- Órdenes pendientes por mesa

---

## Modelos de Datos

### Modelos Principales

| Modelo | Descripción |
|--------|-------------|
| `Table` | Mesas del restaurante (soft delete) |
| `ProductCategory` | Categorías de productos (soft delete) |
| `DispatchArea` | Áreas de despacho (soft delete) |
| `Warehouse` | Bodegas de almacenamiento (soft delete) |
| `Product` | Productos del menú (soft delete) |
| `Ingredient` | Ingredientes del inventario (soft delete) |
| `ProductIngredient` | Recetas (relación producto-ingrediente) |
| `IngredientMovement` | Movimientos de inventario |
| `Order` | Órdenes/Comandas |
| `OrderItem` | Items de una orden |
| `Invoice` | Facturas |
| `InvoiceItem` | Items de una factura |
| `CashRegister` | Arqueos de caja |
| `Company` | Datos de la empresa |
| `FoodRecipe` | Recetas de conversión (soft delete) |
| `FoodRecipeItem` | Ingredientes de receta de conversión |

### Soft Delete

Todos los modelos principales heredan de `SoftDeleteModel`:
- Campo `is_deleted`: Boolean para marca de eliminación
- Campo `deleted_at`: Fecha/hora de eliminación
- Manager `objects`: Excluye eliminados
- Manager `all_objects`: Incluye todos

```python
class SoftDeleteModel(models.Model):
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = SoftDeleteManager()  # Solo no eliminados
    all_objects = AllObjectsManager()  # Todos

    def soft_delete(self):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()

    def restore(self):
        self.is_deleted = False
        self.deleted_at = None
        self.save()
```

---

## Sistema de Permisos

### Grupos Fijos

| Grupo | Descripción |
|-------|-------------|
| `Servicio` | Meseros - crear/ver órdenes |
| `Cocinero` | Cocina - ver órdenes, usar conversor |
| `Cajero` | Caja - facturación y arqueo |
| `Supervisor` | Encargados - inventario, cierres |
| `Administrador` | Gerencia - acceso total |

### Funciones de Verificación

```python
# users/utils.py
is_servicio(user)          # Grupo Servicio
is_supervisor(user)        # Grupo Supervisor
is_administrador(user)     # Grupo Administrador
is_cocinero(user)          # Grupo Cocinero
is_cajero(user)            # Grupo Cajero
has_valid_role(user)       # Cualquier grupo válido
user_can_mark_paid(user)   # Puede marcar órdenes pagadas
user_can_manage_menu(user) # Puede gestionar menú
user_can_view_inventory(user)       # Puede ver inventario
user_can_add_inventory_movement(user)  # Puede registrar movimientos
user_can_manage_inventory_full(user)   # Gestión completa inventario
user_can_view_reports(user)          # Puede ver reportes
user_can_use_food_converter(user)    # Puede usar conversor
user_can_manage_food_recipes(user)   # Puede gestionar recetas
user_can_view_sales_report(user)     # Puede ver reporte de ventas
```

---

## URLs del Sistema

### Aliases

Todas las URLs tienen aliases en inglés y español. **Usar aliases en inglés en el código**.

### Principales

| URL | Alias inglés | Alias español | Descripción |
|-----|--------------|---------------|-------------|
| `/pos/` | `table_list` | - | Lista de mesas |
| `/pos/table/<id>/` | `table_orders` | `mesa/<id>/` | Órdenes de mesa |
| `/pos/table/<id>/new/` | `create_order` | `mesa/<id>/nueva/` | Crear orden |
| `/pos/table/<id>/pay/` | `mark_table_paid` | `mesa/<id>/pagar/` | Facturar mesa |
| `/pos/order/<id>/` | `order_detail` | `orden/<id>/` | Detalle de orden |
| `/pos/order/<id>/edit/` | `edit_order` | `orden/<id>/editar/` | Editar orden |
| `/menu/products/` | `product_list` | `productos/` | Productos |
| `/menu/products/<id>/recipes/` | `product_recipes` | `productos/<id>/recetas/` | Recetas |
| `/menu/tables/` | `table_management_list` | `mesas/` | Gestión de mesas |
| `/inventory/ingredients/` | `ingredient_list` | `ingredientes/` | Ingredientes |
| `/inventory/adjust/` | `inventory_movement` | `ingredientes/movimientos/` | Ajuste inventario |
| `/inventory/purchase/` | `purchase_ingredients` | `ingredientes/compras/` | Compras |
| `/inventory/warehouses/` | `warehouse_list` | `bodegas/` | Bodegas |
| `/inventory/recipes/` | `food_recipe_list` | `recetas/` | Recetas conversión |
| `/inventory/convert/` | `food_converter` | `conversor/` | Conversor alimentos |
| `/invoices/` | `invoice_list` | - | Facturas |
| `/cash/` | `cash_register_list` | - | Arqueo de caja |
| `/cash/open/` | `cash_register_open` | - | Abrir turno |
| `/cash/<id>/close/` | `cash_register_close` | - | Cerrar turno |
| `/reports/` | `reports_index` | - | Panel reportes |
| `/reports/inventory/` | `report_inventory` | `reportes/saldo-ingredientes/` | Saldo inventario |
| `/reports/sales-by-product/` | `sales_report_by_product` | `reportes/ventas-producto/` | Ventas por producto |
| `/dashboard/` | `dashboard` | - | Dashboard |
| `/empresa/configuracion/` | `company_settings` | - | Config empresa |
| `/demo/gridjs/` | `gridjs_demo` | - | Demo GridJS |

---

## API Endpoints JSON

| Endpoint | Alias | Descripción |
|----------|-------|-------------|
| `/api/ingredients/` | `api_ingredients` | Ingredientes |
| `/api/products/` | `api_products` | Productos |
| `/api/categories/` | `api_categories` | Categorías |
| `/api/dispatch-areas/` | `api_dispatch_areas` | Áreas despacho |
| `/api/tables/` | `api_tables` | Mesas |
| `/api/orders/` | `api_orders` | Órdenes |
| `/api/invoices/` | `api_invoices` | Facturas |
| `/api/movements/` | `api_movements` | Movimientos inventario |
| `/api/inventory/` | `api_inventory` | Inventario paginado |
| `/api/sales-by-product/` | `api_sales_by_product` | Ventas por producto |
| `/api/orders-report/` | `api_orders_report` | Reporte de órdenes |
| `/api/sales-today/` | `api_sales_today` | Ventas del día |
| `/api/cash/status/` | `api_cash_register_status` | Estado de caja |

### Formato de Respuesta

```json
{
  "count": 150,
  "results": [
    {"id": 1, "campo1": "valor1", "campo2": "valor2"}
  ]
}
```

### Parámetros de Query

| Parámetro | Descripción |
|-----------|-------------|
| `page` | Número de página (empezando en 1) |
| `limit` | Registros por página (0 = todos) |
| `search` | Término de búsqueda |
| `sort` | Campo y dirección (`campo,asc` o `campo,desc`) |

---

## Convenciones de Código

### Imports

Orden obligatorio con líneas en blanco entre grupos:

```python
# 1. Stdlib
import csv
from datetime import datetime, time, timedelta
from decimal import Decimal

# 2. Third-party
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import transaction
from django.db.models import F, Sum

# 3. Local
from .models import (
    CashRegister, Company, Ingredient, IngredientMovement,
    Invoice, InvoiceItem, Order, OrderItem, Product,
    ProductCategory, ProductIngredient, Table
)
```

### Nomenclatura

| Tipo | Convención | Ejemplo |
|------|------------|---------|
| Clases | CamelCase | `ProductCategory`, `CashRegister` |
| Funciones/métodos | snake_case | `parse_date_range`, `get_total` |
| Variables | snake_case | `total_due`, `order_items` |
| Constantes | UPPER_SNAKE_CASE | `UNITS`, `PAYMENT_TYPES` |
| Archivos JS | kebab-case | `grid-utils.js`, `common.js` |

### Strings

- Usar comillas dobles (`"`) para literales
- Usar f-strings para formateo: `f"Mesa {self.name}"`
- Interfaz en español: `verbose_name="Nombre"`, `messages.success(request, "✅ Pedido creado")`

### Vistas

```python
@login_required
@user_passes_test(has_valid_role)
def table_list(request):
    """Muestra todas las mesas y su total pendiente."""
    tables = Table.objects.all().order_by("name")
    return render(request, "pos/table_list.html", {"tables": tables})
```

### Templates

- Extender de `layout.html`
- Usar bloques `{% block title %}` y `{% block body %}`
- CSS adicional con `{% block extra_css %}`
- JS adicional con `{% block extra_js %}`
- Iconos: `<span class="material-icons">icon_name</span>`

---

## JavaScript

### Stack

- **JavaScript puro**: Sin frameworks, sin AlpineJS, sin jQuery
- **Bootstrap 5**: Solo CSS (clases utilities), sin JS de Bootstrap
- **GridJS**: Tablas interactivas
- **SheetJS**: Exportación a Excel

### Archivos JS

| Archivo | Líneas | Propósito |
|---------|--------|-----------|
| `global.js` | 470 | Utilidades: facturas, inventario, recetas, converter |
| `common.js` | 42 | Helpers comunes |
| `grid-utils.js` | 150 | Exportar/copiar datos de GridJS |
| `grid.js` | 209 | Inicialización de tablas GridJS |

### Funciones Globales

```javascript
// Facturas
window.initInvoiceForm(total)

// Inventario
window.initInventoryAdjust()

// Recetas de producto
window.initProductRecipes(initialCount)

// Recetas de conversión
window.initFoodConverter(recipes)
window.initFoodRecipeForm(initialInputCount, initialOutputCount)

// GridJS
window.GridUtils.copyToClipboard()
window.GridUtils.exportToExcel(filename)
window.GridUtils.addToolbar(containerId, gridContainerId, filename)
window.GridJS.init(tableId, apiUrl, columns, options)
window.GridJS.initLocal(tableId, data, columns, options)

// Impresión
window.printOrder(orderId, iframeId)
window.printInventoryReport(iframeId)
```

---

## Linting y Formateo

**Importante**: Ejecutar en archivos individuales modificados, no en todo el proyecto.

### Python

```bash
# Formatear código
black path/to/file.py

# Ordenar imports
isort path/to/file.py

# Verificar estilo
flake8 path/to/file.py --max-line-length=100

# Type checking
mypy path/to/file.py
```

### HTML Templates

```bash
# Formatear templates
djlint --reformat path/to/template.html
```

---

## Errores Comunes

1. **No usar `transaction.atomic`** en operaciones que modifican múltiples tablas
2. **No validar datos del POST** antes de usarlos
3. **No usar `get_object_or_404`** para obtener objetos por ID
4. **Olvidar `@login_required`** en vistas
5. **Olvidar verificar permisos** con `@user_passes_test`
6. **Usar `.objects` en modelos con soft delete** - usar `objects` solo, no `all_objects` a menos que sea necesario
7. **Confundir `quantity` positivo/negativo** - positivo es ingreso, negativo es salida

---

## Patrones de Negocio

### Crear Orden con Receta

```python
# Al crear OrderItem, se descuenta automáticamente del inventario
class OrderItem(models.Model):
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Descontar ingredientes según receta
        for prod_ing in ProductIngredient.objects.filter(product=self.product):
            total_required = prod_ing.quantity * Decimal(self.quantity)
            IngredientMovement.objects.create(
                ingredient=prod_ing.ingredient,
                quantity=-total_required,
                user=self.order.user,
                reason=f"Uso en {self.product.name}, Comanda #{self.order.id}",
            )
```

### Facturación Consolidada

1. Se consolidan todos los items de las órdenes pendientes de una mesa
2. Se crea una Invoice con los items
3. Se marcan las órdenes como pagadas
4. Se actualiza el arqueo de caja según método de pago

### Arqueo de Caja

- Solo un turno activo a la vez (`CashRegister.get_active()`)
- Cada método de pago acumula en su campo correspondiente
- Al cerrar, se calcula diferencia: `closing_amount - (opening_amount + total_contado)`

---

## Recursos

- [docs/SYSTEM.md](docs/SYSTEM.md) - Documentación técnica completa
- [docs/GRIDJS.md](docs/GRIDJS.md) - Guía de GridJS para tablas
- [docs/BOOTSTRAP.md](docs/BOOTSTRAP.md) - Guía de estilos Bootstrap
- [docs/FRONTEND.md](docs/FRONTEND.md) - Directrices generales frontend
- [Django Docs](https://docs.djangoproject.com/en/5.2/)
- [Bootstrap 5](https://getbootstrap.com/docs/5.3/)
- [GridJS](https://gridjs.io/)
- [Material Icons](https://fonts.google.com/icons)

---

## Resumen para Agentes

1. **NO escribir tests Python** – verificar manualmente en el navegador
2. **Código en inglés**, comentarios/documentación en español
3. **Interfaz en español** (labels, mensajes, verbose_name)
4. **Simplicidad** – evitar soluciones complejas
5. **JavaScript puro** – no usar AlpineJS, no usar jQuery
6. **Bootstrap para CSS** – usar clases, evitar CSS custom
7. **Seguir patrones existentes** en `orders/views.py` y `orders/models.py`
8. **Ejecutar linting** (`black`, `flake8`, `djlint`) en archivos modificados
9. **Usar GridJS** para tablas con búsqueda/paginación
10. **Credenciales en `.secret`** – no hardcodear
11. **Consultar docs/SYSTEM.md** para entender el sistema completo

---

_Last updated: 2026-04-26_