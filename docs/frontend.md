# Especificaciones Frontend - Buffet San Patricio

Este documento define las convenciones y guías para el desarrollo frontend del sistema Buffet San Patricio.

## Filosofía

- **Simplicidad**: Priorizar soluciones simples y mantenibles.
- **Minimalismo**: Evitar JavaScript innecesario; usar AlpineJS para interactividad básica.
- **Framework**: Usar Bootstrap 5 como framework CSS principal.
- **Custom CSS**: Solo cuando Bootstrap no pueda manejar un estilo específico.
- **Iconos**: Google Material Icons para todos los iconos.

## Interactividad

### AlpineJS

- **Uso principal**: Para interactividad básica (toggles, modales, menús desplegables).
- **Ubicación**: Se incluye vía CDN en `templates/layout.html`.
- **Directivas comunes**: `x-data`, `x-show`, `x-on`, `x-model`.
- **Evitar**: Lógica compleja; si se requiere, mover a archivos JavaScript separados.

### JavaScript Personalizado

- **Solo cuando sea estrictamente necesario**.
- **Ubicación**: `static/js/` (crear si no existe).
- **Convenciones**:
  - Nombres de archivos en `kebab-case` (ej. `form-validation.js`).
  - Usar módulos ES6 si es posible.
  - Documentar funciones y propósito.

## Estilos CSS

### Bootstrap 5

El proyecto usa **Bootstrap 5** como framework CSS principal. Se incluye vía CDN en el layout base.

**Recursos:**
- Documentación: https://getbootstrap.com/docs/5.3/
- CDN: https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css

### Uso de Clases Bootstrap

**Utilidades:**
- Layout: `container`, `container-fluid`, `row`, `col-*`
- Spacing: `m-*`, `p-*`, `mt-*`, `mb-*`, `ms-*`, `me-*`
- Typography: `text-start`, `text-center`, `text-end`, `fw-bold`, `fs-*`
- Colors: `text-primary`, `text-secondary`, `bg-primary`, `bg-light`, etc.
- Flexbox: `d-flex`, `justify-content-*`, `align-items-*`, `flex-wrap`
- Borders: `border`, `border-*`, `rounded`, `rounded-*`

**Componentes:**
- Cards: `card`, `card-header`, `card-body`, `card-footer`
- Buttons: `btn`, `btn-primary`, `btn-secondary`, `btn-sm`, `btn-lg`
- Forms: `form-control`, `form-label`, `form-select`, `input-group`
- Tables: `table`, `table-striped`, `table-hover`, `table-responsive`
- Modals: `modal`, `modal-dialog`, `modal-content`, `modal-header`, `modal-body`
- Navbar: `navbar`, `navbar-expand-*`, `navbar-light`, `navbar-dark`
- Alerts: `alert`, `alert-primary`, `alert-success`, `alert-warning`, `alert-danger`

### Custom CSS

Solo crear CSS personalizado cuando Bootstrap no pueda manejar el estilo necesario.

**Directorios:**
- `static/css/` – archivos CSS personalizados

**Casos válidos para custom CSS:**
- Estilos específicos del proyecto que requieren variables CSS reutilizables
- Estilos para componentes muy específicos del dominio
- Animaciones o transiciones complejas

**Casos NO válidos (usar Bootstrap):**
- Margins, paddings, sizes (`mt-1`, `p-2`, etc.)
- Colores de texto o fondo (`text-primary`, `bg-success`, etc.)
- Flexbox (`d-flex`, `justify-content-between`, etc.)
- Borders y rounded (`border`, `rounded`, etc.)

### Ejemplo: Estructura con Bootstrap

```html
<div class="container my-4">
  <div class="row">
    <div class="col-md-6 mb-3">
      <div class="card">
        <div class="card-header">
          <h5 class="card-title mb-0">Título</h5>
        </div>
        <div class="card-body">
          <p class="card-text">Contenido de la tarjeta.</p>
        </div>
        <div class="card-footer">
          <button class="btn btn-primary btn-sm">Acción</button>
        </div>
      </div>
    </div>
  </div>
</div>
```

## Iconos

### Google Material Icons

El proyecto usa **Google Material Icons** vía CDN.

**Include en el layout:**
```html
<link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
```

**Uso en HTML:**
```html
<span class="material-icons">icon_name</span>
```

