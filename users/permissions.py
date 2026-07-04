"""
Definición de grupos y permisos fijos para el sistema Buffet San Patricio.

Los grupos son fijos (no configurables) y tienen permisos predefinidos.
"""

from django.contrib.auth.models import Permission

# ==========================
# 📋 NOMBRES DE GRUPOS
# ==========================

GROUP_SERVICIO = "Servicio"
GROUP_SUPERVISOR = "Supervisor"
GROUP_ADMINISTRADOR = "Administrador"
GROUP_COCINERO = "Cocinero"
GROUP_CAJERO = "Cajero"

ALL_GROUPS = [
    GROUP_SERVICIO,
    GROUP_SUPERVISOR,
    GROUP_ADMINISTRADOR,
    GROUP_COCINERO,
    GROUP_CAJERO,
]

# ==========================
# 📝 DESCRIPCIONES DE ROLES
# ==========================

ROLE_DESCRIPTIONS = {
    GROUP_SERVICIO: {
        "name": "Servicio",
        "description": "Meseros y personal de piso. Encargados de tomar pedidos y gestionar órdenes de los clientes en las mesas.",
        "color": "success",
        "icon": "room_service"
    },
    GROUP_COCINERO: {
        "name": "Cocinero",
        "description": "Personal de cocina. Puede ver las órdenes pendientes y usar el conversor de alimentos para calcular recetas.",
        "color": "success",
        "icon": "restaurant"
    },
    GROUP_CAJERO: {
        "name": "Cajero",
        "description": "Personal de caja. Encargado de cobrar a los clientes, generar facturas y gestionar el arqueo de caja diario.",
        "color": "info",
        "icon": "point_of_sale"
    },
    GROUP_SUPERVISOR: {
        "name": "Supervisor",
        "description": "Encargados de turno. Tienen acceso a inventario, reportes y movimientos de caja para supervisar operaciones.",
        "color": "warning",
        "icon": "supervisor_account"
    },
    GROUP_ADMINISTRADOR: {
        "name": "Administrador",
        "description": "Gerencia con acceso completo al sistema. Puede gestionar usuarios, permisos, productos, inventario y configuración.",
        "color": "danger",
        "icon": "admin_panel_settings"
    },
}

# ==========================
# 📋 DESCRIPCIONES DETALLADAS DE PERMISOS
# ==========================

