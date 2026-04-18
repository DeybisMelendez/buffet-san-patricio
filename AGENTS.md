# Agente - Buffet San Patricio

Este documento proporciona instrucciones y guías para agentes de IA que trabajan en el proyecto Django **Buffet San Patricio**.

## Descripción del Proyecto

**Buffet San Patricio** es un sistema de gestión integral para restaurantes tipo buffet. Maneja mesas, comandas, inventario con control de recetas, facturación, arqueo de caja y reportes de ventas.

### Funcionalidades Principales

- **POS (Mesas y Comandas)**: Gestión de mesas, creación de órdenes, impresión de comandas
- **Menú**: Productos, categorías, áreas de despacho, recetas (producto-ingredientes)
- **Inventario**: Ingredientes, movimientos de entrada/salida, ajuste de stock
- **Facturación**: Facturas con métodos de pago (contado/crédito)
- **Arqueo de Caja**: Control de turnos y cuadre diario
- **Reportes**: Ventas por producto, inventario, comandas, exportaciones CSV
- **Dashboard**: Panel principal con gráficos adaptivos al rol

## Resumen del Proyecto

- **Framework**: Django 5.2.7
- **Base de datos**: SQLite (`db.sqlite3`)
- **Frontend**: AlpineJS + Bootstrap 5 (CDN)
- **Tablas interactivas**: GridJS
- **Iconos**: Google Material Icons (CDN)
- **Lenguaje**: Python 3.12+
- **Localización**: Español (Nicaragua)

## Filosofía de Desarrollo

- **Código**: Todos los identificadores en inglés (clases, funciones, variables)
- **Documentación**: Comentarios y docstrings en español
- **Interfaz**: Usuario completamente en español (etiquetas, mensajes, verbose_name)
- **Simplicidad**: Priorizar soluciones simples y mantenibles
- **Prácticidad**: Enfocarse en soluciones funcionales y fáciles de entender

## Estructura del Proyecto

```
buffet-san-patricio/
├── core/                  # Configuración Django
├── orders/                # App principal
│   ├── models.py         # Modelos: Table, Product, Order, Invoice, etc.
│   ├── views.py          # ~2200 líneas de vistas y lógica de negocio
│   └── urls.py           # URLs con aliases inglés y español
├── users/                 # App de usuarios
│   ├── permissions.py    # 5 grupos con permisos predefinidos
│   └── utils.py          # Helpers de verificación de roles
├── templates/             # Templates HTML
│   ├── layout.html       # Template base
│   ├── pos/              # Mesas y comandas
│   ├── menu/             # Gestión de productos
│   ├── inventory/        # Inventario
│   ├── invoices/         # Facturación
│   ├── cash/             # Arqueo de caja
│   └── reports/          # Reportes
└── docs/
    ├── SYSTEM.md         # Documentación completa del sistema
    └── frontend.md       # Guías de frontend
```

## Módulos del Sistema

### 1. POS - Mesas y Comandas
- Lista de mesas con totales pendientes
- Crear/editar órdenes por mesa
- Marcar órdenes como pagadas
- Impresión de comandas

### 2. Menú - Productos
- CRUD de productos con categoría y área de despacho
- Gestión de recetas (relación producto-ingredientes)
- CRUD de categorías y áreas de despacho

### 3. Inventario
- CRUD de ingredientes con unidades de medida
- Movimientos de inventario (entradas/salidas)
- Ajuste de inventario físico
- Registro de compras

### 4. Facturación
- Generación de facturas consolidadas por mesa
- Métodos de pago: CONTADO y CREDITO
- Impresión de facturas

### 5. Arqueo de Caja
- Apertura y cierre de turnos
- Control de ventas contado/crédito
- Cálculo de diferencia (sobra/falta)

### 6. Reportes
- Saldo de inventario
- Movimientos de inventario
- Ventas por producto
- Comandas por período
- Exportación CSV

## Sistema de Permisos

### Grupos Fijos

| Grupo | Descripción |
|-------|-------------|
| `Servicio` | Meseros - crear/ver órdenes |
| `Cocinero` | Cocina - ver órdenes e ingredientes |
| `Cajero` | Caja - facturación y arqueo |
| `Supervisor` | Encargados - inventario y cierres |
| `Administrador` | Gerencia - acceso total |

Los permisos se definen en `users/permissions.py` y se asignan a cada grupo.

## Comandos de Desarrollo

### Django

```bash
# Servidor de desarrollo
python manage.py runserver

# Aplicar migraciones
python manage.py migrate

# Crear migraciones después de cambios en modelos
python manage.py makemigrations

# Shell de Django
python manage.py shell

# Recolectar archivos estáticos
python manage.py collectstatic
```

### Linting y Formateo

**Importante**: Ejecutar en archivos individuales modificados, no en todo el proyecto.

```bash
# Formatear código Python
black path/to/file.py

# Ordenar imports
isort path/to/file.py

# Verificar estilo
flake8 path/to/file.py --max-line-length=100

# Type checking
mypy path/to/file.py

# Formatear templates HTML
djlint --reformat path/to/template.html
```

**Separación de herramientas por lenguaje**:
- **Python**: `black`, `isort`, `flake8`, `mypy`
- **HTML**: `djlint`
- No mezclar herramientas entre lenguajes

### Herramientas Instaladas

- Black 26.1.0 – formateo de código
- isort 8.0.0 – ordenamiento de imports
- flake8 7.3.0 – verificación de estilo
- mypy 1.19.1 – type checking
- djlint – formateo de templates HTML

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
| Constantes | UPPER_SNAKE_CASE | `UNITS`, `PAYMENT_METHODS` |

