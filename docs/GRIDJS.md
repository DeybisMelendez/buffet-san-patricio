# Guía de GridJS - Buffet San Patricio

Sistema de tablas interactivas para listados, reportes y datos paginados.

---

## Introducción

El proyecto usa **GridJS** para generar tablas interactivas con:
- Búsqueda general de registros
- Ordenamiento por columnas
- Paginación con selección de cantidad de items
- Carga dinámica desde API (server-side)
- Exportación a Excel

---

## CDN y Recursos

```html
<!-- GridJS CSS -->
<link href="https://cdn.jsdelivr.net/npm/gridjs/dist/theme/mermaid.min.css" rel="stylesheet">

<!-- GridJS JS (UMD) -->
<script src="https://unpkg.com/gridjs/dist/gridjs.umd.js"></script>

<!-- SheetJS para exportar a Excel -->
<script src="https://cdn.jsdelivr.net/npm/xlsx@0.18.5/dist/xlsx.full.min.js"></script>
```

Estos recursos ya están incluidos en `templates/layout.html`.

---

## Utilidades Disponibles

El proyecto proporciona utilidades en `static/js/`:

### GridUtils (`grid-utils.js`)

| Función | Descripción |
|---------|-------------|
| `GridUtils.showLoading(containerId)` | Muestra spinner de carga |
| `GridUtils.showError(containerId, message)` | Muestra mensaje de error |
| `GridUtils.getTableData()` | Obtiene datos de la tabla renderizada |
| `GridUtils.copyToClipboard()` | Copia datos al portapapeles |
| `GridUtils.exportToExcel(filename)` | Exporta a archivo Excel |
| `GridUtils.addToolbar(containerId, gridContainerId, filename)` | Agrega botones Copiar/Excel |
| `GridUtils.handleServerError(res)` | Manejo de errores en requests |

### GridJS (`grid.js`)

| Función | Descripción |
|---------|-------------|
| `GridJS.init(tableId, apiUrl, columns, options)` | Inicializa tabla con datos remotos |
| `GridJS.initLocal(tableId, data, columns, options)` | Inicializa tabla con datos locales |
| `GridJS.createColumns(fields)` | Crea definición de columnas |
| `GridJS.addColumnFilters(tableId, placeholder)` | Agrega filtros por columna |

---

## Estructura Básica

### Template HTML

```html
{% extends 'layout.html' %}
{% load static %}

{% block extra_css %}
<link href="https://cdn.jsdelivr.net/npm/gridjs/dist/theme/mermaid.min.css" rel="stylesheet">
<style>
    .gridjs-wrapper { box-shadow: none; }
    .gridjs-table { width: 100%; }
</style>
{% endblock %}

{% block body %}
<div class="container-fluid">
    <div class="row mb-3">
        <div class="col">
            <h4 class="mb-0">Título del Listado</h4>
        </div>
    </div>
    <div class="card">
        <div class="card-body">
            <div id="grid-container"></div>
        </div>
    </div>
</div>
{% endblock %}

{% block extra_js %}
<script src="https://unpkg.com/gridjs/dist/gridjs.umd.js"></script>
<script>
document.addEventListener('DOMContentLoaded', function() {
    // Configuración del Grid
});
</script>
{% endblock %}
```

---

## Ejemplos por Módulo

### Ingredientes (`/inventory/ingredients/`)

```javascript
const grid = new gridjs.Grid({
    columns: [
        { name: 'ID', id: 'id', width: '60px' },
        { name: 'Nombre', id: 'name' },
        { name: 'Stock', id: 'stock_quantity' },
        { name: 'Unidad', id: 'unit' },
        { name: 'Bodega', id: 'warehouse_name' },
    ],
    server: {
        url: '/api/ingredients/',
        then: data => data.results.map(item => [
            item.id,
            item.name,
            item.stock_quantity,
            item.unit,
            item.warehouse_name || '-',
        ]),
        total: data => data.count
    },
    search: { enabled: true, placeholder: 'Buscar ingrediente...' },
    sort: { enabled: true },
    pagination: { enabled: true, limit: 25, summary: true },
    language: 'es-ES'
});
grid.render(document.getElementById('grid-container'));
```

### Productos (`/menu/products/`)

```javascript
const columns = [
    { name: 'Nombre', id: 'name' },
    { name: 'Categoría', id: 'category_name' },
    { name: 'Área', id: 'dispatch_area_name' },
    { name: 'Precio', id: 'price', formatter: cell => cell ? `C$ ${parseFloat(cell).toFixed(2)}` : '-' },
    { name: 'Acciones', id: 'actions', sort: false }
];

const grid = new gridjs.Grid({
    columns,
    server: {
        url: '/api/products/',
        then: data => data.results.map(item => [
            item.name,
            item.category_name || '-',
            item.dispatch_area_name || '-',
            item.price,
            gridjs.html(`<a href="/menu/products/${item.id}/edit/" class="btn btn-sm btn-outline-primary">Editar</a>`)
        ]),
        total: data => data.count
    },
    search: { enabled: true },
    sort: { enabled: true },
    pagination: { enabled: true, limit: 25, summary: true },
    language: 'es-ES'
});
grid.render(document.getElementById('grid-container'));
```

