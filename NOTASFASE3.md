# NOTAS DE APRENDIZAJE — FASE 3
### Flet — Interfaz gráfica para PyMEs
> Escrito en lenguaje propio. Para teoría formal consultar documentación oficial.
> Flet versión: 0.82.2 | API 1.0 Beta

---

## DÍA 26-29 — Conceptos base de Flet

### Qué es Flet
Framework que permite construir apps de escritorio, web y móvil usando solo Python.
No requiere conocer HTML, CSS ni JavaScript.
Usa Flutter por debajo — el mismo motor de Google que usan apps como Google Pay.

```
CLI → input() / print()     ← Fase 2
Flet → TextField / Text     ← Fase 3
```

### Cómo correr una app Flet
```bash
uv run flet run main.py          # ventana de escritorio
uv run flet run main.py --web    # en el navegador
```

**Nota importante:** La terminal queda bloqueada mientras la app está abierta. Es normal.
Los mensajes CRITICAL de XDG portal en Linux son advertencias de GTK — no afectan la app.

### Estructura mínima
```python
import flet as ft

def main(page: ft.Page):
    page.title = "Mi App"
    page.add(ft.Text("Hola"))

ft.run(main)   # ← en Flet 0.80+ ya no es ft.app(target=main)
```

```
ft.run(main)
    └── main(page: ft.Page)
            └── page = la ventana
                    └── page.add(control)
                            └── control = lo que el usuario ve o toca
```

**Regla:** Todo en Flet es un control. Text, TextField, Button, Column, Row — todos son controles.

### Page — la ventana
```python
page.title = "Sistema PyME"
page.window.width  = 900
page.window.height = 600
page.padding = 20
```

### La regla más importante de Flet
```
Modificar un control NO actualiza la pantalla automáticamente.
Siempre necesitas page.update() después de cualquier cambio.
```

```python
def guardar(e):
    resultado.value = "✅ Guardado"
    page.update()   # ← sin esto la pantalla no cambia
```

---

## DÍA 26-29 — Controles básicos

### Text — mostrar información
```python
ft.Text("Inventario")
ft.Text("Título", size=24, weight=ft.FontWeight.BOLD)
ft.Text("Subtítulo", size=13, color=ft.Colors.GREY_500)
ft.Text("Error", color=ft.Colors.RED_700)
```

### TextField — entrada de texto
```python
ft.TextField(label="Nombre del producto", width=350)
ft.TextField(label="Precio", prefix="$", width=160)     # prefix no prefix_text
ft.TextField(label="Stock", suffix="uds", width=120)    # suffix no suffix_text
```

**Regla de API Flet 0.80+:**
```
prefix_text / suffix_text  → prefix / suffix   ← cambio de API en v0.80
```

Para leer el valor:
```python
nombre = campo_nombre.value.strip()   # siempre .strip()
```

### ElevatedButton y OutlinedButton
```python
ft.ElevatedButton("Guardar", icon=ft.Icons.SAVE, on_click=guardar)
ft.OutlinedButton("Cancelar", icon=ft.Icons.CANCEL, on_click=cancelar)
```

### Íconos
```python
ft.Icons.SAVE
ft.Icons.ADD
ft.Icons.DELETE_OUTLINE
ft.Icons.INVENTORY_2
ft.Icons.BAR_CHART
```

**Regla de API Flet 0.80+:**
```
ft.icons.add   → ft.Icons.ADD    ← mayúsculas en v0.80+
```

### SnackBar — notificación temporal
```python
# Flet 0.80+
page.snack_bar = ft.SnackBar(ft.Text("✅ Guardado"))
page.update()

# page.open(ft.SnackBar(...)) también funciona en algunas versiones
# si falla, usar page.snack_bar = ... + page.update()
```

---

## DÍA 26-29 — Layout: Column y Row