PERMISSION_DESCRIPTIONS = {
    # === MESAS ===
    "view_table": {
        "name": "Ver Mesas",
        "description": "Permite ver la lista de mesas del restaurante con su estado actual (ocupada o disponible).",
        "use_case": "Necesario para que meseros y cajeros puedan identificar qué mesa cobrar o atender.",
        "group": "Mesas",
        "group_order": 1,
    },
    "add_table": {
        "name": "Crear Mesas",
        "description": "Permite agregar nuevas mesas al restaurante.",
        "use_case": "Para expandir el restaurante o reconfigurear las mesas disponibles.",
        "group": "Mesas",
        "group_order": 1,
    },
    "change_table": {
        "name": "Editar Mesas",
        "description": "Permite modificar los datos de una mesa (nombre, capacidad).",
        "use_case": "Cuando se necesita renombrar una mesa o cambiar su capacidad.",
        "group": "Mesas",
        "group_order": 1,
    },
    "delete_table": {
        "name": "Eliminar Mesas",
        "description": "Permite eliminar una mesa del sistema (soft delete).",
        "use_case": "Cuando una mesa se retira permanentemente del restaurante.",
        "group": "Mesas",
        "group_order": 1,
    },

    # === CATEGORÍAS DE PRODUCTOS ===
    "view_productcategory": {
        "name": "Ver Categorías",
        "description": "Permite ver la lista de categorías de productos (Entradas, Principales, Bebidas, Postres).",
        "use_case": "Para que meseros y cocineros puedan navegar el menú por categorías.",
        "group": "Menú",
        "group_order": 2,
    },
    "add_productcategory": {
        "name": "Crear Categorías",
        "description": "Permite crear nuevas categorías para agrupar productos.",
        "use_case": "Para agregar nuevas secciones al menú del restaurante.",
        "group": "Menú",
        "group_order": 2,
    },
    "change_productcategory": {
        "name": "Editar Categorías",
        "description": "Permite modificar el nombre u orden de una categoría.",
        "use_case": "Cuando se necesita renombrar una categoría o cambiar su posición.",
        "group": "Menú",
        "group_order": 2,
    },
    "delete_productcategory": {
        "name": "Eliminar Categorías",
        "description": "Permite eliminar una categoría (soft delete).",
        "use_case": "Cuando una categoría ya no es necesaria.",
        "group": "Menú",
        "group_order": 2,
    },

    # === ÁREAS DE DESPACHO ===
    "view_dispatcharea": {
        "name": "Ver Áreas de Despacho",
        "description": "Permite ver las áreas donde se preparan los productos (Cocina, Bar, Cafetería).",
        "use_case": "Para identificar dónde se prepara cada producto del menú.",
        "group": "Menú",
        "group_order": 2,
    },
    "add_dispatcharea": {
        "name": "Crear Áreas de Despacho",
        "description": "Permite crear nuevas áreas de preparación.",
        "use_case": "Para agregar nuevas estaciones de trabajo (ej: Parrilla, Repostería).",
        "group": "Menú",
        "group_order": 2,
    },
    "change_dispatcharea": {
        "name": "Editar Áreas de Despacho",
        "description": "Permite modificar el nombre de un área de despacho.",
        "use_case": "Cuando se necesita renombrar una estación de trabajo.",
        "group": "Menú",
        "group_order": 2,
    },
    "delete_dispatcharea": {
        "name": "Eliminar Áreas de Despacho",
        "description": "Permite eliminar un área de despacho (soft delete).",
        "use_case": "Cuando un área de trabajo se desactiva.",
        "group": "Menú",
        "group_order": 2,
    },

    # === BODEGAS ===
    "view_warehouse": {
        "name": "Ver Bodegas",
        "description": "Permite ver la lista de bodegas o almacenes donde se guardan los ingredientes.",
        "use_case": "Para conocer dónde está almacenado cada ingrediente.",
        "group": "Inventario",
        "group_order": 3,
    },
    "add_warehouse": {
        "name": "Crear Bodegas",
        "description": "Permite crear nuevas bodegas o ubicaciones de almacenamiento.",
        "use_case": "Para agregar nuevas áreas de almacenamiento (ej: Cuarto frío, Alacena).",
        "group": "Inventario",
        "group_order": 3,
    },
    "change_warehouse": {
        "name": "Editar Bodegas",
        "description": "Permite modificar el nombre de una bodega.",
        "use_case": "Cuando se necesita renombrar una ubicación de almacenamiento.",
        "group": "Inventario",
        "group_order": 3,
    },
    "delete_warehouse": {
        "name": "Eliminar Bodegas",
        "description": "Permite eliminar una bodega (soft delete).",
        "use_case": "Cuando un área de almacenamiento se desactiva.",
        "group": "Inventario",
        "group_order": 3,
    },

    # === PRODUCTOS ===
    "view_product": {
        "name": "Ver Productos",
        "description": "Permite ver el catálogo de productos con sus precios, categorías y áreas de despacho.",
        "use_case": "Necesario para que meseros puedan mostrar el menú a los clientes y tomar pedidos.",
        "group": "Menú",
        "group_order": 2,
    },
    "add_product": {
        "name": "Crear Productos",
        "description": "Permite agregar nuevos platos o bebidas al menú del restaurante.",
        "use_case": "Para incorporar nuevos platillos al buffet.",
        "group": "Menú",
        "group_order": 2,
    },
    "change_product": {
        "name": "Editar Productos",
        "description": "Permite modificar productos existentes (precio, nombre, categoría).",
        "use_case": "Cuando se actualizan precios o se corrigen datos de un producto.",
        "group": "Menú",
        "group_order": 2,
    },
    "delete_product": {
        "name": "Eliminar Productos",
        "description": "Permite eliminar un producto del menú (soft delete).",
        "use_case": "Cuando un producto se deja de ofrecer temporalmente.",
        "group": "Menú",
        "group_order": 2,
    },

    # === INGREDIENTES ===
    "view_ingredient": {
        "name": "Ver Ingredientes",
        "description": "Permite ver la lista de ingredientes con su stock actual y unidad de medida.",
        "use_case": "Para que cocineros y supervisores puedan verificar disponibilidad de insumos.",
        "group": "Inventario",
        "group_order": 3,
    },
    "add_ingredient": {
        "name": "Crear Ingredientes",
        "description": "Permite agregar nuevos ingredientes al inventario.",
        "use_case": "Para dar de alta nuevos insumos que se compren regularmente.",
        "group": "Inventario",
        "group_order": 3,
    },
    "change_ingredient": {
        "name": "Editar Ingredientes",
        "description": "Permite modificar ingredientes existentes (nombre, unidad, stock mínimo).",
        "use_case": "Cuando se corrigen datos de un ingrediente o se ajusta el stock mínimo.",
        "group": "Inventario",
        "group_order": 3,
    },
    "delete_ingredient": {
        "name": "Eliminar Ingredientes",
        "description": "Permite eliminar un ingrediente del inventario (soft delete).",
        "use_case": "Cuando un ingrediente ya no se usa en ninguna receta.",
        "group": "Inventario",
        "group_order": 3,
    },

    # === RECETAS DE PRODUCTO ===
    "view_productingredient": {
        "name": "Ver Recetas de Producto",
        "description": "Permite ver qué ingredientes necesita cada producto y en qué cantidad.",
        "use_case": "Para que cocineros conozcan las porciones exactas de cada platillo.",
        "group": "Menú",
        "group_order": 2,
    },
    "add_productingredient": {
        "name": "Crear Recetas de Producto",
        "description": "Permite definir los ingredientes y cantidades necesarios para un producto.",
        "use_case": "Para configurar qué ingredientes se descontarán del inventario al vender un producto.",
        "group": "Menú",
        "group_order": 2,
    },
    "change_productingredient": {
        "name": "Editar Recetas de Producto",
        "description": "Permite modificar las cantidades de ingredientes en una receta.",
        "use_case": "Cuando se ajustan las porciones de un platillo.",
        "group": "Menú",
        "group_order": 2,
    },
    "delete_productingredient": {
        "name": "Eliminar Recetas de Producto",
        "description": "Permite eliminar un ingrediente de una receta.",
        "use_case": "Cuando un producto ya no usa cierto insumo.",
        "group": "Menú",
        "group_order": 2,
    },

    # === MOVIMIENTOS DE INVENTARIO ===
    "view_ingredientmovement": {
        "name": "Ver Movimientos de Inventario",
        "description": "Permite ver el historial de entradas y salidas de ingredientes.",
        "use_case": "Para rastrear de dónde vienen los ingredientes y dónde se usaron.",
        "group": "Inventario",
        "group_order": 3,
    },
    "add_ingredientmovement": {
        "name": "Registrar Movimientos",
        "description": "Permite registrar entradas (compras) y salidas de ingredientes.",
        "use_case": "Para registrar las compras de insumos y los ajustes de inventario.",
        "group": "Inventario",
        "group_order": 3,
    },
    "change_ingredientmovement": {
        "name": "Editar Movimientos",
        "description": "Permite modificar un movimiento de inventario existente.",
        "use_case": "Para corregir errores en el registro de movimientos.",
        "group": "Inventario",
        "group_order": 3,
    },
    "delete_ingredientmovement": {
        "name": "Eliminar Movimientos",
        "description": "Permite eliminar un movimiento de inventario.",
        "use_case": "Cuando se detecta un movimiento registrado incorrectamente.",
        "group": "Inventario",
        "group_order": 3,
    },

    # === ÓRDENES ===
    "view_order": {
        "name": "Ver Órdenes",
        "description": "Permite ver la lista de órdenes pendientes y su historial.",
        "use_case": "Necesario para que cocineros vean qué preparar y cajeros qué cobrar.",
        "group": "Órdenes",
        "group_order": 4,
    },
    "add_order": {
        "name": "Crear Órdenes",
        "description": "Permite crear nuevas órdenes para las mesas del restaurante.",
        "use_case": "Para registrar los pedidos de los clientes en cada mesa.",
        "group": "Órdenes",
        "group_order": 4,
    },
    "change_order": {
        "name": "Editar Órdenes",
        "description": "Permite modificar órdenes existentes y marcar como pagadas.",
        "use_case": "Para agregar productos a una orden o cerrar la cuenta de una mesa.",
        "group": "Órdenes",
        "group_order": 4,
    },
    "delete_order": {
        "name": "Eliminar Órdenes",
        "description": "Permite eliminar una orden del sistema.",
        "use_case": "Solo en casos excepcionales. Las órdenes generalmente no deben eliminarse.",
        "group": "Órdenes",
        "group_order": 4,
    },

    # === ITEMS DE ORDEN ===
    "view_orderitem": {
        "name": "Ver Items de Orden",
        "description": "Permite ver los productos específicos de cada orden con cantidades y precios.",
        "use_case": "Para ver el detalle de qué productos pidió cada mesa.",
        "group": "Órdenes",
        "group_order": 4,
    },
    "add_orderitem": {
        "name": "Agregar Items a Orden",
        "description": "Permite agregar productos a una orden existente.",
        "use_case": "Cuando un cliente quiere agregar más productos a su pedido.",
        "group": "Órdenes",
        "group_order": 4,
    },
    "change_orderitem": {
        "name": "Editar Items de Orden",
        "description": "Permite modificar las cantidades o productos de un item.",
        "use_case": "Para corregir la cantidad de un producto en la orden.",
        "group": "Órdenes",
        "group_order": 4,
    },
    "delete_orderitem": {
        "name": "Eliminar Items de Orden",
        "description": "Permite quitar un producto de una orden.",
        "use_case": "Cuando un cliente cancela un producto de su pedido.",
        "group": "Órdenes",
        "group_order": 4,
    },

    # === FACTURAS ===
    "view_invoice": {
        "name": "Ver Facturas",
        "description": "Permite ver el historial de facturas creadas.",
        "use_case": "Para reimprimir facturas o verificar transacciones anteriores.",
        "group": "Facturación",
        "group_order": 5,
    },
    "add_invoice": {
        "name": "Crear Facturas",
        "description": "Permite generar facturas para las órdenes pagadas.",
        "use_case": "Función principal del cajero para cobrar a los clientes.",
        "group": "Facturación",
        "group_order": 5,
    },
    "change_invoice": {
        "name": "Editar Facturas",
        "description": "Permite modificar una factura existente.",
        "use_case": "Para correcciones en caso de errores. Las facturas no deberían modificarse frecuentemente.",
        "group": "Facturación",
        "group_order": 5,
    },
    "delete_invoice": {
        "name": "Eliminar Facturas",
        "description": "Permite eliminar una factura del sistema.",
        "use_case": "No recomendado. Las facturas son documentos legales y no deberían borrarse.",
        "group": "Facturación",
        "group_order": 5,
    },

    # === ITEMS DE FACTURA ===
    "view_invoiceitem": {
        "name": "Ver Items de Factura",
        "description": "Permite ver el detalle de productos facturados.",
        "use_case": "Para ver qué productos incluía cada factura.",
        "group": "Facturación",
        "group_order": 5,
    },
    "add_invoiceitem": {
        "name": "Agregar Items a Factura",
        "description": "Permite agregar productos a una factura.",
        "use_case": "Para añadir cargos adicionales a una factura existente.",
        "group": "Facturación",
        "group_order": 5,
    },
    "change_invoiceitem": {
        "name": "Editar Items de Factura",
        "description": "Permite modificar productos en una factura.",
        "use_case": "Para corregir productos facturados erroneamente.",
        "group": "Facturación",
        "group_order": 5,
    },
    "delete_invoiceitem": {
        "name": "Eliminar Items de Factura",
        "description": "Permite quitar productos de una factura.",
        "use_case": "Para eliminar cargos incorrectos de una factura.",
        "group": "Facturación",
        "group_order": 5,
    },

    # === ARQUEO DE CAJA ===
    "view_cashregister": {
        "name": "Ver Arqueos de Caja",
        "description": "Permite ver el historial de arqueos de caja y turnos.",
        "use_case": "Para supervisores y administradores que necesitan auditar cajas.",
        "group": "Caja",
        "group_order": 6,
    },
    "add_cashregister": {
        "name": "Abrir Turno de Caja",
        "description": "Permite abrir un nuevo turno de caja indicando el monto de apertura.",
        "use_case": "Al iniciar la jornada, el cajero abre su caja con un monto inicial.",
        "group": "Caja",
        "group_order": 6,
    },
    "change_cashregister": {
        "name": "Cerrar Turno de Caja",
        "description": "Permite cerrar el turno actual indicando el monto final en caja.",
        "use_case": "Al finalizar la jornada, el cajero cierra su caja para calcular ganancias.",
        "group": "Caja",
        "group_order": 6,
    },
    "delete_cashregister": {
        "name": "Eliminar Arqueo",
        "description": "Permite eliminar un registro de arqueo de caja.",
        "use_case": "Solo para administradores en casos excepcionales.",
        "group": "Caja",
        "group_order": 6,
    },

    # === RECETAS DE CONVERSIÓN ===
    "view_foodrecipe": {
        "name": "Ver Recetas de Conversión",
        "description": "Permite ver recetas que convierten ingredientes brutos en productos preparados.",
        "use_case": "Para que cocineros vean cómo preparar ingredientes (ej: masa desde harina).",
        "group": "Inventario",
        "group_order": 3,
    },
    "add_foodrecipe": {
        "name": "Crear Recetas de Conversión",
        "description": "Permite crear recetas que definen cómo convertir ingredientes.",
        "use_case": "Para dar de alta conversiones como: 1kg harina + huevos → 2kg masa.",
        "group": "Inventario",
        "group_order": 3,
    },
    "change_foodrecipe": {
        "name": "Editar Recetas de Conversión",
        "description": "Permite modificar recetas de conversión existentes.",
        "use_case": "Cuando se ajustan las proporciones de una conversión.",
        "group": "Inventario",
        "group_order": 3,
    },
    "delete_foodrecipe": {
        "name": "Eliminar Recetas de Conversión",
        "description": "Permite eliminar una receta de conversión.",
        "use_case": "Cuando una receta de conversión ya no se usa.",
        "group": "Inventario",
        "group_order": 3,
    },

    # === USUARIOS Y GRUPOS (Auth) ===
    "view_user": {
        "name": "Ver Usuarios",
        "description": "Permite ver la lista de usuarios del sistema.",
        "use_case": "Para que administradores puedan ver qué usuarios existen.",
        "group": "Administración",
        "group_order": 7,
    },
    "add_user": {
        "name": "Crear Usuarios",
        "description": "Permite crear nuevos usuarios en el sistema.",
        "use_case": "Para dar de alta nuevos empleados.",
        "group": "Administración",
        "group_order": 7,
    },
    "change_user": {
        "name": "Editar Usuarios",
        "description": "Permite modificar datos de usuarios y cambiar contraseñas.",
        "use_case": "Para actualizar información de empleados o resetear contraseñas.",
        "group": "Administración",
        "group_order": 7,
    },
    "delete_user": {
        "name": "Eliminar Usuarios",
        "description": "Permite eliminar usuarios del sistema.",
        "use_case": "Cuando un empleado deja de trabajar en el restaurante.",
        "group": "Administración",
        "group_order": 7,
    },
    "view_group": {
        "name": "Ver Grupos",
        "description": "Permite ver los grupos de permisos del sistema.",
        "use_case": "Para consultar qué grupos de permisos existen.",
        "group": "Administración",
        "group_order": 7,
    },
    "add_group": {
        "name": "Crear Grupos",
        "description": "Permite crear nuevos grupos de permisos.",
        "use_case": "Para agregar nuevos roles al sistema (además de los 5 predefinidos).",
        "group": "Administración",
        "group_order": 7,
    },
    "change_group": {
        "name": "Editar Grupos",
        "description": "Permite modificar grupos de permisos.",
        "use_case": "Para cambiar los permisos asignados a un grupo.",
        "group": "Administración",
        "group_order": 7,
    },
    "delete_group": {
        "name": "Eliminar Grupos",
        "description": "Permite eliminar grupos de permisos.",
        "use_case": "Cuando un grupo ya no es necesario.",
        "group": "Administración",
        "group_order": 7,
    },
}

