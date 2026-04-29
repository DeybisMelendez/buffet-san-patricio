# Guía de Bootstrap - Buffet San Patricio

Este documento define las convenciones para el uso de Bootstrap 5 en el proyecto.

---

## Filosofía

- **Bootstrap First**: Usar siempre Bootstrap antes de crear CSS personalizado
- **Clases Utilities**: Preferir clases utilities de Bootstrap sobre CSS custom
- **Sin CSS Custom**: Evitar archivos CSS personalizados a menos que sea absolutamente necesario
- **Responsive**: Usar el sistema de grid de Bootstrap

---

## CDN y Recursos

```html
<!-- Bootstrap 5 CSS -->
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css"
      rel="stylesheet"
      integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH"
      crossorigin="anonymous">

<!-- Bootstrap 5 JS (para modales, dropdowns, etc.) -->
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"
        integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz"
        crossorigin="anonymous"></script>
```

Estos recursos ya están incluidos en `templates/layout.html`.

---

## Sistema de Grid

### Contenedor

```html
<!-- Ancho fijo -->
<div class="container">...</div>

<!-- Ancho completo -->
<div class="container-fluid">...</div>
```

### Filas y Columnas

```html
<div class="container">
    <div class="row">
        <div class="col">1 de 2</div>
        <div class="col">2 de 2</div>
    </div>
    <div class="row">
        <div class="col-8">8 columnas</div>
        <div class="col-4">4 columnas</div>
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

```html
<div class="row">
    <div class="col-12 col-md-6 col-lg-4">Responsive</div>
</div>
```

---

## Clases de Utilidades Más Usadas

### Espaciado

| Propiedad | Direcciones | Tamaños |
|-----------|-------------|---------|
| `m-*` (margin) | t, b, s, e, x, y | 0-5, auto |
| `p-*` (padding) | t, b, s, e, x, y | 0-5, auto |

```html
<!-- Margen -->
<div class="mt-3 mb-2 mx-auto">...</div>

<!-- Padding -->
<div class="p-3 px-4 py-2">...</div>

<!-- Auto -->
<div class="mx-auto">Centrado</div>
```

### Tamaños (width/height)

```html
<div class="w-25">25%</div>
<div class="w-50">50%</div>
<div class="w-75">75%</div>
<div class="w-100">100%</div>

<div class="h-25">25%</div>
<div class="h-50">50%</div>
<div class="h-75">75%</div>
<div class="h-100">100%</div>
```

### Texto

```html
<!-- Alineación -->
<p class="text-start">Izquierda</p>
<p class="text-center">Centro</p>
<p class="text-end">Derecha</p>

<!-- Tamaño -->
<p class="fs-1">Texto grande</p>
<p class="fs-4">Texto normal</p>
<p class="fs-6">Texto pequeño</p>

<!-- Peso -->
<p class="fw-bold">Negrita</p>
<p class="fw-normal">Normal</p>
<p class="fw-light">Ligera</p>

<!-- Color -->
<p class="text-primary">Primary</p>
<p class="text-secondary">Secondary</p>
<p class="text-success">Success</p>
<p class="text-danger">Danger</p>
<p class="text-warning">Warning</p>
<p class="text-info">Info</p>
<p class="text-muted">Muted</p>
```

### Fondo y Bordes

```html
<!-- Fondo -->
<div class="bg-primary">Primary</div>
<div class="bg-light">Light</div>
<div class="bg-dark">Dark</div>
<div class="bg-white">White</div>

<!-- Bordes -->
<div class="border">Borde</div>
<div class="border-top">Borde arriba</div>
<div class="border-end">Borde derecha</div>
<div class="border-bottom">Borde abajo</div>
<div class="border-start">Borde izquierda</div>

<!-- Redondear -->
<div class="rounded">Redondeado</div>
<div class="rounded-pill">Píldora</div>
<div class="rounded-circle">Círculo</div>
```

### Flexbox

```html
<!-- Contenedor flex -->
<div class="d-flex">...</div>
<div class="d-inline-flex">...</div>

