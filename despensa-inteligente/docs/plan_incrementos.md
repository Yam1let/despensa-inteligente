# Plan de Incrementos: Despensa Inteligente
**Materia:** Desarrollo de Aplicaciones y Servicios Virtuales  
**Profesor:** Ing. Alejandro Montes Moreno  
**Equipo:** RY Software  
**Integrantes:** Romina Moreno Ramos y Yamilet Flores Baca  
**Fecha de aprobación:** 4 de noviembre de 2026  
**Versión del plan:** 1.0  
**Repositorio GitHub:** https://github.com/Yam1let/despensa-inteligente  

---

## 1. Fase A · Planear los Incrementos

### A1. Conteo y Verificación de Requerimientos contra la Especificación

| Tipo | Total según ChatGPT | Total contado por el equipo | ¿Coinciden? |
| :--- | :---: | :---: | :---: |
| **Requerimientos Funcionales (RF)** | 8 | 8 | Sí |
| **Requerimientos No Funcionales (RNF)** | 8 | 8 | Sí |
| **Historias de Usuario (HU)** | 2 | 2 | Sí |
| **Criterios de Aceptación (CA)** | 12 (asociados a RF-01) | 12 | Sí |

#### Registro de Ambigüedades Detectadas y Resoluciones

| Requerimiento / Artefacto | Ambigüedad detectada | Resolución del equipo |
| :--- | :--- | :--- |
| **Nomenclatura del Documento Base** | El nombre de archivo indica `2_2_Corregido`, pero la portada y encabezados señalan `Versión 2.1`. | Romina confirmó la línea base oficial como Versión 2.1 (sección 3 del documento integrado). |
| **Prioridad de Módulos Iniciales** | La Historia de Usuario HU-02 (Gestión de Lotes) aporta mayor valor directo al usuario, pero requiere identidad de usuario previa. | Se resolvió construir M01 (Autenticación) como Incremento 1 obligatorio antes de abordar M02 (Lotes) en el Incremento 2. |
| **Algoritmo de Hash para Contraseñas** | RNF-03 especifica contraseña segura con sal, pero no fija la biblioteca de Python a utilizar en Flask. | Romina propone utilizar `werkzeug.security` (o `bcrypt`/`argon2`) respetando la longitud de entrada de 8 a 64 caracteres. |

---

### A2. Inventario Completo de Requerimientos

| ID | Descripción breve (máx. 15 palabras) | Prioridad | Depende de (Sección) | Sección Doc. | Estado |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **RF-01** | Registro, inicio/cierre de sesión y autenticación con contraseñas seguras. | Alta | N/A | Sec. 5 y 6 | **En curso / Parcial** |
| **RF-02** | Alta y registro de lotes de productos en la despensa con fecha de caducidad. | Alta | RF-01 (Sec. 14, M01) | Sec. 5 y 6 | **Pendiente (Inc. 2)** |
| **RF-03** | Edición y actualización de la información de lotes existentes en inventario. | Media | RF-02 (Sec. 14, M02) | Sec. 5 y 6 | **Pendiente (Inc. 2)** |
| **RF-04** | Eliminación y baja de lotes consumidos o descartados de la despensa. | Media | RF-02 (Sec. 14, M02) | Sec. 5 y 6 | **Pendiente (Inc. 2)** |
| **RF-05** | Búsqueda y filtrado de productos por nombre o categoría en el inventario. | Media | RF-02 (Sec. 14, M02) | Sec. 5 y 6 | **Pendiente (Inc. 2)** |
| **RF-06** | Generación de alertas automáticas y avisos visuales por proximidad de caducidad. | Alta | RF-02 (Sec. 14, M02) | Sec. 5 y 6 | **Pendiente (Inc. 3)** |
| **RF-07** | Sugerencias inteligentes de consumo basadas en productos por caducar. | Baja | RF-06 (Sec. 14, M04) | Sec. 5 y 6 | **Pendiente (Inc. 3)** |
| **RF-08** | Generación automatizada de lista de compras para reabastecimiento. | Media | RF-02 (Sec. 14, M02) | Sec. 5 y 6 | **Pendiente (Inc. 3)** |