### Column — controles en vertical
```python
ft.Column(
    controls=[
        ft.TextField(label="Nombre"),
        ft.TextField(label="Precio"),
        ft.ElevatedButton("Guardar"),
    ],
    spacing=12,                                    # espacio entre controles
    horizontal_alignment=ft.CrossAxisAlignment.START,
    tight=True,                                    # sin espacio extra al final
)
```

### Row — controles en horizontal
```python
ft.Row(
    controls=[
        ft.Text("Sistema PyME"),
        ft.Text("v1.0"),
    ],
    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,  # distribuir espacio
    spacing=8,
)
```

### Alineación en Column y Row
```
MainAxisAlignment    → alineación en la dirección principal
                       (vertical en Column, horizontal en Row)

CrossAxisAlignment   → alineación en la dirección perpendicular
                       (horizontal en Column, vertical en Row)

SPACE_BETWEEN  → espacio igual entre controles
CENTER         → centrado
START          → inicio (izquierda/arriba)
END            → final (derecha/abajo)
```

### expand=True — ocupar espacio disponible
```python
campo = ft.TextField(label="Buscar", expand=True)   # ocupa todo el ancho disponible
lista = ft.ListView(expand=True)                     # ocupa todo el alto disponible
```

**Regla:** Sin `expand=True`, ListView no sabe cuánto espacio tomar y puede no mostrar nada.

### Divider — separador visual
```python
ft.Divider()              # línea horizontal
ft.Divider(height=16)     # con espacio vertical
ft.VerticalDivider()      # línea vertical (dentro de Row)
```

---

## DÍA 26-29 — Eventos

### Estructura de un evento
```python
def guardar(e):            # e = evento, siempre se recibe aunque no se use
    nombre = campo.value.strip()
    if not nombre:
        page.snack_bar = ft.SnackBar(ft.Text("❌ Campo vacío"))
        page.update()
        return             # ← salir si hay error

    # lógica principal
    resultado.value = f"✅ {nombre}"
    campo.value = ""       # limpiar campo
    page.update()          # ← siempre al final

btn = ft.ElevatedButton("Guardar", on_click=guardar)
```

### Lambda para pasar parámetros a eventos
```python
# Cuando necesitas pasar un valor al handler (ej: en un loop)
for producto in productos:
    btn = ft.IconButton(
        icon=ft.Icons.DELETE,
        on_click=lambda e, p=producto: eliminar(e, p)   # p=producto captura el valor
    )
```

**Regla crítica:** Sin `p=producto` en el lambda, todos los botones apuntarían al último
producto del loop — bug clásico en Python con closures.

---

## DÍA 30 — ListView y ListTile

### Column vs ListView
```
Column    → apila controles sin scroll
            si hay más contenido que espacio → se corta

ListView  → scroll automático
            para listas de tamaño variable o desconocido
```

**Regla:** En una app de inventario siempre usar ListView para productos,
no sabes cuántos hay.

### ListView
```python
lista = ft.ListView(
    controls=[ft.Text(p) for p in productos],
    spacing=8,              # espacio entre ítems
    divider_thickness=1,    # línea separadora entre ítems
    expand=True,            # ← obligatorio para que ocupe espacio
)

# Agregar un ítem dinámicamente
lista.controls.append(ft.Text("Nuevo producto"))
page.update()

# Limpiar toda la lista
lista.controls.clear()
page.update()
```

### ListTile — ítem estándar de lista
Estructura visual de un ListTile:
```
┌─────────────────────────────────────────────┐
│ [leading]  title          [trailing]        │
│            subtitle                         │
└─────────────────────────────────────────────┘
```

```python
ft.ListTile(
    leading=ft.Icon(ft.Icons.INVENTORY_2),
    title=ft.Text("Silla", weight=ft.FontWeight.W_500),
    subtitle=ft.Text("Muebles", color=ft.Colors.GREY_600),
    trailing=ft.Text("$1,350.00"),
    on_click=lambda e: print("clic en Silla"),   # opcional
)
```

