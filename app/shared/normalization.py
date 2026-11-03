"""Normalización de datos de acceso (RF-01)."""


def normalizar_correo(correo: str) -> str:
    """Recorta espacios en los extremos y pasa a minúsculas.

    No valida el formato: eso corresponde a validation.validar_correo.
    """
    if not isinstance(correo, str):
        raise TypeError("El correo debe ser texto.")
    return correo.strip().lower()
