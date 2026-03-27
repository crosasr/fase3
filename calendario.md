## Ruta de Aprendizaje Completa — Python + Flet + SQLite para PyMEs

### Fase 1 — Fundamentos Python (15 días)

| Día | Tema | Mini-proyecto |
|-----|------|--------------|
| 1 | Variables, tipos de datos, f-strings | Ficha de producto formateada |
| 2 | Listas y métodos (append, remove, sort) | Catálogo con operaciones básicas |
| 3 | Diccionarios | Catálogo con detalles y valor de inventario |
| 4 | if/elif/else + operadores | Reporte de alertas de inventario |
| 5 | for y while | Recorrer productos con filtros |
| 6 | Mini-proyecto Semana 1 — parte 1 | Script consola: alta y baja de productos |
| 7 | Mini-proyecto Semana 1 — parte 2 | Listado y búsqueda por nombre |
| 8 | Funciones: parámetros y return | `calcular_total()`, `aplicar_descuento()` |
| 9 | Funciones con valores por defecto | `calcular_precio(precio, descuento=0)` |
| 10 | Scope + try/except | Capturar errores de input del usuario |
| 11 | Módulos e import | Separar código en `productos.py` |
| 12 | Refactor — parte 1 | Reescribir script con funciones propias |
| 13 | Refactor — parte 2 | Agregar manejo de errores al script |
| 14 | Archivos .txt y .csv | Guardar y recargar productos desde CSV |
| 15 | JSON + list comprehensions | Convertir CSV a JSON, filtros avanzados |

---

### Fase 2 — Datos persistentes con SQLite (10 días)

| Día | Tema | Mini-proyecto |
|-----|------|--------------|
| 16 | Qué es una base de datos, tablas y columnas | Diseñar estructura de tabla `productos` |
| 17 | CREATE TABLE + INSERT con sqlite3 | Crear BD y agregar productos desde Python |
| 18 | SELECT — consultas básicas | Listar todos los productos de la BD |
| 19 | UPDATE y DELETE | Modificar stock y eliminar productos |
| 20 | Filtros con WHERE | Buscar productos por nombre y categoría |
| 21 | Mini-proyecto parte 1 | Script que guarda productos en SQLite |
| 22 | Mini-proyecto parte 2 | Agregar búsqueda y filtros al script |
| 23 | Consultas con ORDER BY y LIMIT | Ranking de productos por precio y stock |
| 24 | Reporte desde BD | Total de inventario y productos sin stock |
| 25 | Refactor completo Fase 2 | Script consola completo con SQLite |

---

### Fase 3 — Interfaz gráfica con Flet (15 días)

| Día | Tema | Mini-proyecto |
|-----|------|--------------|
| 26 | Introducción a Flet: page, Text, Button | App "Hola PyME" con botón funcional |
| 27 | TextField y captura de input | Formulario de un solo campo |
| 28 | Eventos: qué pasa al hacer clic | Botón que guarda texto en variable |
| 29 | Row y Column — diseño básico | Formulario de producto con campos alineados |
| 30 | Mostrar listas con ListView | Listado de productos en pantalla |
| 31 | Conectar Flet con SQLite — parte 1 | Botón Guardar que inserta en BD |
| 32 | Conectar Flet con SQLite — parte 2 | Lista que carga productos de la BD |
| 33 | Eliminar desde la interfaz | Botón eliminar por producto |
| 34 | Validaciones en formulario | Campos obligatorios y tipos correctos |
| 35 | Mini-proyecto parte 1 | App con formulario + lista de productos |
| 36 | Mini-proyecto parte 2 | Agregar edición de productos |
| 37 | Alertas y diálogos | Confirmar antes de eliminar |
| 38 | Estilo: colores, tamaños, íconos | Darle identidad visual a la app |
| 39 | Refactor parte 1 | Separar UI y lógica en archivos distintos |
| 40 | Refactor parte 2 | App limpia y lista para la Fase 4 |

---

### Fase 4 — App completa para PyME (20 días)

| Día | Tema | Mini-proyecto |
|-----|------|--------------|
| 41 | Navegación entre vistas | App con menú lateral y 3 pantallas |
| 42 | Vista Productos completa | CRUD completo de productos |
| 43 | Vista Clientes — parte 1 | Formulario y listado de clientes |
| 44 | Vista Clientes — parte 2 | Búsqueda y edición de clientes |
| 45 | Relaciones entre tablas (FK) | Tabla ventas relacionada con clientes |
| 46 | Vista Ventas — parte 1 | Seleccionar cliente y productos |
| 47 | Vista Ventas — parte 2 | Calcular total y registrar venta |
| 48 | Control de stock automático | Venta resta stock en tiempo real |
| 49 | Reportes — parte 1 | Ventas del día con totales |
| 50 | Reportes — parte 2 | Productos más vendidos y stock crítico |
| 51 | Filtros y búsqueda global | Buscar en cualquier vista |
| 52 | Manejo de fechas | Filtrar ventas por rango de fechas |
| 53 | Exportar a CSV | Botón para descargar reporte |
| 54 | Mini-proyecto integrador — parte 1 | App con las 3 vistas funcionando |
| 55 | Mini-proyecto integrador — parte 2 | Reportes y exportación integrados |
| 56 | Pruebas y corrección de bugs | Simular uso real de una PyME |
| 57 | Optimización de consultas SQL | Mejorar velocidad en listas grandes |
| 58 | Manejo de errores global | App que nunca se rompe ante el usuario |
| 59 | Refactor final — parte 1 | Código limpio y documentado |
| 60 | Refactor final — parte 2 | App lista para entregar |

---

### Fase 5 — Empaquetado y entrega (5 días)

| Día | Tema | Mini-proyecto |
|-----|------|--------------|
| 61 | flet pack — generar ejecutable | App convertida a .exe en Windows |
| 62 | Prueba en equipo limpio | Verificar que funciona sin Python instalado |
| 63 | Despliegue web con Render | Versión web accesible desde navegador |
| 64 | README y documentación | Manual de usuario básico en GitHub |
| 65 | Entrega final | App presentada a un "cliente simulado" |

---

**Total: 65 días de estudio — aproximadamente 13 semanas a 5 días/semana.** Al terminar tendrás una app funcional, código en GitHub y un proyecto real para mostrar en entrevistas. 🚀