- `leading` → izquierda — ícono, avatar, imagen
- `title` → texto principal
- `subtitle` → texto secundario (más pequeño y gris)
- `trailing` → derecha — precio, botón, estado

### Patrón: construir tiles desde datos
```python
def construir_tile(producto):
    return ft.ListTile(
        leading=ft.Icon(ft.Icons.CHAIR),
        title=ft.Text(producto["nombre"]),
        subtitle=ft.Text(producto["categoria"]),
        trailing=ft.Text(f"${producto['precio']:,.2f}"),
    )

lista = ft.ListView(
    controls=[construir_tile(p) for p in productos],
    expand=True,
)
```

### Indicadores visuales de stock — patrón semáforo
```python
def color_stock(stock):
    if stock == 0:   return ft.Colors.RED_700      # sin stock
    if stock <= 5:   return ft.Colors.ORANGE_700   # stock crítico
    return ft.Colors.GREEN_700                      # stock OK

def icono_stock(stock):
    if stock == 0:   return ft.Icons.CANCEL         # ❌ sin stock
    if stock <= 5:   return ft.Icons.WARNING        # ⚠️ crítico
    return ft.Icons.CHECK_CIRCLE                    # ✅ OK
```

### Eliminar ítem de lista con referencia al tile
```python
def construir_tile_con_eliminar(producto):
    tile = ft.ListTile(
        title=ft.Text(producto["nombre"]),
    )

    def eliminar(e, t=tile):
        lista.controls.remove(t)
        page.update()

    tile.trailing = ft.IconButton(
        icon=ft.Icons.DELETE_OUTLINE,
        icon_color=ft.Colors.RED_400,
        on_click=eliminar,
    )
    return tile
```

**Regla:** el tile debe existir antes de asignarle el trailing que lo referencia.
Por eso se crea primero y se asigna el trailing después.

---

## Resumen de API — cambios Flet 0.80+

| Antes (≤ 0.28) | Ahora (0.80+) | Notas |
|----------------|---------------|-------|
| `ft.app(target=main)` | `ft.run(main)` | Nuevo punto de entrada |
| `ft.icons.ADD` | `ft.Icons.ADD` | Mayúsculas |
| `prefix_text="$"` | `prefix="$"` | En TextField |
| `suffix_text="uds"` | `suffix="uds"` | En TextField |
| `page.show_snack_bar()` | `page.snack_bar = ... + page.update()` | SnackBar |

---

## Controles usados hasta el Día 30

| Control | Para qué sirve |
|---------|---------------|
| `ft.Text` | Mostrar texto |
| `ft.TextField` | Capturar texto del usuario |
| `ft.ElevatedButton` | Acción principal |
| `ft.OutlinedButton` | Acción secundaria |
| `ft.IconButton` | Botón solo con ícono |
| `ft.Icon` | Ícono decorativo |
| `ft.Column` | Layout vertical sin scroll |
| `ft.Row` | Layout horizontal |
| `ft.ListView` | Lista con scroll |
| `ft.ListTile` | Ítem estándar de lista |
| `ft.Divider` | Separador horizontal |
| `ft.SnackBar` | Notificación temporal |

---

---

## DÍA 31 — Flet + SQLite Parte 1

### El momento clave de la ruta
El Día 31 es cuando Flet y SQLite se conectan por primera vez.
La interfaz deja de ser un ejercicio para convertirse en una app real.

```
FASE 2 (consola)          FASE 3 (interfaz)
─────────────────         ──────────────────────
database.py        →      database.py  (sin cambios ✅)
input()            →      ft.TextField
print()            →      ft.Text / ft.ListTile
while True: menú   →      ft.run(main)
```

