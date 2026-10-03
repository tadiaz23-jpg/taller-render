"""
Pruebas unitarias para la lógica matemática de la calculadora.
"""
import pytest
from calculator import Calculator

def test_sumar():
    assert Calculator.sumar(5, 3) == 8
    assert Calculator.sumar(-1, 1) == 0

def test_restar():
    assert Calculator.restar(10, 4) == 6
    assert Calculator.restar(0, 5) == -5

def test_multiplicar():
    assert Calculator.multiplicar(6, 7) == 42
    assert Calculator.multiplicar(0, 10) == 0

def test_dividir():
    assert Calculator.dividir(20, 5) == 4.0
    assert Calculator.dividir(7, 2) == 3.5

def test_dividir_por_cero():
    with pytest.raises(ValueError, match="No se puede dividir por cero"):
        Calculator.dividir(10, 0)
