# Sistema Buffet San Patricio

Sistema de gestión integral para el restaurante **Buffet San Patricio**, diseñado para manejar mesas, comandas, inventario, facturación y reportes de ventas.

---

## Descripción General

**Buffet San Patricio** es un sistema de punto de venta (POS) especializado para restaurantes tipo buffet. Maneja múltiples áreas de producción (cocina, bar, cafetería), control de inventario basado en recetas, y genera reportes detallados de ventas.

### Características Principales

- **Gestión de mesas y comandas** en tiempo real
- **Recetas por producto** con control automático de inventario
- **Múltiples áreas de despacho** (cocina, bar, cafetería)
- **Facturación** con métodos de pago (contado/crédito)
- **Arqueo de caja** por turno
- **Reportes de ventas** por producto y período
- **Control de inventario** con movimientos de entrada/salida
- **Sistema de permisos** por roles (Servicio, Supervisor, Administrador, Cocinero, Cajero)

---

## Arquitectura del Sistema

### Stack Tecnológico

| Componente | Tecnología |
|------------|------------|
| Framework | Django 5.2.7 |
| Base de datos | SQLite |
| Frontend | AlpineJS + Bootstrap 5 (CDN) |
| Iconos | Google Material Icons (CDN) |
| Tablas interactivas | GridJS |
| Lenguaje | Python 3.12+ |
| Localización | Español (Nicaragua) |

### Estructura del Proyecto

```
buffet-san-patricio/
├── core/                 # Configuración de Django
│   ├── settings.py        # Configuración principal
│   ├── urls.py           # URLs del proyecto
│   ├── wsgi.py           # Punto de entrada WSGI
│   └── asgi.py           # Punto de entrada ASGI
├── orders/               # App principal de órdenes
│   ├── models.py         # Modelos de datos
│   ├── views.py          # Vistas y lógica de negocio
│   ├── urls.py           # URLs de la app
│   ├── forms.py          # Formularios
│   └── admin.py          # Configuración admin
├── users/                # App de usuarios y permisos
│   ├── models.py         # Modelos de usuario
│   ├── views.py          # Vistas de autenticación
│   ├── permissions.py    # Definición de roles y permisos
│   └── utils.py          # Utilidades de verificación
├── templates/            # Templates HTML
│   ├── layout.html       # Template base
│   ├── dashboard.html    # Panel principal
│   ├── pos/              # Módulo POS (mesas, comandas)
│   ├── menu/             # Gestión de productos
│   ├── inventory/        # Inventario
│   ├── invoices/         # Facturación
│   ├── cash/             # Arqueo de caja
│   ├── reports/          # Reportes
│   └── settings/         # Configuración
├── static/               # Archivos estáticos
│   ├── css/              # Estilos personalizados
│   └── js/               # JavaScript personalizado
├── docs/                 # Documentación
├── db.sqlite3            # Base de datos
├── requirements.txt      # Dependencias
└── manage.py             # Utilidad Django
```

### Configuración de Entorno

El sistema usa un archivo `.secret` para cargar variables de entorno:

| Variable | Descripción | Valor por defecto |
|----------|-------------|-------------------|
| `DJANGO_SECRET_KEY` | Clave secreta de Django | (generada automáticamente) |
| `DJANGO_DEBUG` | Modo debug (`True`/`False`) | `False` |
| `DJANGO_ALLOWED_HOSTS` | Hosts permitidos (producción) | `localhost,127.0.0.1` |

---

## Módulos del Sistema

### 1. POS - Mesas y Comandas

Gestión de mesas del restaurante y creación/edición de comandas.

**URLs principales:**
- `/pos/` - Lista de mesas con totales pendientes
- `/pos/table/<id>/` - Órdenes activas de una mesa
- `/pos/table/<id>/new/` - Crear nueva orden
- `/pos/order/<id>/` - Detalle de una orden
- `/pos/order/<id>/edit/` - Editar orden
- `/pos/order/<id>/print/` - Imprimir comanda

**Funcionalidades:**
- Crear órdenes seleccionando productos y cantidades
- Ver órdenes pendientes por mesa
- Marcar órdenes como pagadas
- Editar mesa o usuario asignado a una orden
- Impresión de comandas para cocina

**Flujo de trabajo:**
1. El servicio selecciona una mesa vacía
2. Crea una nueva orden agregando productos
3. La cocina ve las comandas y prepara los pedidos
4. Al finalizar, el cajero genera la factura y cobra

---

### 2. Menú - Productos, Categorías y Áreas

Gestión del catálogo de productos y su organización.

**URLs principales:**
- `/menu/products/` - Lista de productos
- `/menu/products/new/` - Crear producto
- `/menu/products/<id>/edit/` - Editar producto
- `/menu/products/<id>/recipes/` - Gestionar receta del producto
- `/menu/categories/` - Lista de categorías
- `/menu/dispatch-areas/` - Lista de áreas de despacho