### Patrón: cargar lista desde SQLite
```python
def cargar_lista():
    lista.controls.clear()          # limpiar lista actual
    productos = db.obtener_todos()  # consultar BD

    if not productos:
        lista.controls.append(
            ft.ListTile(title=ft.Text("Sin productos aún"))
        )
        return

    for p in productos:
        lista.controls.append(construir_tile(p))
    # NO llamar page.update() aquí — se llama desde quien invoca cargar_lista()
```

### Patrón: guardar y recargar
```python
def guardar(e):
    # 1. Validar
    if not nombre:
        ...
        return

    # 2. Insertar en BD
    nuevo_id = db.agregar_producto(nombre, categoria, precio, stock)

    # 3. Limpiar campos
    campo_nombre.value = ""
    ...

    # 4. Recargar lista desde BD (no agregar manualmente)
    cargar_lista()

    # 5. Feedback + actualizar pantalla
    page.snack_bar = ft.SnackBar(ft.Text(f"✅ Guardado — ID: {nuevo_id}"))
    page.snack_bar.open = True
    page.update()
```

**Regla:** Siempre recargar desde la BD después de un INSERT — no agregar el control
manualmente. Así la lista siempre refleja el estado real de los datos.

### Inicialización al arrancar
```python
db.init_db()      # crear tablas si no existen
cargar_lista()    # cargar datos iniciales
page.update()     # refrescar pantalla
```

---

## DÍA 32 — Flet + SQLite Parte 2

### Búsqueda en tiempo real con on_change
```python
campo_buscar = ft.TextField(
    label="Buscar producto",
    prefix_icon=ft.Icons.SEARCH,
    expand=True,
)

def buscar(e):
    termino = campo_buscar.value.strip()
    if termino:
        cargar_lista(db.buscar_por_nombre(termino))
    else:
        cargar_lista()

campo_buscar.on_change = buscar   # ← se dispara en cada tecla
```

`on_change` vs `on_submit`:
```
on_change  → se dispara en cada tecla (tiempo real)
on_submit  → se dispara al presionar Enter
```

### Contador dinámico
```python
contador = ft.Text("", color=ft.Colors.GREY_600, size=13)

n = len(productos)
contador.value = f"{n} producto{'s' if n != 1 else ''}"
```

### BottomSheet — panel desde abajo
`AlertDialog` y `page.dialog` no funcionan en Flet 0.82 — usar `BottomSheet`:

```python
def mostrar_panel(e):
    def cerrar(e):
        bs.open = False
        page.update()

    bs = ft.BottomSheet(
        content=ft.Container(
            padding=20,
            content=ft.Column(
                controls=[
                    ft.Text("Título", size=18, weight=ft.FontWeight.BOLD),
                    ft.Text("Contenido..."),
                    ft.TextButton("Cerrar", on_click=cerrar),
                ],
                spacing=8,
                tight=True,
            ),
        ),
    )
    page.overlay.append(bs)   # ← agregar al overlay, no a page.add()
    bs.open = True
    page.update()
```

**Tabla de equivalencias de diálogos en Flet 0.82:**
```
AlertDialog + page.dialog  → NO funciona en 0.82
page.open(AlertDialog)     → NO existe en 0.82
BottomSheet                → ✅ funciona con page.overlay.append()
```

---

## DÍA 33 — Eliminar desde la interfaz

### Botón eliminar por ítem — lambda con captura
```python
ft.IconButton(
    icon=ft.Icons.DELETE_OUTLINE,
    icon_color=ft.Colors.RED_400,
    tooltip="Eliminar",
    on_click=lambda e, i=pid, n=nombre: confirmar_eliminar(i, n),
    # i=pid y n=nombre capturan el valor en cada iteración
    # sin esto todos los botones apuntarían al último producto del loop
)
```

