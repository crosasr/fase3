# 🖥️ Fase 3 — Interfaz gráfica con Flet

Repositorio de aprendizaje activo. Construcción de una app de escritorio real para PyMEs mexicanas usando Python + Flet + SQLite.

---

## 🎯 Objetivo

Conectar la capa de datos construida en Fase 2 (SQLite) con una interfaz gráfica funcional usando Flet, hasta obtener una app de escritorio entregable como `.exe`.

---

## 🗺️ Ruta completa de aprendizaje

| Fase | Contenido | Estado |
|------|-----------|--------|
| [Fase 0](https://github.com/crosasr/fase1) | Setup: Python, UV, Windsurf, Flet | ✅ Completada |
| [Fase 1](https://github.com/crosasr/fase1) | Fundamentos Python | ✅ Completada |
| [Fase 2](https://github.com/crosasr/fase2) | Base de datos con SQLite | ✅ Completada |
| **Fase 3** | **Interfaz gráfica con Flet** | 🔄 En progreso |
| Fase 4 | App completa para PyME | ⬜ Pendiente |
| Fase 5 | Empaquetado .exe y despliegue web | ⬜ Pendiente |

---

## 📁 Contenido de este repositorio

| Archivo | Tema | Conceptos |
|---------|------|-----------|
| `database.py` | Capa de datos reutilizable | `row_factory`, `lastrowid`, `rowcount`, context manager |
| `dia20.py` | Conceptos base de Flet | `Page`, `TextField`, `Button`, `Column`, `Row`, eventos |
| `dia30.py` | ListView y ListTile | Listas con scroll, semáforo de stock, tiles dinámicos |
| `dia31.py` | Flet + SQLite parte 1 | Formulario que inserta en BD real, `lastrowid` en UI |
| `dia32.py` | Flet + SQLite parte 2 | Lista dinámica, búsqueda en tiempo real, reporte |
| `dia33.py` | Eliminar desde interfaz | `BottomSheet` de confirmación, eliminar con feedback |
| `NOTAS_FASE3.md` | Notas de aprendizaje | Conceptos explicados en lenguaje propio |

---

## ⚠️ Notas de API — Flet 0.82.2

Esta fase usa Flet 0.82.x (1.0 Beta). Cambios importantes respecto a versiones anteriores:

| Antes (≤ 0.28) | Ahora (0.82+) |
|----------------|---------------|
| `ft.app(target=main)` | `ft.run(main)` |
| `ft.icons.ADD` | `ft.Icons.ADD` |
| `prefix_text="$"` | `prefix="$"` |
| `ElevatedButton` | `ft.Button` |
| `page.dialog` / `page.open()` | `ft.BottomSheet` + `page.overlay.append()` |

---

## 🛠️ Stack tecnológico

- **Python** 3.14
- **Flet** 0.82.2 — interfaz gráfica de escritorio
- **SQLite** — base de datos local persistente
- **UV** — gestor de entornos virtuales
- **Windsurf** — IDE con asistente IA
- **Git + GitHub** — control de versiones

---

## 🚀 Cómo ejecutar

```bash
# Clonar el repo
git clone git@github.com:crosasr/fase3.git
cd fase3

# Instalar dependencias
uv sync

# Ejecutar cualquier día
uv run flet run dia33.py
```

La base de datos `tienda.db` se crea automáticamente al primer arranque.

---

## 📈 Proyecto objetivo al terminar la ruta

App de escritorio funcional para una PyME con:

- Módulo de productos (CRUD completo)
- Módulo de clientes
- Módulo de ventas con control de stock automático
- Reportes exportables a CSV
- Empaquetada como `.exe` para entregar sin instalar Python

---

## 💡 Filosofía de aprendizaje

- **Práctica desde el día 1** — cada concepto aplicado a casos reales de PyME
- **Windsurf como copiloto, no como piloto** — entender antes de aplicar
- **`database.py` no cambia** — la separación de capas permite reemplazar el frontend sin tocar los datos
- **Commits descriptivos** — el historial cuenta la historia del aprendizaje

---

## 👤 Autor

**César Victorio Rosas Ramos**
Desarrollador en formación especializado en soluciones para PyMEs mexicanas.

Python · Flet · SQLite · BI · Automatización · MAHE

→ [github.com/crosasr](https://github.com/crosasr)
