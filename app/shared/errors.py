"""Errores de validación de acceso (RF-01 / HU-01).

Cada error lleva un mensaje presentable para el usuario final.
"""


class ErrorValidacion(Exception):
    """Error base: los datos de acceso no cumplen las reglas de RF-01."""

    def __init__(self, mensaje: str):
        super().__init__(mensaje)
        self.mensaje = mensaje


class ErrorFormatoCorreo(ErrorValidacion):
    """El correo no tiene un formato válido."""


class ErrorLongitudContrasena(ErrorValidacion):
    """La contraseña no tiene entre 8 y 64 caracteres."""
