
# Despensa Inteligente

## Descripción

Despensa Inteligente es una aplicación web diseñada para optimizar la organización y administración de productos alimenticios en el hogar, facilitando el control de inventarios, el seguimiento de fechas de caducidad y la planificación de compras.

El proyecto busca contribuir a la reducción del desperdicio de alimentos mediante herramientas digitales de organización y gestión.

## Funcionalidades

- Registro e inicio de sesión de usuarios.
- Gestión de inventario de productos.
- Administración de productos por lotes.
- Seguimiento de fechas de caducidad.
- Alertas de vencimiento.
- Lista de compras.
- Almacenamiento de información por usuario.
- Validación y normalización de datos.

## Tecnologías utilizadas

| Tecnología | Aplicación |
|---|---|
| Python | Lógica del servidor |
| Flask | Framework de desarrollo web |
| SQLite | Almacenamiento de cuentas |
| HTML5 | Estructura de la interfaz |
| CSS3 | Diseño visual |
| JavaScript | Interactividad |
| LocalStorage | Almacenamiento local del inventario |
| Unittest | Pruebas unitarias |
| Git y GitHub | Control de versiones |

## Instalación y ejecución

### 1. Clonar el repositorio

```bash
git clone https://github.com/Yam1let/despensa-inteligente.git
cd despensa-inteligente
```

### 2. Instalar las dependencias

```bash
python -m pip install -r requirements.txt
```

### 3. Ejecutar la aplicación

```bash
python app.py
```

### 4. Acceder desde el navegador

http://127.0.0.1:5000

## Estructura del proyecto

```text
despensa-inteligente/
├── .vscode/
├── app/
│   └── shared/
│       ├── errors.py
│       ├── normalization.py
│       └── validation.py
├── docs/
├── evidencias/
├── static/
│   └── despensa.html
├── tests/
├── .gitignore
├── app.py
├── README.md
└── requirements.txt
```

## Pruebas unitarias

Para ejecutar las pruebas de validación:

```bash
python -m unittest discover -s tests -v
```

## Almacenamiento de datos

Las cuentas de usuario se almacenan en SQLite. Los productos, lotes y listas de compras se almacenan mediante LocalStorage en el navegador, de forma independiente para cada usuario.

La base de datos se genera automáticamente al iniciar la aplicación y no se incluye en el repositorio.

## Información académica

- **Universidad:** Universidad Iberoamericana León.
- **Asignatura:** Desarrollo de Aplicaciones y Servicios Virtuales.
- **Profesor:** Ing. Alejandro Montes Moreno.
- **Cliente académico:** Hogar Organizado.

## Desarrolladoras

- Yamilet Flores Baca
- Romina Moreno Ramos