### Órdenes (`/api/orders/`)

```javascript
const columns = [
    { name: 'ID', id: 'id', width: '60px' },
    { name: 'Mesa', id: 'table_name' },
    { name: 'Usuario', id: 'user_username' },
    { name: 'Fecha', id: 'created_at', formatter: cell => new Date(cell).toLocaleString('es-NI') },
    { name: 'Total', id: 'total', formatter: cell => `C$ ${parseFloat(cell || 0).toFixed(2)}` },
    { name: 'Estado', id: 'is_paid', formatter: cell => cell ? 'Pagada' : 'Pendiente' }
];

new gridjs.Grid({
    columns,
    server: {
        url: '/api/orders/',
        then: data => data.results.map(item => [
            item.id,
            item.table_name || 'Sin mesa',
            item.user_username || '-',
            item.created_at,
            item.total,
            item.is_paid
        ]),
        total: data => data.count
    },
    search: { enabled: true },
    sort: { enabled: true },
    pagination: { enabled: true, limit: 25 },
    language: 'es-ES'
}).render(document.getElementById('grid-container'));
```

### Facturas (`/invoices/`)

```javascript
new gridjs.Grid({
    columns: [
        { name: 'Número', id: 'invoice_number', width: '80px' },
        { name: 'Fecha', id: 'created_at' },
        { name: 'Mesa', id: 'table_name' },
        { name: 'Total', id: 'total' },
        { name: 'Método', id: 'payment_type_display' },
        { name: 'Cajero', id: 'cashier_username' }
    ],
    server: {
        url: '/api/invoices/',
        then: data => data.results.map(item => [
            `#${item.invoice_number}`,
            new Date(item.created_at).toLocaleDateString('es-NI'),
            item.table_name || '-',
            `C$ ${parseFloat(item.total).toFixed(2)}`,
            item.payment_type_display,
            item.cashier_username || '-'
        ]),
        total: data => data.count
    },
    search: { enabled: true },
    sort: { enabled: true },
    pagination: { enabled: true, limit: 25 },
    language: 'es-ES'
}).render(document.getElementById('grid-container'));
```

### Movimientos de Inventario (`/reports/movements/`)

```javascript
new gridjs.Grid({
    columns: [
        { name: 'Fecha', id: 'created_at' },
        { name: 'Ingrediente', id: 'ingredient_name' },
        { name: 'Cantidad', id: 'quantity', formatter: cell => {
            const val = parseFloat(cell);
            return val >= 0 ? `+${val.toFixed(2)}` : val.toFixed(2);
        }},
        { name: 'Razón', id: 'reason' },
        { name: 'Usuario', id: 'user_username' }
    ],
    server: {
        url: '/api/movements/',
        then: data => data.results.map(item => [
            new Date(item.created_at).toLocaleString('es-NI'),
            item.ingredient_name,
            item.quantity,
            item.reason || '-',
            item.user_username || '-'
        ]),
        total: data => data.count
    },
    search: { enabled: true },
    sort: { enabled: true },
    pagination: { enabled: true, limit: 50 },
    language: 'es-ES'
}).render(document.getElementById('grid-container'));
```

---

## Configuración de Columnas

### Nombres y IDs

```javascript
columns: [
    { name: 'Nombre Visible', id: 'campo_db' }
]
```

### Formateadores

```javascript
// Formato de moneda
formatter: cell => `C$ ${parseFloat(cell).toFixed(2)}`

// Formato de fecha
formatter: cell => new Date(cell).toLocaleDateString('es-NI')

// HTML en celdas
formatter: cell => gridjs.html('<a href="/url/">Ver</a>')

// Condicional
formatter: cell => cell ? 'Sí' : 'No'
```

### Ancho y Ocultar

```javascript
columns: [
    { name: 'ID', id: 'id', width: '50px', hidden: false },
    { name: 'Nombre', id: 'name', width: '200px' }
]
```

### Deshabilitar Ordenamiento

```javascript
columns: [
    { name: 'Acciones', id: 'actions', sort: false }
]
```

---

## Paginación

### Configuración Básica

```javascript
pagination: {
    enabled: true,
    limit: 25,
    summary: true
}
```

### Opciones de Límite

```javascript
pagination: {
    enabled: true,
    limit: 10,
    limits: [5, 10, 25, 50, 100],
    summary: true
}
```

### Mostrar Todos los Registros

Enviar `limit=0` en la URL (configurar en el evento de cambio del selector).

---

## Búsqueda y Ordenamiento

### Search

```javascript
search: {
    enabled: true,
    placeholder: 'Buscar en todas las columnas...'
}
```

### Sort

```javascript
sort: {
    enabled: true,
    multiColumn: true
}
```

---

## Exportación a Excel

### Usando Utilidades del Proyecto

```javascript
// Después de crear el grid, agregar toolbar:
GridUtils.addToolbar('toolbar-container', 'grid-container', 'reporte');

