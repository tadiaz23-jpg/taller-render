"""
Módulo principal de lógica de la calculadora.
Implementa las operaciones básicas y extendidas para el Taller de TBD + Feature Toggles.
"""

class Calculator:
    @staticmethod
    def sumar(a: float, b: float) -> float:
        return a + b

    @staticmethod
    def restar(a: float, b: float) -> float:
        return a - b

    @staticmethod
    def multiplicar(a: float, b: float) -> float:
        """Operación de multiplicación (Ejemplo 5 - Slice 1)"""
        return a * b

    @staticmethod
    def dividir(a: float, b: float) -> float:
        """Operación de división con validación de error por cero (Ejemplo 5 - Slice 3)"""
        if b == 0:
            raise ValueError("No se puede dividir por cero")
        return a / b
