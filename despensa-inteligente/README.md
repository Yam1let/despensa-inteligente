# Despensa Inteligente — RY Software

Aplicación web en Flask para organizar la despensa: inventario por lotes, caducidades, alertas y lista de compras.

## Cómo correrla en VS Code

1. Abre la carpeta del proyecto en VS Code e instala la extensión **Python** si te la sugiere.
2. En la terminal de VS Code instala las dependencias (solo la primera vez):

   ```
   pip install -r requirements.txt
   ```

3. Presiona **F5** (o abre `app.py` y pulsa ▶). El navegador se abre solo en http://127.0.0.1:5000.
4. Crea una cuenta en **Registro**, inicia sesión y se abre la interfaz de la despensa.

Para detener el servidor pulsa el cuadro rojo de VS Code o `Ctrl + C` en la terminal.

## Estructura

| Ruta | Qué es |
| :--- | :--- |
| `app.py` | Servidor Flask: registro, inicio/cierre de sesión (SQLite + hash) y rutas de la app |
| `static/despensa.html` | Interfaz principal (Resumen, Inventario con lotes, Lista de compras, alertas) |
| `app/shared/` | Validación y normalización de acceso (T-03) |
| `tests/` | Pruebas unitarias: `python -m unittest -v` |
| `docs/plan_incrementos.md` | Plan de incrementos |
| `.vscode/` | Configuración para correr con F5 y ejecutar pruebas |

La base de datos `despensa.db` se crea sola al arrancar y no se sube a GitHub.

## Nota sobre los datos

Las cuentas se guardan en SQLite. Los productos, lotes y la lista de compras de la interfaz se guardan en el navegador (`localStorage`), separados por usuario. Si se borran los datos del navegador, se pierden.