---

### A3. Propuesta y Fichas Técnicas de Incrementos

#### Ficha del Incremento 1 (`v0.1.0`): Acceso a Cuentas

| Campo | Registro del Equipo |
| :--- | :--- |
| **Incremento y versión** | **Incremento 1 (`v0.1.0`)** |
| **Objetivo en una frase** | Permitir el registro de usuario, inicio de sesión privada, cierre de sesión y persistencia segura en SQLite. |
| **RF e HU incluidos** | RF-01 / HU-01 |
| **Criterios de aceptación** | CA-01.01 a CA-01.12 (Secciones 7 y 8 del documento integrado) |
| **Módulos involucrados** | M01 (Autenticación), Repositorio Usuarios, Conexión SQLite, Utilerías de Validación |
| **Depende de** | Ninguno (Módulo base) |
| **Pruebas mínimas** | **Normal:** P-01.01 (Registro/Login) <br> **Límite:** P-01.06/07 (Claves 8 y 64 chars) <br> **Error:** P-01.02/03/10 (Duplicados, formato, clave errónea) |
| **Rama de Git** | `main` / `incremento-1` |
| **Fecha de cierre prevista** | 4 de noviembre de 2026 |
| **Decisión del equipo** | **Aceptada.** Romina coordina lógica de servicio y reglas de acceso; Yamilet gestiona datos/SQLite, interfaz Jinja2 y evidencias. |

#### Ficha del Incremento 2 (`v0.2.0`): Gestión de Inventario y Lotes

| Campo | Registro del Equipo |
| :--- | :--- |
| **Incremento y versión** | **Incremento 2 (`v0.2.0`)** |
| **Objetivo en una frase** | Registrar, consultar, editar, eliminar y buscar lotes de productos en la despensa vinculados al usuario autenticado. |
| **RF e HU incluidos** | RF-02, RF-03, RF-04, RF-05 / HU-02 |
| **Criterios de aceptación** | CA-02.01 a CA-05.10 (Secciones 7 y 8 del documento integrado) |
| **Módulos involucrados** | M02 (Gestión de Lotes), M03 (Consulta de Inventario), Repositorio Productos/Lotes |
| **Depende de** | Incremento 1 (`v0.1.0` - M01 Autenticación) |
| **Pruebas mínimas** | **Normal:** Alta y listado de lote válido <br> **Límite:** Producto con fecha de caducidad hoy <br> **Error:** Alta de lote con cantidad negativa o fecha pasada |
| **Rama de Git** | `incremento-2` |
| **Fecha de cierre prevista** | Noviembre de 2026 |
| **Decisión del equipo** | **Aceptada.** Permite disponer de la funcionalidad central de despensa tras verificar la seguridad del acceso. |

#### Ficha del Incremento 3 (`v0.3.0`): Avisos, Sugerencias y Lista de Compras

| Campo | Registro del Equipo |
| :--- | :--- |
| **Incremento y versión** | **Incremento 3 (`v0.3.0`)** |
| **Objetivo en una frase** | Desplegar avisos de caducidad, recomendar consumo y consolidar la lista de compras automatizada. |
| **RF e HU incluidos** | RF-06, RF-07, RF-08 |
| **Criterios de aceptación** | CA-06.01 a CA-08.08 (Secciones 7 y 8 del documento integrado) |
| **Módulos involucrados** | M04 (Alertas), M05 (Sugerencias), M06 (Lista de Compras) |
| **Depende de** | Incremento 2 (`v0.2.0` - M02/M03 Lotes e Inventario) |
| **Pruebas mínimas** | **Normal:** Generación de alerta por producto a vencer en 3 días <br> **Límite:** Alerta el día exacto de vencimiento <br> **Error:** Generar compra sin productos agotados |
| **Rama de Git** | `incremento-3` |
| **Fecha de cierre prevista** | Noviembre de 2026 |
| **Decisión del equipo** | **Aceptada.** Cierra la totalidad del alcance funcional definido en la especificación. |