**Iconos comunes:**
- Editar: `edit`
- Eliminar: `delete`
- Agregar: `add`
- Guardar: `save`
- Cancelar: `close`
- Volver: `arrow_back`
- Buscar: `search`
- Menú: `menu`
- Configuración: `settings`

## Temas Claro y Oscuro

Bootstrap 5 soporta temas claro y oscuro de forma nativa.

### Enfoque

- Usar clases de Bootstrap para ambos temas.
- Para tema oscuro, usar la clase `dark` en el elemento `html` o usar variables CSS de Bootstrap.
- Personalizar con CSS variables cuando sea necesario.

### Custom CSS para Temas

```css
:root {
  --mi-color-primary: #0d6efd;
}

[data-bs-theme="dark"] {
  --mi-color-primary: #6ea8fe;
}
```

## Estructura de Carpetas

```
static/
├── css/
│   └── (archivos CSS personalizados, mínimo)
├── js/
│   └── (scripts personalizados si son necesarios)
└── (otros assets: imágenes, fuentes, etc.)
```

## Integración con Django Templates

### Carga de Estilos

El layout base (`layout.html`) carga Bootstrap 5 y Google Material Icons vía CDN.

**En el layout base:**
```html
<head>
  <!-- Bootstrap CSS -->
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
  <!-- Google Material Icons -->
  <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
  <!-- Custom CSS -->
  <link rel="stylesheet" href="{% static 'css/styles.css' %}">
  {% block extra_css %}{% endblock %}
</head>
```

### Bloques Extra para Templates

Cada template puede agregar CSS y JavaScript adicional mediante los bloques `extra_css` y `extra_js`:

**En un template específico:**

```html
{% extends 'layout.html' %}
{% load static %}

{% block extra_css %}
<style>
  /* Custom styles only when Bootstrap can't handle it */
</style>
{% endblock %}

{% block extra_js %}
<script src="{% static 'js/mi-script.js' %}"></script>
{% endblock %}

{% block body %}
<!-- Content using Bootstrap classes -->
{% endblock %}
```

## Directrices para Nuevo Desarrollo

1. **Usar Bootstrap primero**: Antes de crear custom CSS, verificar si Bootstrap tiene clases útiles.
2. **Iconos**: Siempre usar Google Material Icons.
3. **AlpineJS**: Para interactividad básica, preferir AlpineJS sobre JavaScript personalizado.
4. **Mantenibilidad**: Si se crea custom CSS, documentar su propósito.
5. **Responsive**: Usar clases de Bootstrap para responsive design (`col-`, `col-sm-`, `col-md-`, etc.).

## GridJS - Tablas y Listados

### Cuándo usar GridJS

Utilizar **GridJS** para generar listados, tablas o reportes cuando se requiera:
- Búsqueda general de registros
- Filtros por columna
- Ordenamiento por columnas
- Paginación con selección de cantidad de items por página
- Carga dinámica de datos desde API

**CDN GridJS:**
```html
<!-- GridJS CSS -->
<link href="https://cdn.jsdelivr.net/npm/gridjs/dist/theme/mermaid.min.css" rel="stylesheet">
<!-- GridJS JS -->
<script src="https://cdn.jsdelivr.net/npm/gridjs/dist/gridjs.production.min.js"></script>
<!-- SheetJS para exportar a Excel -->
<script src="https://cdn.jsdelivr.net/npm/xlsx@0.18.5/dist/xlsx.full.min.js"></script>
```

### Implementación en Templates

#### 1. Estructura básica del template

```html
{% extends 'layout.html' %}
{% load static %}

{% block extra_css %}
<link href="https://cdn.jsdelivr.net/npm/gridjs/dist/theme/mermaid.min.css" rel="stylesheet">
<style>
  /* Custom styles for GridJS */
  .gridjs-wrapper {
    box-shadow: none;
  }
  .gridjs-table {
    width: 100%;
  }
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
<script src="https://cdn.jsdelivr.net/npm/gridjs/dist/gridjs.production.min.js"></script>
<script>
  document.addEventListener('DOMContentLoaded', function() {
    const grid = new gridjs.Grid({
      columns: [
        { name: 'Columna 1', id: 'campo1' },
        { name: 'Columna 2', id: 'campo2' },
        { name: 'Acciones', id: 'acciones', sort: false, plugin: gridjs.plugins.selection }
      ],
      server: {
        url: '/api/endpoint/',
        then: data => data.results.map(item => [
          item.campo1,
          item.campo2,
          // Acciones
        ]),
        total: data => data.count
      },
      search: {
        enabled: true,
        placeholder: 'Buscar...'
      },
      sort: {
        enabled: true
      },
      pagination: {
        enabled: true,
        limit: 10,
        summary: true,
        labels: {
          first: '«',
          last: '»',
          prev: '‹',
          next: '›'
        }
      },
      language: 'es-ES'
    });
    grid.render(document.getElementById('grid-container'));
  });
</script>
{% endblock %}
```

