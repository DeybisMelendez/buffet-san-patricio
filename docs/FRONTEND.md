# Directrices Frontend - Buffet San Patricio

Este documento establece las directrices para el desarrollo frontend del sistema Buffet San Patricio.

---

## Filosofía General

- **Simplicidad**: Priorizar soluciones simples y mantenibles
- **JavaScript Puro**: Sin frameworks ni librerías de interactividad (no AlpineJS, no jQuery)
- **Bootstrap First**: Usar Bootstrap 5 para estilos antes de crear CSS personalizado
- **Responsive**: Usar el sistema de grid de Bootstrap

---

## JavaScript

### Stack de JavaScript

El proyecto usa **JavaScript vanilla** (puro) para toda interactividad:

| Librería | Uso |
|----------|-----|
| `global.js` | Utilidades de la app (470 líneas) |
| `common.js` | Helpers comunes (42 líneas) |
| `grid-utils.js` | Exportar/copiar datos GridJS (150 líneas) |
| `grid.js` | Inicialización de GridJS (209 líneas) |

### ❌ NO Usar

- **AlpineJS**: No está en el proyecto
- **jQuery**: No está en el proyecto
- **Otros frameworks de JavaScript**: No están en el proyecto

### Implementar Interactividad

Usar `addEventListener` para manejar eventos:

```javascript
document.addEventListener('DOMContentLoaded', function() {
    const btn = document.querySelector('#mi-boton');
    if (btn) {
        btn.addEventListener('click', function() {
            // lógica
        });
    }
});
```

### Funciones Globales Disponibles

El proyecto define funciones globales en `global.js`:

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

// GridJS utilities
window.GridUtils.copyToClipboard()
window.GridUtils.exportToExcel(filename)
window.GridUtils.addToolbar(containerId, gridContainerId, filename)

// Impresión
window.printOrder(orderId, iframeId)
window.printInventoryReport(iframeId)
```

### Acceso a Elementos del DOM

```javascript
// Por ID
document.getElementById('element-id')

// Por selector CSS (primer match)
document.querySelector('.class-name')
document.querySelector('#id .child')

// Por selector CSS (todos los matches)
document.querySelectorAll('.class-name')
```

### Manipulación del DOM

```javascript
// Crear elemento
const div = document.createElement('div');
div.className = 'card-body';
div.textContent = 'Texto';

// Agregar al DOM
parentElement.appendChild(div);

// Modificar atributos
element.setAttribute('data-value', '123');
element.getAttribute('data-value');

// Modificar clases
element.classList.add('active');
element.classList.remove('hidden');
element.classList.toggle('visible');

// Modificar estilos inline
element.style.display = 'none';
element.style.color = 'red';
```

### Fetch API

```javascript
// GET request
fetch('/api/endpoint/')
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.error('Error:', error));

// POST request
fetch('/api/endpoint/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
    },
    body: JSON.stringify({ key: 'value' })
})
    .then(response => response.json())
    .then(data => console.log(data));
```

---

## CSS y Estilos

### Bootstrap 5

El proyecto usa **Bootstrap 5** como framework CSS principal. Ver [BOOTSTRAP.md](./BOOTSTRAP.md) para guía completa.

### ❌ NO Usar CSS Personalizado

Evitar crear archivos CSS personalizados. Solo usar cuando Bootstrap no pueda manejar el estilo.

### Casos donde SE Permite CSS Custom

- Variables CSS para colores del tema
- Estilos muy específicos del dominio

### Casos donde NO se Permite

- Margins, paddings (usar `m-*`, `p-*`)
- Colores de texto/fondo (usar `text-*`, `bg-*`)
- Flexbox (usar `d-flex`, `justify-content-*`)
- Borders y rounded (usar `border`, `rounded`)

---

## Estructura de Plantillas

### Herencia de Templates

```html
{% extends 'layout.html' %}
{% load static %}

{% block title %}Título de la Página{% endblock %}

{% block body %}
<div class="container-fluid py-4">
    <!-- Contenido -->
</div>
{% endblock %}

{% block extra_css %}
<!-- CSS adicional solo para esta página -->
{% endblock %}

{% block extra_js %}
<!-- JavaScript adicional solo para esta página -->
{% endblock %}
```

### Bloques Disponibles

| Bloque | Propósito |
|--------|----------|
| `title` | Título de la página (tag `<title>`) |
| `body` | Contenido principal |
| `extra_css` | CSS adicional |
| `extra_js` | JavaScript adicional |

---

## Iconos

### Google Material Icons

El proyecto usa **Google Material Icons** vía CDN.

```html
<link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
```

**Uso:**
```html
<span class="material-icons">icon_name</span>
```

### Iconos Comunes

| Propósito | Icono |
|-----------|-------|
| Editar | `edit` |
| Eliminar | `delete` |
| Agregar | `add` |
| Guardar | `save` |
| Cancelar | `close` |
| Volver | `arrow_back` |
| Buscar | `search` |
| Imprimir | `print` |
| Copiar | `content_copy` |
| Descargar | `download` |

---

## Tablas con GridJS

Para tablas interactivas con búsqueda, ordenamiento y paginación, usar **GridJS**.

Ver [GRIDJS.md](./GRIDJS.md) para guía completa.

### Ejemplo Básico

```javascript
new gridjs.Grid({
    columns: [
        { name: 'Nombre', id: 'name' },
        { name: 'Precio', id: 'price' }
    ],
    server: {
        url: '/api/endpoint/',
        then: data => data.results.map(item => [item.name, item.price]),
        total: data => data.count
    },
    search: true,
    sort: true,
    pagination: { enabled: true, limit: 25 },
    language: 'es-ES'
}).render(document.getElementById('grid-container'));
```

---

## Formularios

### Estructura con Bootstrap

```html
<form method="post">
    {% csrf_token %}
    <div class="mb-3">
        <label class="form-label">Nombre</label>
        <input type="text" name="name" class="form-control" required>
    </div>
    <div class="mb-3">
        <label class="form-label">Categoría</label>
        <select name="category" class="form-select">
            <option value="">Seleccione...</option>
            <option value="1">Opción 1</option>
        </select>
    </div>
    <button type="submit" class="btn btn-primary">Guardar</button>
</form>
```

### CSRF Token

Siempre incluir el token CSRF en formularios POST:

```html
{% csrf_token %}
```

### Validación

La validación se hace en el backend. No confiar en validación solo frontend.

---

## Responsive Design

### Sistema de Grid de Bootstrap

```html
<div class="container">
    <div class="row">
        <div class="col-12 col-md-6 col-lg-4">
            <!-- Contenido responsive -->
        </div>
    </div>
</div>
```

### Breakpoints

| Breakpoint | Prefijo | Ancho mínimo |
|------------|---------|--------------|
| Extra small | (predeterminado) | < 576px |
| Small | `sm-` | ≥ 576px |
| Medium | `md-` | ≥ 768px |
| Large | `lg-` | ≥ 992px |
| Extra large | `xl-` | ≥ 1200px |

---

## Recursos

- [BOOTSTRAP.md](./BOOTSTRAP.md) - Guía de estilos Bootstrap
- [GRIDJS.md](./GRIDJS.md) - Guía de GridJS para tablas
- [SYSTEM.md](./SYSTEM.md) - Documentación técnica completa
- [JavaScript MDN](https://developer.mozilla.org/es/docs/Web/JavaScript)
- [Bootstrap 5](https://getbootstrap.com/docs/5.3/)
- [GridJS](https://gridjs.io/)

---

_Last updated: 2026-04-26_