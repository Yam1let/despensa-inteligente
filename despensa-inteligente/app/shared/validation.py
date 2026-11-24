"""Validaciones de acceso (RF-01 / HU-01, CA-01.03 a CA-01.09).

Funciones puras: no usan base de datos, rutas, sesiones ni hash.
"""

from app.shared.errors import ErrorFormatoCorreo, ErrorLongitudContrasena
from app.shared.normalization import normalizar_correo

LONGITUD_MINIMA_CONTRASENA = 8
LONGITUD_MAXIMA_CONTRASENA = 64

MSG_CORREO_INVALIDO = "El correo no tiene un formato válido."
MSG_CONTRASENA_LONGITUD = (
    f"La contraseña debe tener entre {LONGITUD_MINIMA_CONTRASENA} "
    f"y {LONGITUD_MAXIMA_CONTRASENA} caracteres."
)


def validar_correo(correo: str) -> str:
    """Normaliza y valida el correo; devuelve el correo normalizado.

    Reglas mínimas (plan, sección 6):
    - sin espacios internos;
    - exactamente un '@' con texto antes y después;
    - el dominio contiene un punto con texto a ambos lados.
    """
    normalizado = normalizar_correo(correo)

    if not normalizado or any(c.isspace() for c in normalizado):
        raise ErrorFormatoCorreo(MSG_CORREO_INVALIDO)
    if normalizado.count("@") != 1:
        raise ErrorFormatoCorreo(MSG_CORREO_INVALIDO)

    local, dominio = normalizado.split("@")
    if not local or not dominio:
        raise ErrorFormatoCorreo(MSG_CORREO_INVALIDO)

    partes = dominio.split(".")
    if len(partes) < 2 or any(not parte for parte in partes):
        raise ErrorFormatoCorreo(MSG_CORREO_INVALIDO)

    return normalizado


def validar_contrasena(contrasena: str) -> str:
    """Valida que la contraseña tenga de 8 a 64 caracteres, tal cual.

    No recorta ni altera la contraseña, y nunca la registra.
    """
    if not isinstance(contrasena, str):
        raise TypeError("La contraseña debe ser texto.")
    if not (LONGITUD_MINIMA_CONTRASENA <= len(contrasena) <= LONGITUD_MAXIMA_CONTRASENA):
        raise ErrorLongitudContrasena(MSG_CONTRASENA_LONGITUD)
    return contrasena