<!-- Dirección -->
<div class="flex-row">Fila (default)</div>
<div class="flex-column">Columna</div>
<div class="flex-row-reverse">Fila invertida</div>

<!-- Justificar -->
<div class="justify-content-start">Inicio</div>
<div class="justify-content-center">Centro</div>
<div class="justify-content-end">Fin</div>
<div class="justify-content-between">Entre</div>
<div class="justify-content-around">Alrededor</div>

<!-- Alinear -->
<div class="align-items-start">Arriba</div>
<div class="align-items-center">Centro</div>
<div class="align-items-end">Abajo</div>

<!-- Gap -->
<div class="d-flex gap-2">...</div>
<div class="d-flex gap-3">...</div>

<!-- Wrap -->
<div class="flex-wrap">Wrap</div>
<div class="flex-nowrap">No wrap</div>
```

---

## Componentes

### Cards

```html
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
```

### Botones

```html
<!-- Colores -->
<button class="btn btn-primary">Primary</button>
<button class="btn btn-secondary">Secondary</button>
<button class="btn btn-success">Success</button>
<button class="btn btn-danger">Danger</button>
<button class="btn btn-warning">Warning</button>
<button class="btn btn-info">Info</button>
<button class="btn btn-outline-primary">Outline</button>
<button class="btn btn-link">Link</button>

<!-- Tamaños -->
<button class="btn btn-sm">Small</button>
<button class="btn">Normal</button>
<button class="btn btn-lg">Large</button>

<!-- Estados -->
<button class="btn btn-primary" disabled>Disabled</button>
```

### Formularios

```html
<!-- Input -->
<div class="mb-3">
    <label class="form-label">Nombre</label>
    <input type="text" class="form-control" placeholder="Ingrese nombre">
</div>

<!-- Select -->
<div class="mb-3">
    <label class="form-label">Categoría</label>
    <select class="form-select">
        <option selected> Seleccione...</option>
        <option value="1">Opción 1</option>
        <option value="2">Opción 2</option>
    </select>
</div>

<!-- Textarea -->
<div class="mb-3">
    <label class="form-label">Descripción</label>
    <textarea class="form-control" rows="3"></textarea>
</div>

<!-- Input group -->
<div class="input-group mb-3">
    <span class="input-group-text">@</span>
    <input type="text" class="form-control" placeholder="Username">
</div>
```

### Tablas

```html
<table class="table">
    <thead>
        <tr>
            <th>Columna 1</th>
            <th>Columna 2</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Dato 1</td>
            <td>Dato 2</td>
        </tr>
    </tbody>
</table>

<!-- Con striped y hover -->
<table class="table table-striped table-hover">
    ...
</table>

<!-- Responsive -->
<div class="table-responsive">
    <table class="table">...</table>
</div>
```

### Modals

```html
<!-- Botón que abre el modal -->
<button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#myModal">
    Abrir Modal
</button>

<!-- Estructura del modal -->
<div class="modal fade" id="myModal" tabindex="-1">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title">Título</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body">
                <p>Contenido del modal.</p>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cerrar</button>
                <button type="button" class="btn btn-primary">Guardar</button>
            </div>
        </div>
    </div>
</div>
```

### Alerts

```html
<div class="alert alert-success" role="alert">
    Operación exitosa
</div>

<div class="alert alert-danger" role="alert">
    Error en la operación
</div>

<!-- Con botón de cerrar -->
<div class="alert alert-warning alert-dismissible fade show" role="alert">
    Alerta
    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
</div>
```

### Navbar

```html
<nav class="navbar navbar-expand-lg navbar-light bg-light">
    <div class="container-fluid">
        <a class="navbar-brand" href="#">Brand</a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav">
                <li class="nav-item">
                    <a class="nav-link active" href="#">Inicio</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="#">Enlace</a>
                </li>
            </ul>
        </div>
    </div>