### Confirmación antes de eliminar
```python
def confirmar_eliminar(producto_id, nombre):
    def eliminar(e):
        db.eliminar_producto(producto_id)
        bs.open = False
        cargar_lista()
        page.snack_bar = ft.SnackBar(ft.Text(f"🗑️ '{nombre}' eliminado"))
        page.snack_bar.open = True
        page.update()

    def cancelar(e):
        bs.open = False
        page.update()

    bs = ft.BottomSheet(
        content=ft.Container(
            padding=20,
            content=ft.Column(
                controls=[
                    ft.Text("¿Eliminar producto?",
                            size=18, weight=ft.FontWeight.BOLD),
                    ft.Text(f"'{nombre}' será eliminado permanentemente.",
                            color=ft.Colors.GREY_600),
                    ft.Divider(),
                    ft.Row(controls=[
                        ft.TextButton("Cancelar", on_click=cancelar),
                        ft.TextButton(
                            "Eliminar",
                            on_click=eliminar,
                            style=ft.ButtonStyle(color=ft.Colors.RED_700),
                        ),
                    ]),
                ],
                spacing=8,
                tight=True,
            ),
        ),
    )
    page.overlay.append(bs)
    bs.open = True
    page.update()
```

### Flujo completo de eliminación
```
Clic en 🗑️
    → BottomSheet de confirmación
        → "Cancelar" → cierra sin cambios
        → "Eliminar" → db.eliminar_producto() → recargar lista → SnackBar
```

---

## Resumen de API — cambios Flet 0.80+

| Antes (≤ 0.28) | Ahora (0.82+) | Notas |
|----------------|---------------|-------|
| `ft.app(target=main)` | `ft.run(main)` | Nuevo punto de entrada |
| `ft.icons.ADD` | `ft.Icons.ADD` | Mayúsculas |
| `prefix_text="$"` | `prefix="$"` | En TextField |
| `suffix_text="uds"` | `suffix="uds"` | En TextField |
| `ElevatedButton` | `ft.Button` | Deprecado en 0.80 |
| `page.show_snack_bar()` | `page.snack_bar = ... + .open = True` | SnackBar |
| `AlertDialog` / `page.dialog` | `ft.BottomSheet` | No funciona en 0.82 |
| `page.open()` | No existe | Usar overlay |

---

## Controles usados hasta el Día 33

| Control | Para qué sirve |
|---------|---------------|
| `ft.Text` | Mostrar texto |
| `ft.TextField` | Capturar texto del usuario |
| `ft.Button` | Acción principal |
| `ft.TextButton` | Acción secundaria o en diálogos |
| `ft.IconButton` | Botón solo con ícono (eliminar, editar) |
| `ft.Icon` | Ícono decorativo |
| `ft.Column` | Layout vertical sin scroll |
| `ft.Row` | Layout horizontal |
| `ft.ListView` | Lista con scroll |
| `ft.ListTile` | Ítem estándar de lista |
| `ft.Container` | Contenedor con padding/margin/color |
| `ft.Divider` | Separador horizontal |
| `ft.SnackBar` | Notificación temporal |
| `ft.BottomSheet` | Panel desde abajo (confirmaciones, reportes) |

---

---

## DÍA 34 — Validaciones en formulario

### El problema con error_text y SnackBar en Flet 0.82
```
error_text en TextField  → no renderiza visualmente en Flet 0.82
SnackBar de error        → no siempre aparece en Flet 0.82
Solución confiable       → ft.Text() visible en el layout + page.update()
```

