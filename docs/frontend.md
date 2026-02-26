# Especificaciones Frontend - Boa POS

Este documento define las convenciones y guías para el desarrollo frontend del proyecto Boa POS.

## Filosofía

- **Simplicidad**: Priorizar soluciones simples y mantenibles.
- **Minimalismo**: Evitar JavaScript innecesario; usar AlpineJS para interactividad básica.
- **Reutilización**: Crear componentes CSS reutilizables usando la metodología BEM.
- **Compatibilidad**: Diseñar pensando en temas claro y oscuro.

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

### Metodología BEM (Bloque, Elemento, Modificador)

- **Bloque**: Componente independiente y reutilizable (ej. `.card`, `.nav`).
- **Elemento**: Parte de un bloque (ej. `.card__title`, `.card__body`).
- **Modificador**: Variante de un bloque o elemento (ej. `.card--featured`, `.nav__item--active`).

### Estructura de Archivos

- **Directorio**: `static/css/`
- **Organización**: Un archivo por bloque principal.
- **Nombres**: En `kebab-case` (ej. `nav.css`, `card.css`, `modal.css`).
- **Importación selectiva**: No hay un archivo principal único; cada template importa los bloques que necesita. El layout base incluye bloques esenciales (base, navegación, mensajes, botones, contenido principal, pie de página).

### Contenido de Archivos CSS

Cada archivo debe incluir:

1. **Comentario de cabecera**: Descripción del bloque y su propósito.
2. **Variables CSS**: Definir colores, espaciados, etc. para temas.
3. **Bloque**: Estilos base.
4. **Elementos**: Estilos de elementos dentro del bloque.
5. **Modificadores**: Variantes.
6. **Media queries**: Responsividad si es necesario.

### Ejemplo: `static/css/card.css`

```css
/* ============================================
   CARD
   Componente para mostrar contenido en cajas
   ============================================ */

:root {
  --card-bg-light: #ffffff;
  --card-bg-dark: #1e1e1e;
  --card-border-light: #e0e0e0;
  --card-border-dark: #333333;
  --card-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.card {
  background-color: var(--card-bg-light);
  border: 1px solid var(--card-border-light);
  border-radius: 8px;
  box-shadow: var(--card-shadow);
  padding: 1.5rem;
  transition: all 0.3s ease;
}

@media (prefers-color-scheme: dark) {
  .card {
    background-color: var(--card-bg-dark);
    border-color: var(--card-border-dark);
  }
}

.card__header {
  margin-bottom: 1rem;
  padding-bottom: 0.75rem;
  border-bottom: 1px solid var(--card-border-light);
}

.card__title {
  font-size: 1.25rem;
  font-weight: 600;
  margin: 0;
}

.card__body {
  line-height: 1.6;
}

.card__footer {
  margin-top: 1rem;
  padding-top: 0.75rem;
  border-top: 1px solid var(--card-border-light);
  text-align: right;
}

/* Modificadores */
.card--featured {
  border-color: #007bff;
  box-shadow: 0 4px 12px rgba(0, 123, 255, 0.2);
}

.card--compact {
  padding: 1rem;
}

.card--borderless {
  border: none;
  box-shadow: none;
}
```

## Temas Claro y Oscuro

### Enfoque

- Usar `prefers-color-scheme` para detección automática.
- Definir variables CSS en `:root` para ambos temas.
- Proporcionar alternativas de color en media queries.

### Variables Recomendadas