# ==========================
# 🔐 PERMISOS POR GRUPO
# ==========================

# Permisos de solo lectura (view) para modelos básicos
VIEW_ONLY_PERMS = [
    "view_table",
    "view_productcategory",
    "view_dispatcharea",
    "view_warehouse",
    "view_product",
    "view_ingredient",
    "view_productingredient",
    "view_ingredientmovement",
    "view_order",
    "view_orderitem",
]

# Permisos de gestión completa (add, change, delete, view) para modelos de configuración
FULL_MANAGEMENT_PERMS = [
    "add_table",
    "change_table",
    "delete_table",
    "view_table",
    "add_productcategory",
    "change_productcategory",
    "delete_productcategory",
    "view_productcategory",
    "add_dispatcharea",
    "change_dispatcharea",
    "delete_dispatcharea",
    "view_dispatcharea",
    "add_warehouse",
    "change_warehouse",
    "delete_warehouse",
    "view_warehouse",
    "add_product",
    "change_product",
    "delete_product",
    "view_product",
    "add_ingredient",
    "change_ingredient",
    "delete_ingredient",
    "view_ingredient",
    "add_productingredient",
    "change_productingredient",
    "delete_productingredient",
    "view_productingredient",
    "add_ingredientmovement",
    "change_ingredientmovement",
    "delete_ingredientmovement",
    "view_ingredientmovement",
    "add_order",
    "change_order",
    "delete_order",
    "view_order",
    "add_orderitem",
    "change_orderitem",
    "delete_orderitem",
    "view_orderitem",
    # Facturación
    "add_invoice",
    "change_invoice",
    "delete_invoice",
    "view_invoice",
    "add_invoiceitem",
    "change_invoiceitem",
    "delete_invoiceitem",
    "view_invoiceitem",
    # Arqueo de caja
    "add_cashregister",
    "change_cashregister",
    "delete_cashregister",
    "view_cashregister",
    # Recetas de conversión
    "add_foodrecipe",
    "change_foodrecipe",
    "delete_foodrecipe",
    "view_foodrecipe",
]