**Modelos:**

#### ProductCategory
Categorías para agrupar productos (ej: Entradas, Principales, Bebidas, Postres).

#### DispatchArea
Áreas donde se preparan los productos (ej: Cocina, Bar, Cafetería, Parrilla).

#### Product
- `name`: Nombre del producto
- `category`: Categoría a la que pertenece
- `dispatch_area`: Área donde se prepara
- `price`: Precio de venta

**Recetas (ProductIngredient)**
Cada producto tiene una receta que define qué ingredientes necesita y en qué cantidad. Estas recetas se usan para descontar automáticamente del inventario al crear una orden.

---

### 3. Inventario - Ingredientes y Movimientos

Control de stock de ingredientes con registro de movimientos.

**URLs principales:**
- `/inventory/ingredients/` - Lista de ingredientes
- `/inventory/ingredients/new/` - Crear ingrediente
- `/inventory/ingredients/<id>/edit/` - Editar ingrediente
- `/inventory/adjust/` - Ajuste de inventario físico
- `/inventory/purchase/` - Registrar compras

**Modelos:**

#### Ingredient
- `name`: Nombre del ingrediente
- `stock_quantity`: Cantidad actual en stock
- `unit`: Unidad de medida (oz, lb, g, kg, ml, l, und)
- `warehouse`: Bodega donde se almacena

#### Warehouse
Bodegas o ubicaciones de almacenamiento (ej: Principal, Secundario).

#### IngredientMovement
Registro de movimientos de inventario:
- `ingredient`: Ingrediente afectado
- `quantity`: Cantidad (positiva = ingreso, negativa = salida)
- `reason`: Motivo del movimiento
- `user`: Usuario que realizó el movimiento
- `created_at`: Fecha y hora

**Tipos de movimientos:**
1. **Compra de ingredientes**: Registrar ingresos por compras
2. **Ajuste de inventario**: Corrección física del stock
3. **Uso en comandas**: Descontaje automático por recetas (al crear OrderItem)

**Flujo de trabajo:**
1. Se registran las compras de ingredientes
2. Al crear una orden, se reservan los ingredientes según recetas
3. Periódicamente se hace ajuste físico del inventario
4. Los reportes muestran movimientos y saldos

---

### 4. Facturación

Generación de facturas para las órdenes pagadas.

**URLs principales:**
- `/invoices/` - Lista de facturas
- `/pos/table/<id>/invoice/` - Generar factura para una mesa
- `/invoices/<id>/print/` - Imprimir factura

**Modelos:**

#### Invoice
- `invoice_number`: Número secuencial único
- `table`: Mesa asociada (opcional)
- `user`: Usuario que creó la orden
- `cashier`: Cajero que facturó
- `subtotal`: Subtotal antes de impuestos
- `total`: Total a pagar
- `payment_method`: CONTADO o CREDITO
- `created_at`: Fecha y hora
- `is_active`: Si la factura está activa

#### InvoiceItem
- `invoice`: Factura a la que pertenece
- `product`: Producto vendido
- `quantity`: Cantidad
- `unit_price`: Precio unitario
- `total`: Total de la línea

**Flujo de trabajo:**
1. El cliente solicita la cuenta
2. El cajero genera la factura consolidando todas las órdenes
3. Se selecciona método de pago (contado/crédito)
4. Se actualiza el arqueo de caja según el método
5. La factura se puede imprimir en formato térmico

---

### 5. Arqueo de Caja

Control de turnos de caja y cuadre diario.

**URLs principales:**
- `/cash/` - Lista de arqueos
- `/cash/open/` - Abrir turno
- `/cash/<id>/` - Ver detalle del turno
- `/cash/<id>/close/` - Cerrar turno

**Modelo:**

#### CashRegister
- `user`: Cajero responsable
- `date`: Fecha del turno
- `opening_amount`: Monto de apertura
- `closing_amount`: Monto de cierre (al cerrar)
- `total_sales`: Total de ventas del turno
- `total_contado`: Ventas al contado
- `total_credito`: Ventas a crédito
- `closing_time`: Hora de cierre
- `notes`: Notas adicionales

**Flujo de trabajo:**
1. El cajero abre su turno indicando el monto de apertura
2. Durante el turno, cada venta al contado suma a `total_contado`
3. Al finalizar, el cajero cierra el turno indicando el monto en caja
4. El sistema calcula si hay diferencia (sobra/falta)

---

### 6. Reportes

Módulo de generación de reportes y exportaciones.