```css
:root {
  /* Colores base - tema claro */
  --color-bg-light: #ffffff;
  --color-text-light: #333333;
  --color-border-light: #e0e0e0;
  --color-primary-light: #007bff;
  --color-secondary-light: #6c757d;

  /* Colores base - tema oscuro */
  --color-bg-dark: #1e1e1e;
  --color-text-dark: #f0f0f0;
  --color-border-dark: #444444;
  --color-primary-dark: #3399ff;
  --color-secondary-dark: #8a93a2;
}

@media (prefers-color-scheme: dark) {
  :root {
    --color-bg: var(--color-bg-dark);
    --color-text: var(--color-text-dark);
    --color-border: var(--color-border-dark);
    --color-primary: var(--color-primary-dark);
    --color-secondary: var(--color-secondary-dark);
  }
}

@media (prefers-color-scheme: light) {
  :root {
    --color-bg: var(--color-bg-light);
    --color-text: var(--color-text-light);
    --color-border: var(--color-border-light);
    --color-primary: var(--color-primary-light);
    --color-secondary: var(--color-secondary-light);
  }
}
```

## Estructura de Carpetas Recomendada

```
static/
├── css/
│   ├── base.css            # Estilos base (reset, tipografía)
│   ├── card.css            # Bloque de tarjetas
│   ├── footer.css          # Pie de página
│   ├── form.css            # Bloque de formularios
│   ├── main.css            # Contenido principal
│   ├── messages.css        # Mensajes y alertas
│   ├── modal.css           # Bloque de modales
│   ├── nav.css             # Bloque de navegación
│   └── table.css           # Bloque de tablas
├── js/
│   └── (scripts personalizados si son necesarios)
└── (otros assets: imágenes, fuentes, etc.)
```

## Directrices para Crear Nuevos Bloques

1. **Evaluar necesidad**: ¿Existe ya un bloque que pueda adaptarse?
2. **Nombre semantico**: Usar nombres que describan el propósito del componente, no su apariencia o ubicación. Los bloques deben ser reutilizables, con nombres semánticos y funcionales, no genéricos, utilitarios ni específicos para una plantilla.
   - **Correcto**: `.card`, `.toolbar`, `.ads`, `.grid`, `.messages`, `.list` (componentes reutilizables)
   - **Incorrecto**: `.create-order`, `.auth`, `.new-table` (específicos de página), `.text-small`, `.mt-1`, `.p-1` (clases utilitarias)
3. **Archivo separado**: Crear nuevo archivo en `static/css/`.
4. **Documentar**: Incluir comentario de cabecera explicando propósito.
5. **Variables**: Definir variables CSS para temas.
6. **Probar**: Verificar en temas claro y oscuro.

## Filosofía BEM - No usar clases utilitarias

**IMPORTANTE**: En la metodología BEM, **NO se deben crear clases utilitarias** como `.flex`, `.grid`, `.mt-1`, `.text-center`, etc. Tampoco se deben crear bloques específicos para una plantilla (ej. `.create-order`, `.auth`, `.new-table`). Estas clases violan los principios de BEM porque:

1. **No son bloques independientes**: Solo modifican propiedades CSS individuales o están atados a un contexto específico.
2. **Rompen la encapsulación**: Los estilos se dispersan en múltiples clases.
3. **Dificultan el mantenimiento**: Cambiar el diseño requiere modificar HTML, no CSS.
4. **Reducen reutilización**: Los bloques específicos de página no pueden ser reutilizados en otros contextos.

### Enfoque correcto en BEM

- **Crear bloques semanticos**: `.card`, `.nav`, `.modal` (no `.flex-container`, `.grid-layout`)
- **Usar elementos dentro de bloques**: `.card__header`, `.nav__menu` (no `.mt-3`, `.text-right`)
- **Aplicar modificadores para variantes**: `.card--featured`, `.nav--sticky` (no clases utilitarias)

### Ejemplo incorrecto vs correcto

```html
<!-- INCORRECTO: Clases utilitarias -->
<div class="flex justify-between items-center mt-4 mb-2">
  <h3 class="text-lg font-bold text-primary">Título</h3>
  <button class="btn btn--primary">Acción</button>
</div>

<!-- CORRECTO: Bloque BEM -->
<div class="card__header">
  <h3 class="card__title">Título</h3>
  <button class="card__button card__button--primary">Acción</button>
</div>
```

En el CSS correspondiente:

```css
.card__header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: var(--space-lg);
  margin-bottom: var(--space-sm);
}

.card__title {
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--color-primary);
}

.card__button {
  /* estilos específicos para el botón dentro del card */
}
```

### Bloques Implementados

Los siguientes bloques están implementados en `static/css/`:

- **`base.css`** – Variables de tema, reset básico, utilidades
- **`nav.css`** – Navegación (`.nav`, `.nav__menu`, `.nav__item`, etc.)
- **`card.css`** – Tarjetas (`.card`, `.card__header`, `.card__body`, etc.)
- **`modal.css`** – Modales (`.modal`, `.modal__dialog`, `.modal__header`, etc.)
- **`form.css`** – Formularios (`.form`, `.form__group`, `.form__control`, etc.)
- **`table.css`** – Tablas (`.table`, `.table--striped`, `.table--responsive`, etc.)
- **`messages.css`** – Mensajes y alertas (`.message`, `.message--success`, `.message--warning`, etc.)
- **`main.css`** – Contenido principal (`.main`, `.main__container`, etc.)
- **`footer.css`** – Pie de página (`.footer`, `.footer__container`, etc.)

### Bloques Específicos del Proyecto

- `.order-card` - Tarjeta para mostrar órdenes
- `.inventory-item` - Item de inventario
- `.sales-summary` - Resumen de ventas

**Nota**: Aunque estos bloques son específicos del dominio del proyecto, deben ser diseñados como componentes reutilizables dentro del sistema. Sus nombres describen su propósito funcional (ej. mostrar una orden, item de inventario, resumen de ventas) y no están atados a una plantilla específica.

## Integración con Django Templates

### Carga de Estilos

El layout base (`layout.html`) carga los bloques CSS esenciales para la estructura común (base, navegación, mensajes, contenido principal y pie de página). Cada template puede importar bloques adicionales según sus necesidades mediante el bloque `extra_css`.

**Bloques cargados por defecto en `layout.html`:**
```html
<link rel="stylesheet" href="{% static 'css/base.css' %}">
<link rel="stylesheet" href="{% static 'css/nav.css' %}">
<link rel="stylesheet" href="{% static 'css/messages.css' %}">
<link rel="stylesheet" href="{% static 'css/main.css' %}">
<link rel="stylesheet" href="{% static 'css/footer.css' %}">
```

### Bloques Extra para Templates

Cada template puede agregar CSS y JavaScript adicional mediante los bloques `extra_css` y `extra_js`:

**En el template base (`layout.html`):**

```html
<head>
  <!-- ... -->
  {% block extra_css %}{% endblock %}
</head>
<body>
  <!-- ... -->
  {% block extra_js %}{% endblock %}
</body>
```

**En un template específico:**

```html
{% extends 'layout.html' %} {% load static %} {% block extra_css %}
<link rel="stylesheet" href="{% static 'css/mi-estilo-especifico.css' %}" />
{% endblock %} {% block extra_js %}
<script src="{% static 'js/mi-script-especifico.js' %}"></script>
{% endblock %} {% block body %}
<!-- Contenido del template -->
{% endblock %}
```

### Uso de Bloques BEM en HTML

```html
<article class="card card--featured">
  <header class="card__header">
    <h3 class="card__title">Título de la tarjeta</h3>
  </header>
  <div class="card__body">
    <p>Contenido de la tarjeta</p>
  </div>
  <footer class="card__footer">
    <button class="btn btn--primary">Acción</button>
  </footer>
</article>
```

## Actualización de Documentación

Cada vez que se cree un nuevo bloque o archivo CSS, se debe:

1. Actualizar este documento agregando el bloque en la sección correspondiente.
2. Actualizar `AGENTS.md` para mantener contexto de las convenciones.
3. Asegurar que el archivo esté disponible en `static/css/` para su importación selectiva. Opcionalmente, se puede agregar al archivo `styles.css` (bundle completo) si se desea mantener compatibilidad.

---

_Última actualización: 2026-02-26_