// Funciones disponibles:
GridUtils.copyToClipboard();      // Copiar datos
GridUtils.exportToExcel('archivo'); // Exportar a Excel
```

### Implementación Manual

```javascript
function exportToExcel() {
    const table = document.querySelector('.gridjs-table');
    if (!table) return;

    const wb = XLSX.utils.table_to_book(table, { sheet: 'Datos' });
    const ws = wb.Sheets[wb.Sheets[0]];

    // Ajustar ancho de columnas
    const colWidths = [];
    table.querySelectorAll('thead th').forEach((th, i) => {
        const maxWidth = Math.max(
            th.textContent.trim().length,
            ...Array.from(table.querySelectorAll(`tbody td:nth-child(${i + 1})`))
                .map(td => td.textContent.trim().length)
        );
        colWidths.push({ wch: maxWidth + 2 });
    });
    ws['!cols'] = colWidths;

    XLSX.writeFile(wb, 'reporte.xlsx');
}
```

---

## API del Backend

### Formato de Respuesta

```json
{
  "count": 150,
  "next": "http://localhost:8000/api/endpoint/?page=2&limit=10",
  "previous": null,
  "results": [
    { "id": 1, "name": "valor1", "price": 10.00 }
  ]
}
```

### Parámetros de Query

| Parámetro | Descripción | Ejemplo |
|-----------|-------------|---------|
| `page` | Número de página | `?page=2` |
| `limit` | Registros por página | `?limit=25` |
| `search` | Término de búsqueda | `?search=arroz` |
| `sort` | Campo y dirección | `?sort=name,asc` o `?sort=price,desc` |

---

## Vista Django para API

```python
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

@method_decorator(login_required, name="dispatch")
class ApiIngredients(View):
    def get(self, request):
        from .models import Ingredient

        queryset = Ingredient.objects.all()

        # Búsqueda
        search = request.GET.get("search", "").strip()
        if search:
            queryset = queryset.filter(name__icontains=search)

        # Ordenamiento
        sort = request.GET.get("sort", "")
        if sort:
            field, direction = sort.split(",")
            if direction == "desc":
                field = f"-{field}"
            queryset = queryset.order_by(field)

        # Paginación
        try:
            page = int(request.GET.get("page", 1))
            limit = int(request.GET.get("limit", 25))
        except ValueError:
            page = 1
            limit = 25

        if limit == 0:
            items = list(queryset.values())
            return JsonResponse({"count": len(items), "results": items})

        start = (page - 1) * limit
        end = start + limit
        items = list(queryset.values())[start:end]

        return JsonResponse({
            "count": queryset.count(),
            "results": items
        })
```

---

## Filtros por Columna

### Filtros HTML Separados

```html
<div class="row mb-3">
    <div class="col-md-3">
        <select id="filter-category" class="form-select form-select-sm">
            <option value="">Todas las categorías</option>
            <option value="1">Entradas</option>
            <option value="2">Principales</option>
        </select>
    </div>
    <div class="col-md-3">
        <input type="text" id="filter-name" class="form-control form-control-sm"
               placeholder="Filtrar por nombre">
    </div>
</div>
<div id="grid-container"></div>
```

```javascript
const grid = new gridjs.Grid({
    server: {
        url: (params) => {
            const url = new URL('/api/products/', window.location.origin);

            if (params.search) url.searchParams.append('search', params.search);
            if (params.page) url.searchParams.append('page', params.page + 1);
            if (params.limit) url.searchParams.append('limit', params.limit);
            if (params.sort) url.searchParams.append('sort', `${params.sort.field},${params.sort.direction}`);

            // Agregar filtros
            const category = document.getElementById('filter-category').value;
            if (category) url.searchParams.append('category', category);

            const name = document.getElementById('filter-name').value;
            if (name) url.searchParams.append('name', name);

            return url.toString();
        },
        then: data => data.results.map(item => [item.name, item.category_name, item.price]),
        total: data => data.count
    },
    // ... resto de configuración
});

// Recargar al cambiar filtros
document.getElementById('filter-category').addEventListener('change', () => grid.refresh());
document.getElementById('filter-name').addEventListener('input', () => grid.refresh());
```

---

## Estilos Personalizados

Agregar en el block `extra_css` del template:

```css
.gridjs-container {
    font-size: 0.875rem;
}

.gridjs-th {
    font-weight: 600;
    background-color: var(--bs-light);
}

.gridjs-td {
    padding: 0.75rem;
}

.gridjs-td.acciones {
    text-align: center;
}

.gridjs-td .btn {
    padding: 0.25rem 0.5rem;
    font-size: 0.75rem;
}
```

---

## Demo

Ver `/demo/gridjs/` para ejemplos funcionales de GridJS.

---

## Recursos

- [GridJS Documentation](https://gridjs.io/docs/)
- [GridJS GitHub](https://github.com/gridjs/gridjs)
- [SheetJS Documentation](https://sheetjs.com/)

---

_Last updated: 2026-04-26_