### Patrón de validación con texto visible
```python
# Controles de error en el layout — siempre visibles cuando tienen valor
error_nombre = ft.Text("", color=ft.Colors.RED_500, size=12)
error_precio = ft.Text("", color=ft.Colors.RED_500, size=12)

def validar():
    errores = []

    nombre = campo_nombre.value.strip()
    if not nombre:
        errores.append("Nombre obligatorio")

    precio = None
    precio_s = campo_precio.value.strip()
    if not precio_s:
        errores.append("Precio obligatorio")
    else:
        try:
            precio = float(precio_s.replace(",", "."))
            if precio <= 0:
                errores.append("Precio debe ser mayor a 0")
        except ValueError:
            errores.append("Precio inválido")

    # Stock — opcional, default 0
    stock = 0
    stock_s = campo_stock.value.strip()
    if stock_s:
        try:
            stock = int(stock_s)
            if stock < 0:
                errores.append("Stock no puede ser negativo")
        except ValueError:
            errores.append("Stock inválido")

    # Asignar errores a los controles visibles
    if errores:
        error_nombre.value = next((e for e in errores if "Nombre" in e), "")
        error_precio.value = next((e for e in errores if "Precio" in e
                                   or "inválido" in e.lower()), "")

    return errores, precio, stock

def guardar(e):
    errores, precio, stock = validar()
    if errores:
        page.update()   # ← muestra los errores en pantalla
        return
    # continuar con INSERT/UPDATE
```

**Regla:** el stock no es obligatorio — solo se valida si el usuario escribió algo.

---

## DÍA 35-36 — Mini-proyecto CRUD completo

### Modo INSERT vs modo UPDATE — mismo botón
```python
# Estado de edición — variables que controlan el modo
producto_editando = None
modo_edicion      = False

def guardar(e):
    errores, precio, stock = validar()
    if errores:
        page.update()
        return

    nombre    = campo_nombre.value.strip()
    categoria = campo_categoria.value or "Otros"

    if modo_edicion:
        # UPDATE
        db.actualizar_producto(producto_editando["id"],
                               nombre, categoria, precio, stock)
        resetear_edicion()
    else:
        # INSERT
        nuevo_id = db.agregar_producto(nombre, categoria, precio, stock)

    cargar_lista()
    page.update()
```

### Cargar datos en formulario para editar
```python
def editar_producto(producto_id, _):
    nonlocal producto_editando, modo_edicion
    producto = db.obtener_por_id(producto_id)
    if producto:
        producto_editando     = producto
        modo_edicion          = True
        campo_nombre.value    = producto["nombre"]
        campo_categoria.value = producto["categoria"]
        campo_precio.value    = str(producto["precio"])
        campo_stock.value     = str(producto["stock"])
        texto_edicion.value   = f"✏️ Editando: {producto['nombre']}"
        page.update()
```

### nonlocal — modificar variables del scope externo
```python
# Sin nonlocal → Python crea una variable local nueva (bug silencioso)
# Con nonlocal → modifica la variable del scope de main()

def resetear_edicion():
    nonlocal producto_editando, modo_edicion   # ← obligatorio
    producto_editando = None
    modo_edicion      = False
```

### Dropdown — categorías predefinidas
```python
ft.Dropdown(
    label="Categoría",
    width=200,
    options=[
        ft.dropdown.Option("Alimentos"),
        ft.dropdown.Option("Bebidas"),
        ft.dropdown.Option("Otros"),
    ],
)

# Leer valor
categoria = campo_categoria.value or "Otros"   # default si no seleccionó

# Limpiar dropdown
campo_categoria.value = None   # None limpia la selección
```

---

## DÍA 37 — Alertas y diálogos

### Banner — alerta persistente en la parte superior
```python
banner = ft.Banner(
    bgcolor=ft.Colors.ORANGE_50,
    leading=ft.Icon(ft.Icons.WARNING_AMBER_ROUNDED,
                    color=ft.Colors.ORANGE_700),
    content=ft.Text("", color=ft.Colors.ORANGE_900),
    actions=[
        ft.TextButton("Cerrar", on_click=lambda e: cerrar_banner()),
    ],
)

def actualizar_banner():
    criticos = db.stock_critico()
    if criticos:
        banner.content.value = f"⚠️ {len(criticos)} productos con stock crítico"
        page.banner = banner
        banner.open = True
    else:
        banner.open = False
    page.update()

# Llamar después de cada INSERT, UPDATE o DELETE
cargar_lista()
actualizar_banner()
```