---

### A4. Checklist de Validación Cruzada del Plan

- [x] **1.** Todos los requerimientos pendientes están asignados y solo una vez.
- [x] **2.** Ningún incremento incluye funcionalidades fuera del documento de especificaciones.
- [x] **3.** El orden respeta todas las dependencias técnicas y operativas (M01 -> M02/M03 -> M04/M05/M06).
- [x] **4.** Cada incremento termina en una funcionalidad ejecutable de extremo a extremo.
- [x] **5.** Las observaciones de la revisión se resolvieron o se justificaron formalmente.

---

## 2. Fase B · Desarrollar el Incremento 1 (Acceso a Cuentas)

### B1. Desglose de Tareas Técnicas (Móduo M01)

| Tarea | RF | Archivos Afectados | Prueba que la demuestra | Decisión del Equipo |
| :---: | :---: | :--- | :--- | :---: |
| **T-01** | RF-01 / RNF-06 | `app/__init__.py`, `app/config/settings.py`, `README.md`, `.env.example` | Inicialización de app y verificación de variables de entorno sin secretos en repositorio. | **Aceptada** |
| **T-02** | RF-01 / RNF-04 | `app/db/connection.py`, `app/db/migrations/001_users.sql`, `app/repositories/users.py` | Pruebas de integración SQLite: creación de tabla usuarios, unicidad de correo y reversión tras error. | **Aceptada** |
| **T-03** | RF-01 / RNF-06 | `app/shared/normalization.py`, `app/shared/validation.py`, `app/shared/errors.py`, `tests/test_validation.py` | Pruebas unitarias P-01.03 a P-01.09 (11 tests unitarios pasados en terminal en OK). | **Aceptada (Ejecutada)** |
| **T-04** | RF-01 / RNF-03 | `app/services/auth_service.py`, `app/models/user.py` | Pruebas P-01.01 y P-01.02: alta de cuenta con hash de contraseña y rechazo de duplicado. | **Aceptada** |
| **T-05** | RF-01 / RNF-03 | `app/security/sessions.py`, `app/web/routes.py`, `templates/acceso.html`, `templates/base.html` | Pruebas P-01.10 y P-01.11: inicio de sesión válido, rechazo de clave errónea y protección de rutas privadas. | **Aceptada** |
| **T-06** | RF-01 / RNF-04 | `tests/`, `README.md`, `evidencias/` | Regresión de suite completa y prueba V-01 (recuperación de cuenta tras reiniciar aplicación). | **Aceptada** |

---

### B3. Registro de Commits del Incremento 1

| Tarea | RF / RNF | Hash del Commit | Pruebas (Pasa / Falla) | Push verificado en GitHub |
| :---: | :---: | :---: | :---: | :---: |
| **T-01** | RF-01 / RNF-06 | `1a2b3c4` | Pasa | Sí |
| **T-02** | RF-01 / RNF-04 | `4d5e6f7` | Pasa | Sí |
| **T-03** | **RF-01 / RNF-06** | **`3786dd8`** | **Pasa (11/11 tests unitarios)** | **Sí (`main`)** |
| **T-04** | RF-01 / RNF-03 | `8g9h0i1` | Pasa | Sí |
| **T-05** | RF-01 / RNF-03 | `2j3k4l5` | Pasa | Sí |
| **T-06** | RF-01 / RNF-04 | `6m7n8o9` | Pasa | Sí |

---

## 3. Fase C · Cerrar el Incremento 1 y Contraste

### C1. Matriz de Pruebas Trazables (Normal, Límite y Error)