**URLs principales:**
- `/reports/` - Panel de reportes
- `/reports/inventory/` - Saldo de inventario
- `/reports/movements/` - Movimientos de inventario
- `/reports/sales-by-product/` - Ventas por producto
- `/orders/daily/` - Ventas del día
- `/orders/report/` - Comandas por período

**Tipos de reportes:**
1. **Saldo de inventario**: Stock actual de todos los ingredientes
2. **Movimientos de inventario**: Historial de entradas y salidas
3. **Ventas por producto**: Totales vendidos por producto en un período
4. **Ventas del día**: Resumen de ventas diarias
5. **Comandas**: Detalle de todas las comandas en un período

**Exportaciones:**
Todos los reportes supportan exportación a CSV para análisis en Excel.

---

### 7. Dashboard

Panel principal que muestra información relevante según el rol del usuario.

**URL:** `/dashboard/`

**Datos mostrados:**
- Ventas del día (total y por área de despacho)
- Gráfico de ventas últimos 7 días
- Ingredientes con stock bajo
- Órdenes pendientes por mesa

---

## Modelos de Datos

### Diagrama de Relaciones

```
┌─────────────┐       ┌─────────────────┐
│   Table     │       │ ProductCategory │
└──────┬──────┘       └────────┬────────┘
       │                       │
       │    ┌─────────────────┘
       │    │
       ▼    ▼
┌──────────────────────────────────┐
│           Order                  │
│  (table, user, is_paid, created) │
└──────┬───────────────────┬───────┘
       │                   │
       ▼                   ▼
┌─────────────┐   ┌─────────────────┐
│  OrderItem  │   │     Invoice     │
│ (order,     │   │(table, cashier, │
│  product,   │   │ payment_method) │
│  quantity)  │   └────────┬────────┘
└──────┬──────┘          │
       │                 │
       ▼                 ▼
┌─────────────┐   ┌─────────────────┐
│   Product   │   │   InvoiceItem    │
│ (name,      │   │ (invoice,       │
│  category,  │   │  product, qty)  │
│  price)     │   └─────────────────┘
└──────┬──────┘
       │
       ▼
┌─────────────────────┐
│ ProductIngredient    │
│ (product, ingredient│
│  quantity)          │
└──────┬──────────────┘
       │
       ▼
┌─────────────┐   ┌──────────────────┐
│ Ingredient  │◄──│IngredientMovement│
│ (stock_qty, │   │ (quantity, reason│
│  unit)      │   │  user, created)  │
└─────────────┘   └──────────────────┘
```

### Resumen de Modelos

| Modelo | Descripción | App |
|--------|-------------|-----|
| `Table` | Mesas del restaurante | orders |
| `ProductCategory` | Categorías de productos | orders |
| `DispatchArea` | Áreas de despacho | orders |
| `Warehouse` | Bodegas de almacenamiento | orders |
| `Product` | Productos del menú | orders |
| `Ingredient` | Ingredientes del inventario | orders |
| `ProductIngredient` | Recetas (relación producto-ingrediente) | orders |
| `IngredientMovement` | Movimientos de inventario | orders |
| `Order` | Órdenes/Comandas | orders |
| `OrderItem` | Items de una orden | orders |
| `Invoice` | Facturas | orders |
| `InvoiceItem` | Items de una factura | orders |
| `CashRegister` | Arqueos de caja | orders |
| `Company` | Datos de la empresa | orders |

---

## Sistema de Permisos

### Grupos de Usuarios

El sistema define 5 grupos con permisos preestablecidos:

| Grupo | Descripción | Permisos principales |
|-------|-------------|----------------------|
| **Servicio** | Meseros y personal de piso | Crear/ver órdenes, ver productos |
| **Cocinero** | Personal de cocina | Ver órdenes, ver productos/ingredientes |
| **Cajero** | Personal de caja | Órdenes, facturación, arqueo de caja |
| **Supervisor** | Encargados de turno | Inventario, movimientos, cierres |
| **Administrador** | Gerencia | Acceso completo al sistema |

### Permisos por Grupo

#### Servicio
- Ver mesas, productos, categorías, áreas
- Crear y modificar órdenes propias
- Ver órdenes pendientes

#### Cocinero
- Ver mesas y órdenes
- Ver productos, categorías, áreas
- Ver ingredientes y recetas

#### Cajero
- Ver y crear órdenes
- Marcar órdenes como pagadas
- Facturar mesas
- Abrir/cerrar caja
- Ver reportes de ventas

#### Supervisor
- Todo lo de Cajero
- Registrar movimientos de inventario
- Ver reportes de inventario

#### Administrador
- Acceso completo a todas las funcionalidades
- Gestionar usuarios y permisos
- Configurar empresa
- Gestionar productos, categorías, áreas
- Gestionar ingredientes y recetas

---

## API Endpoints

El sistema expone endpoints JSON para consumo por GridJS y otras herramientas.