#### Botones Copiar y Exportar a Excel

Para agregar botones de copiar y exportar a Excel en los listados GridJS:

```html
{% block extra_js %}
<script src="https://cdn.jsdelivr.net/npm/gridjs/dist/gridjs.production.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/xlsx@0.18.5/dist/xlsx.full.min.js"></script>
<script>
  document.addEventListener('DOMContentLoaded', function() {
    // Función para obtener datos actuales del Grid
    function getGridData(grid) {
      const rows = [];
      const table = document.querySelector('.gridjs-table');
      if (!table) return [];
      
      // Obtener encabezados
      const headers = Array.from(table.querySelectorAll('thead th')).map(th => th.textContent.trim());
      rows.push(headers);
      
      // Obtener filas de datos
      table.querySelectorAll('tbody tr').forEach(tr => {
        const row = Array.from(tr.querySelectorAll('td')).map(td => td.textContent.trim());
        rows.push(row);
      });
      
      return rows;
    }

    // Función para copiar al portapapeles
    function copyToClipboard() {
      const table = document.querySelector('.gridjs-table');
      if (!table) return;
      
      let text = '';
      table.querySelectorAll('tr').forEach(tr => {
        const row = Array.from(tr.querySelectorAll('th, td'))
          .map(td => td.textContent.trim())
          .join('\t');
        text += row + '\n';
      });
      
      navigator.clipboard.writeText(text).then(() => {
        alert('Datos copiados al portapapeles');
      }).catch(err => {
        console.error('Error al copiar:', err);
      });
    }

    // Función para exportar a Excel
    function exportToExcel() {
      const table = document.querySelector('.gridjs-table');
      if (!table) return;
      
      const wb = XLSX.utils.table_to_book(table, { sheet: 'Listado' });
      const ws = wb.Sheets[wb.SheetNames[0]];
      
      // Ajustar ancho de columnas
      const colWidths = [];
      const headers = table.querySelectorAll('thead th');
      headers.forEach((th, i) => {
        const maxWidth = Math.max(
          th.textContent.trim().length,
          ...Array.from(table.querySelectorAll(`tbody td:nth-child(${i + 1})`))
            .map(td => td.textContent.trim().length)
        );
        colWidths.push({ wch: maxWidth + 2 });
      });
      ws['!cols'] = colWidths;
      
      XLSX.writeFile(wb, 'listado.xlsx');
    }

    // Crear el Grid
    const grid = new gridjs.Grid({
      columns: [
        { name: 'Columna 1', id: 'campo1' },
        { name: 'Columna 2', id: 'campo2' }
      ],
      // ... resto de configuración
    });
    grid.render(document.getElementById('grid-container'));

    // Agregar botones después de renderizar el Grid
    grid.on('ready', () => {
      const container = document.getElementById('grid-container');
      const wrapper = container.closest('.card-body');
      
      // Crear toolbar de botones
      const toolbar = document.createElement('div');
      toolbar.className = 'd-flex gap-2 mb-3';
      toolbar.innerHTML = `
        <button type="button" class="btn btn-outline-secondary btn-sm" onclick="window.copyGridData()">
          <span class="material-icons" style="font-size: 1rem;">content_copy</span> Copiar
        </button>
        <button type="button" class="btn btn-outline-success btn-sm" onclick="window.exportGridData()">
          <span class="material-icons" style="font-size: 1rem;">download</span> Excel
        </button>
      `;
      
      // Insertar toolbar antes del grid
      container.parentNode.insertBefore(toolbar, container);

      // Exponer funciones globalmente
      window.copyGridData = copyToClipboard;
      window.exportGridData = exportToExcel;
    });
  });
</script>
{% endblock %}
```

**Nota**: Las funciones `copyToClipboard` y `exportToExcel` utilizan la tabla renderizada actualmente en el DOM. Esto significa que copiarán solo los datos visibles en la página actual (respecto a la paginación) y respetarán cualquier ordenamiento aplicado.

#### 2. API del Backend

La API debe retornar paginación del lado del servidor con el siguiente formato:

```json
{
  "count": 150,
  "next": "http://localhost:8000/api/endpoint/?page=2&limit=10",
  "previous": null,
  "results": [
    { "id": 1, "campo1": "valor1", "campo2": "valor2" },
    { "id": 2, "campo1": "valor3", "campo2": "valor4" }
  ]
}
```

**Parámetros que GridJS envía por query string:**
- `page`: número de página (empezando desde 1)
- `limit`: cantidad de registros por página
- `search`: término de búsqueda general
- `sort`: campo y dirección de ordenamiento (formato: `campo,direccion`)

#### 3. Vista Django para la API

```python
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

@method_decorator(login_required, name="dispatch")
class MiListadoAPI(View):
    def get(self, request):
        from .models import MiModelo

        queryset = MiModelo.objects.all()

        # Búsqueda general
        search = request.GET.get("search", "").strip()
        if search:
            queryset = queryset.filter(
                Q(campo1__icontains=search) |
                Q(campo2__icontains=search)
            )

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
            limit = int(request.GET.get("limit", 10))
        except ValueError:
            page = 1
            limit = 10

        if limit == 0:
            # Mostrar todos los registros
            items = list(queryset.values())
            return JsonResponse({
                "count": len(items),
                "results": items
            })

        start = (page - 1) * limit
        end = start + limit
        items = list(queryset.values())[start:end]

        return JsonResponse({
            "count": queryset.count(),
            "results": items
        })
```

#### 4. Paginación con "Mostrar Todo"

Para implementar la opción de mostrar todos los registros:

```javascript
// Agregar selector de cantidad por página
pagination: {
  enabled: true,
  limit: 10,
  limits: [5, 10, 25, 50, 100],
  summary: true
}
```

Para mostrar todo, enviar `limit=0` desde el frontend (configurar en el evento de cambio del selector).

#### 5. Filtros por Columna

Para agregar campos de búsqueda en cada columna, usar el plugin de búsqueda de GridJS o implementar manualmente:

```javascript
search: {
  enabled: true,
  placeholder: 'Buscar en todas las columnas...'
}

// Para búsqueda por columna específica, usar formato:
search: {
  selector: (col) => col.id === 'campo1' ? document.createElement('input') : null
}
```

Opcionalmente, crear filtros HTML separados y pasar los valores a la API:

```html
<div class="row mb-3">
  <div class="col-md-3">
    <input type="text" id="filter-campo1" class="form-control form-control-sm" placeholder="Filtrar campo1">
  </div>
  <div class="col-md-3">
    <select id="filter-campo2" class="form-select form-select-sm">
      <option value="">Todos</option>
      <option value="valor1">Valor 1</option>
    </select>
  </div>
</div>
```

```javascript
const grid = new gridjs.Grid({
  server: {
    url: (params) => {
      const url = new URL('/api/endpoint/', window.location.origin);
      if (params.search) url.searchParams.append('search', params.search);
      if (params.page) url.searchParams.append('page', params.page + 1);
      if (params.limit) url.searchParams.append('limit', params.limit);
      if (params.sort) url.searchParams.append('sort', `${params.sort.field},${params.sort.direction}`);
      
      // Agregar filtros de columnas
      const filtro1 = document.getElementById('filter-campo1').value;
      if (filtro1) url.searchParams.append('campo1', filtro1);
      
      return url.toString();
    },
    // ...resto de configuración
  }
});
```

### Estilos Personalizados para GridJS

Agregar en el block `extra_css` del template:

```css
/* Personalizar GridJS */
.gridjs-container {
  font-size: 0.875rem;
}

.gridjs-th {
  font-weight: 600;
}

.gridjs-td {
  padding: 0.75rem;
}

/* Estilo para columna de acciones */
.gridjs-td.acciones {
  text-align: center;
}

.gridjs-td .btn {
  padding: 0.25rem 0.5rem;
  font-size: 0.75rem;
}
```

---

## Migración de BEM a Bootstrap

El proyecto anteriormente usaba metodología BEM. La migración a Bootstrap implica:

1. **Templates nuevos**: Usar clases Bootstrap exclusivamente.
2. **Templates existentes**: Migración gradual según sea necesario.
3. **Custom CSS**: Minimizar; migrar a Bootstrap donde sea posible.
4. **Archivos BEM legacy**: Los archivos en `static/css/` se mantienen temporalmente pero no se deben crear nuevos.

---

_Última actualización: 2026-03-03_