### Strings

- Usar comillas dobles (`"`) para literales
- Usar f-strings para formateo: `f"Mesa {self.name}"`
- Interfaz en español: `verbose_name="Nombre"`, `messages.success(request, "✅ Pedido creado")`

```python
name = models.CharField(max_length=255, verbose_name="Nombre")
```

### Modelos

```python
class Ingredient(models.Model):
    UNITS = [
        ("oz", "Onzas"),
        ("lb", "Libras"),
    ]

    def add_stock(self, amount):
        self.stock_quantity += Decimal(amount)
        self.save()

    def __str__(self):
        return f"{self.name} ({self.stock_quantity} {self.unit})"
```

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

## Frontend

### Stack

- **AlpineJS**: Interactividad simple (toggles, modales)
- **Bootstrap 5**: Framework CSS principal (CDN)
- **GridJS**: Tablas con búsqueda, ordenamiento, paginación
- **Material Icons**: Iconos (CDN)

### GridJS - Listados y Reportes

Usar GridJS cuando se necesite:
- Búsqueda general de registros
- Filtros por columna
- Ordenamiento
- Paginación
- Exportación a Excel

**CDN necesario:**
```html
<link href="https://cdn.jsdelivr.net/npm/gridjs/dist/theme/mermaid.min.css" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/gridjs/dist/gridjs.production.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/xlsx@0.18.5/dist/xlsx.full.min.js"></script>
```

La implementación completa está en `docs/frontend.md`.

### CSS Personalizado

- Solo cuando Bootstrap no pueda manejar el estilo
- Ubicación: `static/css/`
- Usar clases de Bootstrap primero (utilities, components)

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

Cuando se factura una mesa:
1. Se consolidan todos los items de las órdenes pendientes
2. Se crea una Invoice con los items
3. Se marcan las órdenes como pagadas
4. Se actualiza el arqueo de caja según método de pago

### Arqueo de Caja

- Solo un turno activo a la vez
- Ventas CONTADO suman a `total_contado`
- Ventas CREDITO suman a `total_credito`
- Al cerrar, se calcula diferencia vs efectivo en caja

## URLs del Sistema

### Aliases

Todas las URLs tienen aliases en inglés (`product_list`) y español (`productos/`). Usar los aliases en inglés en el código (`url 'product_list'`).

### Principales

| URL | Alias | Descripción |
|-----|-------|-------------|
| `/pos/` | `table_list` | Lista de mesas |
| `/pos/table/<id>/new/` | `create_order` | Crear orden |
| `/menu/products/` | `product_list` | Productos |
| `/menu/products/<id>/recipes/` | `product_recipes` | Recetas |
| `/inventory/ingredients/` | `ingredient_list` | Ingredientes |
| `/inventory/adjust/` | `inventory_movement` | Ajuste inventario |
| `/inventory/purchase/` | `purchase_ingredients` | Compras |
| `/reports/` | `reports_index` | Panel reportes |
| `/cash/` | `cash_register_list` | Arqueo de caja |
| `/invoices/` | `invoice_list` | Facturas |
| `/dashboard/` | `dashboard` | Dashboard |
| `/empresa/configuracion/` | `company_settings` | Config empresa |

## API Endpoints JSON

| Endpoint | Descripción |
|----------|-------------|
| `/api/ingredients/` | Ingredientes |
| `/api/products/` | Productos |
| `/api/categories/` | Categorías |
| `/api/dispatch-areas/` | Áreas despacho |
| `/api/tables/` | Mesas |
| `/api/orders/` | Órdenes |
| `/api/invoices/` | Facturas |
| `/api/movements/` | Movimientos inventario |
| `/api/inventory/` | Inventario paginado |
| `/api/sales-by-product/` | Ventas por producto |
| `/api/orders-report/` | Reporte de órdenes |
| `/api/sales-today/` | Ventas del día |
| `/api/cash/status/` | Estado de caja |

## Errores Comunes

1. **No usar `transaction.atomic`** en operaciones que modifican múltiples tablas
2. **No validar datos del POST** antes de usarlos
3. **No usar `get_object_or_404`** para obtener objetos por ID
4. **Olvidar `@login_required`** en vistas
5. **Olvidar verificar permisos** con `@user_passes_test`

## Recursos

- [Documentación del Sistema](docs/SYSTEM.md)
- [Guía de Frontend](docs/frontend.md)
- [Django Docs](https://docs.djangoproject.com/en/5.2/)
- [Bootstrap 5](https://getbootstrap.com/docs/5.3/)
- [GridJS](https://gridjs.io/)
- [Material Icons](https://fonts.google.com/icons)

## Resumen para Agentes

1. **NO escribir tests Python** – verificar manualmente en el navegador
2. **Código en inglés**, comentarios/documentación en español
3. **Interfaz en español** (labels, mensajes, verbose_name)
4. **Simplicidad** – evitar soluciones complejas
5. **Seguir patrones existentes** en `orders/views.py` y `orders/models.py`
6. **Ejecutar linting** (`black`, `flake8`, `djlint`) en archivos modificados
7. **Usar GridJS** para tablas con búsqueda/paginación
8. **Activar venv** (`.env/bin/activate`) antes de comandos Python
9. **Credenciales en `.secret`** – no hardcodear
10. **Consultar `docs/SYSTEM.md`** para entender el sistema completo

---

_Last updated: 2026-04-17_