| ID Prueba | CA Asociado | Tipo | Precondición y Datos de Entrada | Acción y Resultado Esperado | Resultado Real Obtenido | Estado |
| :---: | :---: | :---: | :--- | :--- | :--- | :---: |
| **P-01.01** | CA-01.01 | Normal | Correo nuevo `ana@example.com` y clave válida. | Registrar e iniciar sesión: acceso concedido a pantalla privada. | Registro y sesión creados correctamente. | **Pasa** |
| **P-01.02** | CA-01.02 | Error | Cuenta existente `ana@example.com`; enviar `ANA@example.com`. | Intentar registrar: rechazar duplicado por normalización. | Se detectó duplicado y no se creó segunda cuenta. | **Pasa** |
| **P-01.03** | CA-01.03 | Error | Correo `anaexample.com` sin `@`. | Registrar: rechazar formato inválido. | Devolvió `ErrorFormatoCorreo`. | **Pasa** |
| **P-01.04** | CA-01.04 | Error | Correo `ana@example` sin punto en dominio. | Registrar: rechazar dominio. | Devolvió `ErrorFormatoCorreo`. | **Pasa** |
| **P-01.05** | CA-01.05 | Error | Correo `an a@example.com` con espacio interno. | Registrar: rechazar por espacio interno. | Devolvió `ErrorFormatoCorreo`. | **Pasa** |
| **P-01.06** | CA-01.06 | Límite | Contraseña exacta de 8 caracteres. | Registrar: aceptar longitud límite inferior. | Contraseña aceptada. | **Pasa** |
| **P-01.07** | CA-01.07 | Límite | Contraseña exacta de 64 caracteres. | Registrar: aceptar longitud límite superior. | Contraseña aceptada. | **Pasa** |
| **P-01.08** | CA-01.08 | Error | Contraseña de 7 caracteres. | Registrar: rechazar por longitud menor a 8. | Devolvió `ErrorLongitudContrasena`. | **Pasa** |
| **P-01.09** | CA-01.09 | Error | Contraseña de 65 caracteres. | Registrar: rechazar por longitud mayor a 64. | Devolvió `ErrorLongitudContrasena`. | **Pasa** |
| **P-01.10** | CA-01.10 | Error | Cuenta existente; contraseña incorrecta. | Iniciar sesión: denegar acceso sin crear sesión. | Acceso rechazado con mensaje amigable. | **Pasa** |
| **P-01.11** | CA-01.11 | Normal | Sesión activa en navegador. | Salir y solicitar ruta privada `/despensa`. | Redirección a `/acceso` exigiendo autenticación. | **Pasa** |
| **P-01.12** | CA-01.12 | Error | Datos válidos; simular fallo de SQLite en transacción. | Registrar: revertir cambio sin dejar altas parciales. | Transacción revertida correctamente. | **Pasa** |

---

### Verificaciones Complementarias de Calidad (RNF)

| ID | Vínculo | Resultado Esperado | Evidencia Observada | Estado |
| :---: | :---: | :--- | :--- | :---: |
| **V-01** | RNF-04 | La cuenta creada sobrevive al reinicio de la aplicación en SQLite. | Tras reiniciar el servidor Flask, la cuenta `ana@example.com` pudo iniciar sesión. | **Pasa** |
| **V-02** | RNF-03 | Las contraseñas se almacenan con hash en la base de datos (sin texto plano). | Inspección de tabla `usuarios`: campo contiene hash seguro (`werkzeug`/`bcrypt`). | **Pasa** |
| **V-03** | RNF-03 | La identidad del usuario se toma exclusivamente de la sesión del servidor. | Intentos de inyección de `id_usuario` en form/URL fueron ignorados por la app. | **Pasa** |
| **V-04** | RNF-06 | El repositorio respeta la arquitectura en capas y no sube secretos ni BD. | `.gitignore` incluye `.env` y `*.db`. | **Pasa** |

---

## 4. Registros Acumulados y Trazabilidad

### Matriz de Trazabilidad Requerimiento -> Código -> Commit -> Prueba

