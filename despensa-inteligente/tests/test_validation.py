"""Pruebas unitarias de T-03 (RF-01 / HU-01). Ejecutar: python -m unittest -v"""

import unittest

from app.shared.errors import ErrorFormatoCorreo, ErrorLongitudContrasena
from app.shared.normalization import normalizar_correo
from app.shared.validation import validar_contrasena, validar_correo


class PruebasNormalizacion(unittest.TestCase):
    def test_normaliza_mayusculas_y_espacios_extremos(self):
        # Apoya CA-01.02 (duplicado sin distinción de mayúsculas)
        self.assertEqual(normalizar_correo("  ANA@example.com "), "ana@example.com")


class PruebasCorreo(unittest.TestCase):
    def test_P_01_01_correo_valido_normal(self):
        self.assertEqual(validar_correo("ana@example.com"), "ana@example.com")

    def test_P_01_03_sin_arroba(self):
        with self.assertRaises(ErrorFormatoCorreo):
            validar_correo("anaexample.com")

    def test_P_01_04_dominio_sin_punto(self):
        with self.assertRaises(ErrorFormatoCorreo):
            validar_correo("ana@example")

    def test_P_01_05_espacio_interno(self):
        with self.assertRaises(ErrorFormatoCorreo):
            validar_correo("an a@example.com")

    def test_correo_vacio(self):
        with self.assertRaises(ErrorFormatoCorreo):
            validar_correo("   ")

    def test_dos_arrobas(self):
        with self.assertRaises(ErrorFormatoCorreo):
            validar_correo("a@b@example.com")


class PruebasContrasena(unittest.TestCase):
    def test_P_01_06_limite_8_caracteres(self):
        self.assertEqual(validar_contrasena("a" * 8), "a" * 8)

    def test_P_01_07_limite_64_caracteres(self):
        self.assertEqual(validar_contrasena("a" * 64), "a" * 64)

    def test_P_01_08_7_caracteres_rechazada(self):
        with self.assertRaises(ErrorLongitudContrasena):
            validar_contrasena("a" * 7)

    def test_P_01_09_65_caracteres_rechazada(self):
        with self.assertRaises(ErrorLongitudContrasena):
            validar_contrasena("a" * 65)


if __name__ == "__main__":
    unittest.main()