### Deshacer eliminación — segundo BottomSheet
`SnackBar action/on_action` no funciona en Flet 0.82. Patrón alternativo:

```python
def confirmar_eliminar(producto_id, nombre):
    def eliminar(e):
        # 1. Guardar copia ANTES de eliminar
        ultimo_eliminado = dict(db.obtener_por_id(producto_id))
        db.eliminar_producto(producto_id)
        bs.open = False
        cargar_lista()

        # 2. Abrir segundo BottomSheet con opción Deshacer
        def deshacer(e):
            db.agregar_producto(
                ultimo_eliminado["nombre"],
                ultimo_eliminado["categoria"],
                ultimo_eliminado["precio"],
                ultimo_eliminado["stock"],
            )
            bs2.open = False
            cargar_lista()
            page.update()

        def ignorar(e):
            bs2.open = False
            page.update()

        bs2 = ft.BottomSheet(...)   # con botones Ignorar y Deshacer
        page.overlay.append(bs2)
        bs2.open = True
        page.update()
```

**Tabla de alertas en Flet 0.82:**
```
Banner               → ✅ page.banner = banner + banner.open = True
SnackBar action      → ❌ no funciona en 0.82
AlertDialog          → ❌ no funciona en 0.82
BottomSheet          → ✅ page.overlay.append() — patrón universal
```

---

## DÍA 38 — Estilo e identidad visual

### Tema global con Material 3
```python
page.theme = ft.Theme(
    color_scheme_seed=ft.Colors.BLUE_GREY,
    use_material3=True,
)
page.bgcolor = ft.Colors.GREY_100
```

### Container como wrapper estilizado
```python
ft.Container(
    content=ft.ListTile(...),
    bgcolor=ft.Colors.WHITE,
    border_radius=8,
    margin=ft.margin.symmetric(vertical=2),   # espacio entre ítems
    padding=ft.padding.symmetric(horizontal=8),
)
```

### NavigationRail — barra lateral de navegación
```python
rail = ft.NavigationRail(
    selected_index=0,
    label_type=ft.NavigationRailLabelType.ALL,
    min_width=80,
    bgcolor=ft.Colors.WHITE,
    destinations=[
        ft.NavigationRailDestination(
            icon=ft.Icons.INVENTORY_2_OUTLINED,
            selected_icon=ft.Icons.INVENTORY_2,
            label="Inventario",
        ),
        ft.NavigationRailDestination(
            icon=ft.Icons.BAR_CHART_OUTLINED,
            selected_icon=ft.Icons.BAR_CHART,
            label="Reporte",
        ),
    ],
    on_change=cambiar_vista,
)

def cambiar_vista(e):
    idx = e.control.selected_index
    if idx == 0:
        contenido.content = vista_inventario()
    elif idx == 1:
        contenido.content = vista_reporte()
    page.update()
```

### Layout con NavigationRail
```python
page.add(
    ft.Row(
        controls=[
            rail,
            ft.VerticalDivider(width=1, color=ft.Colors.GREY_200),
            contenido,   # ft.Container(expand=True)
        ],
        expand=True,
        spacing=0,
    )
)
```

**Regla:** `expand=True` en el Row y en el contenido — sin esto el layout no ocupa toda la ventana.

---

## DÍA 39-40 — Refactor: arquitectura modular

### Por qué refactorizar
Un archivo de 400+ líneas con UI, lógica y datos mezclados es difícil de mantener.
La separación de capas permite cambiar una parte sin romper las demás.

### Arquitectura final Fase 3
```
main.py              ← punto de entrada — solo ft.run(main)
app.py               ← orquestador — NavigationRail + estado global
database.py          ← capa de datos — sin cambios desde Fase 2
ui/
├── __init__.py      ← vacío — marca la carpeta como módulo Python
├── componentes.py   ← controles reutilizables — tiles, tarjetas
├── formulario.py    ← campos + función validar()
└── vistas.py        ← vistas completas — inventario, reporte
```