### Endpoints de Listado

| Endpoint | Descripción |
|----------|-------------|
| `/api/ingredients/` | Lista de ingredientes |
| `/api/products/` | Lista de productos |
| `/api/categories/` | Lista de categorías |
| `/api/dispatch-areas/` | Lista de áreas de despacho |
| `/api/tables/` | Lista de mesas |
| `/api/orders/` | Lista de órdenes |
| `/api/invoices/` | Lista de facturas |
| `/api/movements/` | Movimientos de inventario |
| `/api/inventory/` | Inventario con paginación |
| `/api/sales-by-product/` | Ventas por producto con paginación |
| `/api/orders-report/` | Reporte de órdenes con paginación |
| `/api/sales-today/` | Ventas del día actual |
| `/api/cash/status/` | Estado de caja actual |

### Formato de Respuesta

Los endpoints con paginación retornan:

```json
{
  "count": 150,
  "results": [
    {
      "id": 1,
      "campo1": "valor1",
      "campo2": "valor2"
    }
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
| `start` | Fecha/hora de inicio (formato: `YYYY-MM-DDTHH:MM`) |
| `end` | Fecha/hora de fin (formato: `YYYY-MM-DDTHH:MM`) |

---

## Guía de Desarrollo

### Convenciones de Código

1. **Idioma del código**: Todos los identificadores en inglés
2. **Idioma de documentación**: Español
3. **Idioma de interfaz**: Español (Nicaragua)
4. **Strings**: Usar comillas dobles (`"`)
5. **Imports**: Agrupar (stdlib, third-party, local) con blank lines

### Patrones de Vistas

```python
@login_required
@user_passes_test(has_valid_role)
def mi_vista(request):
    """Descripción de la vista en español."""
    # Lógica de negocio
    return render(request, "ruta/template.html", context)
```

### Patrones de Modelos

```python
class MiModelo(models.Model):
    name = models.CharField(max_length=255, verbose_name="Nombre")

    class Meta:
        verbose_name = "Modelo"
        verbose_name_plural = "Modelos"

    def __str__(self):
        return self.name

    def un_metodo(self):
        """Descripción del método."""
        pass
```

### Formularios y Validación

- Usar `transaction.atomic` para operaciones que deben ser atómicas
- Usar `messages` de Django para feedback al usuario
- Usar `get_object_or_404` para obtener objetos
- Validar datos en el backend (nunca confiar en el frontend)

---

## Flujos de Trabajo Comunes

### Crear una Nueva Orden

1. Ir a `/pos/` y seleccionar una mesa
2. Clic en "Nueva Orden"
3. Seleccionar productos y cantidades
4. Confirmar creación
5. La orden aparece en la lista de pendientes

### Registrar Compra de Ingredientes

1. Ir a Inventario > Ingresos
2. Ingresar cantidades compradas por ingrediente
3. Confirmar registro
4. Los ingredientes suman al stock

### Facturar una Mesa

1. Ir a la lista de mesas (`/pos/`)
2. Seleccionar mesa con órdenes pendientes
3. Clic en "Facturar"
4. Elegir método de pago
5. Confirmar (marca órdenes como pagadas y suma al arqueo)

### Cerrar un Turno de Caja

1. Ir a Caja > Arqueo de Caja
2. Seleccionar turno activo
3. Clic en "Cerrar Turno"
4. Ingresar monto en caja al cerrar
5. El sistema muestra diferencia (sobra/falta)

---

## Configuración

### Empresa

El sistema permite configurar los datos de la empresa (visible en facturas):

- Nombre de la empresa
- RUC
- Dirección
- Teléfono
- Correo electrónico
- Logo
- Eslogan

**URL:** `/empresa/configuracion/` o `/settings/company/`

---

## Mantenimiento

### Comandos de Gestión

```bash
# Servidor de desarrollo
python manage.py runserver

# Aplicar migraciones
python manage.py migrate

# Crear migraciones
python manage.py makemigrations

# Shell de Django
python manage.py shell

# Recolectar archivos estáticos
python manage.py collectstatic
```

### Respaldo de Base de Datos

El archivo `db.sqlite3` contiene todos los datos. Respaldar regularmente.

---

## Glosario

| Término | Descripción |
|---------|-------------|
| **Comanda** | Orden de un cliente con productos solicitados |
| **Mesa** | Mesa física del restaurante |
| **Área de despacho** | Sección donde se prepara un producto (cocina, bar) |
| **Receta** | Lista de ingredientes y cantidades para un producto |
| **Movimiento** | Entrada o salida de un ingrediente |
| **Factura** | Documento legal de una venta |
| **Arqueo de caja** | Control de efectivo por turno |
| **POS** | Point of Sale - Sistema de punto de venta |

---

_Last updated: 2026-04-17_