# Permisos de usuario y grupo (solo administrador)
USER_GROUP_PERMS = [
    "add_user",
    "change_user",
    "delete_user",
    "view_user",
    "add_group",
    "change_group",
    "delete_group",
    "view_group",
]

# Mapeo de grupos a permisos (nombres de permisos sin la app)
GROUP_PERMISSIONS = {
    GROUP_SERVICIO: [
        "view_table",
        "view_productcategory",
        "view_dispatcharea",
        "view_warehouse",
        "view_product",
        "view_ingredient",
        "view_productingredient",
        "view_ingredientmovement",
        "view_order",
        "view_orderitem",
        "add_order",
        "change_order",
        "add_orderitem",
        "change_orderitem",
    ],
    GROUP_SUPERVISOR: [
        # Inventario completo
        "view_ingredient",
        "change_ingredient",
        "view_ingredientmovement",
        "add_ingredientmovement",
        "change_ingredientmovement",
        "delete_ingredientmovement",
        # Productos (solo ver, no gestionar)
        "view_product",
        "view_productcategory",
        "view_dispatcharea",
        "view_warehouse",
        "view_productingredient",
        # Órdenes y mesas
        "view_table",
        "view_order",
        "view_orderitem",
        "add_order",
        "change_order",
        "delete_order",
        "add_orderitem",
        "change_orderitem",
        "delete_orderitem",
        # Facturación
        "add_invoice",
        "view_invoice",
        # Arqueo de caja
        "add_cashregister",
        "view_cashregister",
        "change_cashregister",
        # Recetas de conversión
        "add_foodrecipe",
        "change_foodrecipe",
        "view_foodrecipe",
        # Reportes
        # Nota: Los reportes no tienen permisos específicos, se controlan por vistas
    ],
    GROUP_ADMINISTRADOR: FULL_MANAGEMENT_PERMS + USER_GROUP_PERMS,
    GROUP_COCINERO: [
        # Mesas y órdenes (solo ver)
        "view_table",
        "view_order",
        "view_orderitem",
        # Productos e ingredientes (solo ver)
        "view_product",
        "view_productcategory",
        "view_dispatcharea",
        "view_warehouse",
        "view_ingredient",
        "view_productingredient",
        "view_ingredientmovement",
        # Recetas de conversión
        "add_foodrecipe",
        "change_foodrecipe",
        "view_foodrecipe",
    ],
    GROUP_CAJERO: [
        # Mesas y órdenes
        "view_table",
        "add_order",
        "change_order",  # Para marcar como pagado
        "view_order",
        "view_orderitem",
        # Productos (para crear órdenes y reportes)
        "view_product",
        # Ingredientes (solo registrar ingresos)
        "view_ingredient",
        "add_ingredientmovement",
        "view_ingredientmovement",
        # Facturación
        "add_invoice",
        "view_invoice",
        # Arqueo de caja
        "add_cashregister",
        "view_cashregister",
        "change_cashregister",
    ],
}

