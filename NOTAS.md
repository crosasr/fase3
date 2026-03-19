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

*Actualizar con días 31-40 al completarlos.*