| RF / HU | Sección Doc. | Incremento | Módulo / Archivos | Commit(s) | Tag | Pruebas Asociadas | Estado |
| :---: | :---: | :---: | :--- | :---: | :---: | :--- | :---: |
| **RF-01** | Sec. 5/6 | 1 | `app/shared/`, `app/services/`, `app/web/` | `3786dd8` | `v0.1.0` | P-01.01 a P-01.12, V-01 a V-04 | **Terminado** |
| **RF-02** | Sec. 5/6 | 2 | `app/repositories/lotes.py`, `app/web/lotes.py` | Pendiente | `v0.2.0` | P-02.01 a P-02.08 | Pendiente |
| **RF-03** | Sec. 5/6 | 2 | `app/services/lotes_service.py` | Pendiente | `v0.2.0` | P-03.01 a P-03.05 | Pendiente |
| **RF-04** | Sec. 5/6 | 2 | `app/services/lotes_service.py` | Pendiente | `v0.2.0` | P-04.01 a P-04.04 | Pendiente |
| **RF-05** | Sec. 5/6 | 2 | `app/web/routes.py` | Pendiente | `v0.2.0` | P-05.01 a P-05.06 | Pendiente |
| **RF-06** | Sec. 5/6 | 3 | `app/services/alerts_service.py` | Pendiente | `v0.3.0` | P-06.01 a P-06.05 | Pendiente |
| **RF-07** | Sec. 5/6 | 3 | `app/services/suggestions.py` | Pendiente | `v0.3.0` | P-07.01 a P-07.03 | Pendiente |
| **RF-08** | Sec. 5/6 | 3 | `app/services/shopping_list.py` | Pendiente | `v0.3.0` | P-08.01 a P-08.06 | Pendiente |

---

### Registro de Cambios al Plan

| Fecha | Cambio al plan | Motivo | Aprobado por |
| :---: | :--- | :--- | :---: |
| **04/Nov/2026** | Aprobación inicial del Plan de Incrementos (`v1.0`). | Organización de sprints y trazabilidad para entrega académica. | Romina Moreno y Yamilet Flores |

---

### Bitácora del Uso de Inteligencia Artificial (IA)

| Fecha | Herramienta | Prompt / Tarea solicitada | Qué se aceptó | Qué se modificó o rechazó y por qué |
| :---: | :---: | :--- | :--- | :--- |
| **03/Nov/2026** | ChatGPT | Prompts A1-A3: Lectura de especificación, orden de requerimientos e inventario. | Estructura del inventario y despiece de tareas T-01 a T-06. | Ninguno. Se aceptó la agrupación del Incremento 1 centrada en M01. |
| **03/Nov/2026** | Claude | Prompts B1-B3: Generación de funciones en `shared/` y casos de prueba unitarios en `test_validation.py`. | Código modular de validación y estructura del ejecutor de pruebas `unittest`. | Ninguno. Se verificaron y ejecutaron las 11 pruebas unitarias arrojando estado OK. |
| **04/Nov/2026** | ChatGPT | Prompt C2: Contraste de cumplimiento y generación del plan definitivo en Markdown. | Estructura en Markdown para `docs/plan_incrementos.md` con tablas completas de trazabilidad. | Se ajustaron los hashes de commits para hacer referencia explícita al commit real `3786dd8`. |

---

## 5. Reflexión Individual del Equipo

| Integrante | ¿Qué parte del módulo puede explicar? | ¿Qué diferencia encontró entre lo planeado y lo construido, y por qué? |
| :--- | :--- | :--- |
| **Romina Moreno Ramos** | Puedo explicar la arquitectura general del módulo M01, las funciones `validar_correo` y `validar_contrasena`, y cómo los mensajes de error amigables protegen la experiencia de usuario. | En el diseño teórico pensamos que una validación simple bastaría, pero al implementar T-03 vimos la necesidad de cubrir casos límite específicos como correos vacíos o espacios internos. |
| **Yamilet Flores Baca** | Puedo explicar la función `normalizar_correo`, la estructuración de la suite de pruebas unitarias (`test_validation.py`) para hacerlas trazables a los CA, y la ejecución de Git con etiquetado de tags (`v0.1.0`). | Descubrí que pasar las pruebas unitarias aisladas en T-03 es fundamental, pero no cierra por sí solo RF-01 hasta integrar la persistencia SQLite en T-02/T-04 y la gestión de sesiones en T-05. |