# ==========================
# 🛠️ FUNCIONES DE UTILIDAD
# ==========================


def get_group_permissions(group_name):
    """Devuelve la lista de permisos (nombres completos) para un grupo."""
    perms = GROUP_PERMISSIONS.get(group_name, [])
    # Añadir prefijo 'orders.' para permisos de la app orders
    # (excepto para permisos de auth)
    full_perms = []
    for perm in perms:
        if perm in USER_GROUP_PERMS:
            full_perms.append(f"auth.{perm}")
        else:
            full_perms.append(f"orders.{perm}")
    return full_perms


def create_groups_with_permissions():
    """Crea los grupos y les asigna los permisos definidos."""
    from django.contrib.auth.models import Group

    for group_name in ALL_GROUPS:
        group, created = Group.objects.get_or_create(name=group_name)
        perms = GROUP_PERMISSIONS.get(group_name, [])
        perm_objects = []
        for perm in perms:
            app_label = "auth" if perm in USER_GROUP_PERMS else "orders"
            try:
                perm_obj = Permission.objects.get(
                    codename=perm, content_type__app_label=app_label
                )
                perm_objects.append(perm_obj)
            except Permission.DoesNotExist:
                pass
        group.permissions.set(perm_objects)
        group.save()


def user_in_group(user, group_name):
    """Verifica si el usuario pertenece a un grupo específico."""
    return user.groups.filter(name=group_name).exists()


