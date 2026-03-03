# Especificaciones Frontend - Boa POS

Este documento define las convenciones y guías para el desarrollo frontend del proyecto Boa POS.

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

## Migración de BEM a Bootstrap

El proyecto anteriormente usaba metodología BEM. La migración a Bootstrap implica:

1. **Templates nuevos**: Usar clases Bootstrap exclusivamente.
2. **Templates existentes**: Migración gradual según sea necesario.
3. **Custom CSS**: Minimizar; migrar a Bootstrap donde sea posible.
4. **Archivos BEM legacy**: Los archivos en `static/css/` se mantienen temporalmente pero no se deben crear nuevos.

---

_Última actualización: 2026-03-03_