</nav>
```

### Badges

```html
<span class="badge bg-primary">Primary</span>
<span class="badge bg-success">Success</span>
<span class="badge bg-danger">Danger</span>

<!-- Pill -->
<span class="badge rounded-pill bg-warning">Pill</span>
```

### Progress

```html
<div class="progress">
    <div class="progress-bar" role="progressbar" style="width: 25%"></div>
</div>

<div class="progress">
    <div class="progress-bar bg-success" role="progressbar" style="width: 50%"></div>
</div>
```

---

## Iconos

### Google Material Icons

El proyecto usa **Google Material Icons** vía CDN.

```html
<link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
```

**Uso en HTML:**

```html
<span class="material-icons">icon_name</span>
```

**Iconos comunes:**

| Propósito | Icono |
|-----------|-------|
| Editar | `edit` |
| Eliminar | `delete` |
| Agregar | `add` |
| Guardar | `save` |
| Cancelar | `close` |
| Volver | `arrow_back` |
| Buscar | `search` |
| Menú | `menu` |
| Configuración | `settings` |
| Imprimir | `print` |
| Copiar | `content_copy` |
| Descargar | `download` |
| Ver | `visibility` |
| Ocultar | `visibility_off` |
| Advertencia | `warning` |
| Error | `error` |
| Info | `info` |
| Éxito | `check_circle` |

---

## NO Usar

### ❌ AlpineJS

El proyecto **NO usa AlpineJS**. Toda interactividad debe implementarse con JavaScript vanilla.

**Incorrecto:**
```html
<div x-data="{ open: false }">
    <button @click="open = true">Abrir</button>
</div>
```

**Correcto:**
```javascript
document.querySelector('button').addEventListener('click', function() {
    // lógica
});
```

### ❌ jQuery

El proyecto **NO usa jQuery**. Usar JavaScript vanilla para todo.

**Incorrecto:**
```javascript
$('#element').click(function() { ... });
```

**Correcto:**
```javascript
document.querySelector('#element').addEventListener('click', function() { ... });
```

### ❌ CSS Personalizado (除非 sea necesario)

Evitar crear archivos CSS personalizados. Solo usar cuando Bootstrap no pueda manejar el estilo.

**Casos donde SE permite CSS custom:**
- Variables CSS para colores del tema
- Estilos muy específicos del dominio que requieren constantes reutilizables

**Casos donde NO se permite:**
- Margins, paddings (usar `m-*`, `p-*`)
- Colores de texto/fondo (usar `text-*`, `bg-*`)
- Flexbox (usar `d-flex`, `justify-content-*`)
- Borders y rounded (usar `border`, `rounded`)

---

## Ejemplo: Estructura Completa de Página

```html
{% extends 'layout.html' %}
{% load static %}

{% block body %}
<div class="container-fluid py-4">
    <!-- Encabezado -->
    <div class="row mb-4">
        <div class="col">
            <h2 class="mb-0">Título de la Página</h2>
        </div>
        <div class="col-auto">
            <button class="btn btn-primary">
                <span class="material-icons">add</span> Nuevo
            </button>
        </div>
    </div>

    <!-- Card con tabla -->
    <div class="card">
        <div class="card-header">
            <h5 class="card-title mb-0">Listado</h5>
        </div>
        <div class="card-body">
            <div class="table-responsive">
                <table class="table table-striped table-hover">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Nombre</th>
                            <th>Acciones</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>1</td>
                            <td>Item</td>
                            <td>
                                <a href="/edit/1/" class="btn btn-sm btn-outline-primary">
                                    <span class="material-icons">edit</span>
                                </a>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

---

## Recursos

- [Bootstrap 5 Documentation](https://getbootstrap.com/docs/5.3/)
- [Bootstrap Utilities](https://getbootstrap.com/docs/5.3/utilities/)
- [Bootstrap Components](https://getbootstrap.com/docs/5.3/components/)
- [Material Icons](https://fonts.google.com/icons)

---

_Last updated: 2026-04-26_