def user_has_permission(user, perm_codename, app_label="orders"):
    """Verifica si el usuario tiene un permiso específico."""
    if user.is_superuser:
        return True
    full_perm = f"{app_label}.{perm_codename}"
    return user.has_perm(full_perm)


def get_permission_info(perm_codename):
    """Devuelve la información detallada de un permiso."""
    return PERMISSION_DESCRIPTIONS.get(perm_codename, {
        "name": perm_codename.replace("_", " ").title(),
        "description": "Sin descripción disponible.",
        "use_case": "Consulta con el administrador.",
        "group": "Otro",
        "group_order": 99,
    })


def get_grouped_permissions(perm_codename_list):
    """Devuelve los permisos agrupados por categoría con sus descripciones."""
    groups = {}
    for perm in perm_codename_list:
        info = get_permission_info(perm)
        group = info["group"]
        group_order = info.get("group_order", 99)
        if group not in groups:
            groups[group] = {"order": group_order, "permissions": []}
        groups[group]["permissions"].append({
            "codename": perm,
            "name": info["name"],
            "description": info["description"],
            "use_case": info["use_case"],
        })
    return groups


def get_role_info(group_name):
    """Devuelve la información detallada de un rol."""
    return ROLE_DESCRIPTIONS.get(group_name, {
        "name": group_name,
        "description": "Sin descripción disponible.",
        "color": "secondary",
        "icon": "help"
    })