### __init__.py — marcar carpeta como módulo
```python
# ui/__init__.py — archivo vacío
# Sin este archivo Python no reconoce la carpeta como módulo importable
```

### Imports entre módulos
```python
# En app.py
from ui.vistas import crear_vista_inventario, crear_vista_reporte

# En ui/vistas.py
import database as db
from ui.componentes import construir_tile, construir_tarjeta
from ui.formulario  import crear_campos, limpiar_campos, validar
```

### Funciones que retornan controles
```python
# Patrón: función que construye y retorna un control Flet
def construir_tile(p, on_editar, on_eliminar) -> ft.Container:
    ...
    return ft.Container(...)

# Patrón: función que retorna vista + función de recarga
def crear_vista_inventario(page):
    ...
    def cargar_lista():
        ...
    vista = ft.Column(...)
    return vista, cargar_lista   # ← retorna dos cosas

# Consumo en app.py
vista_inv, cargar_lista = crear_vista_inventario(page)
```

### Callbacks como parámetros
```python
# construir_tile recibe las funciones de editar y eliminar como parámetros
# → el componente no sabe nada de la lógica, solo llama lo que recibe

def construir_tile(p, on_editar, on_eliminar):
    return ft.Container(
        content=ft.ListTile(
            trailing=ft.Row(controls=[
                ft.IconButton(
                    on_click=lambda e, i=p["id"]: on_editar(i, p["nombre"]),
                ),
                ft.IconButton(
                    on_click=lambda e, i=p["id"]: on_eliminar(i, p["nombre"]),
                ),
            ]),
        ),
    )
```

### Cambios de API — Flet 0.83
```
ft.border.all()       → Border.all()      (importar Border desde flet)
ft.margin.symmetric() → Margin.symmetric() (importar Margin desde flet)
```

---

## Resumen final de API — Flet 0.80-0.83

| Patrón | Código correcto en 0.82-0.83 |
|--------|------------------------------|
| Punto de entrada | `ft.run(main)` |
| Íconos | `ft.Icons.SAVE` |
| Colores | `ft.Colors.BLUE_GREY_700` |
| Botón principal | `ft.Button(...)` o `ft.TextButton(...)` |
| Prefix en TextField | `prefix="$"` |
| Diálogo | `ft.BottomSheet + page.overlay.append()` |
| Banner | `page.banner = banner + banner.open = True` |
| SnackBar | `page.snack_bar = ft.SnackBar(...) + .open = True` |
| Error en campo | `ft.Text()` visible en layout |
| Border | `Border.all()` (importar Border) |
| Margin | `Margin.symmetric()` (importar Margin) |
| NavigationRail | `ft.NavigationRail + ft.NavigationRailDestination` |
| Layout principal | `ft.Row([rail, ft.VerticalDivider(), contenido], expand=True)` |

---

## Controles usados — Fase 3 completa

| Control | Para qué sirve |
|---------|---------------|
| `ft.Text` | Mostrar texto |
| `ft.TextField` | Capturar texto |
| `ft.Dropdown` | Lista de opciones predefinidas |
| `ft.Button` / `ft.TextButton` | Acciones |
| `ft.IconButton` | Botón con ícono |
| `ft.Icon` | Ícono decorativo |
| `ft.Column` | Layout vertical |
| `ft.Row` | Layout horizontal |
| `ft.ListView` | Lista con scroll |
| `ft.ListTile` | Ítem estándar |
| `ft.Container` | Wrapper con estilo |
| `ft.Divider` / `ft.VerticalDivider` | Separadores |
| `ft.SnackBar` | Notificación temporal |
| `ft.BottomSheet` | Panel desde abajo |
| `ft.Banner` | Alerta persistente superior |
| `ft.NavigationRail` | Barra lateral de navegación |

---

*Fase 3 completada — días 26 al 40. Siguiente: Fase 4 — App completa para PyME.*
