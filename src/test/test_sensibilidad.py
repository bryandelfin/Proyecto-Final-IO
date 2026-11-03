# Pruebas del análisis de sensibilidad del método gráfico.
# Ejecutar desde la raíz del proyecto:   python -m pytest src/test -q
import os
import sys

import pytest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "grafico"))

from analisis_sensibilidad import analizar_sensibilidad, resolver_grafico_datos

COFFEE = [(1, 1, ">=", 44), (2, -3, ">=", 0), (-1, 4, ">=", 0), (1, 0, "<=", 36)]


def _por_indice(lista):
    return {item["indice"]: item for item in lista}


def test_coffee_precios_sombra():
    sens = analizar_sensibilidad(3.157, 1.5803, "Minimizar", COFFEE)
    assert sens["disponible"]
    precios = _por_indice(sens["precios_sombra"])
    assert precios[1]["precio"] == pytest.approx(2.52632, rel=1e-4)
    assert precios[2]["precio"] == pytest.approx(0.31534, rel=1e-4)
    assert precios[3]["precio"] == 0
    assert precios[4]["precio"] == 0
    assert precios[1]["activa"] and precios[2]["activa"]
    assert not precios[3]["activa"] and not precios[4]["activa"]


def test_coffee_rangos_coeficientes():
    sens = analizar_sensibilidad(3.157, 1.5803, "Minimizar", COFFEE)
    rangos = _por_indice(sens["rangos_coeficientes"])
    assert rangos[1]["min"] == pytest.approx(1.5803, rel=1e-4)
    assert rangos[1]["max"] is None
    assert rangos[2]["min"] == pytest.approx(-4.7355, rel=1e-4)
    assert rangos[2]["max"] == pytest.approx(3.157, rel=1e-4)


def test_coffee_rango_lado_derecho_r1():
    sens = analizar_sensibilidad(3.157, 1.5803, "Minimizar", COFFEE)
    rangos = _por_indice(sens["rangos_lado_derecho"])
    assert rangos[1]["min"] == pytest.approx(0, abs=1e-2)
    assert rangos[1]["max"] == pytest.approx(60, abs=1e-2)


def test_sin_optimo_unico_no_hay_sensibilidad():
    infactible = [(1, 1, "<=", 1), (1, 1, ">=", 5)]
    empate = [(1, 1, "<=", 4), (1, 0, "<=", 3), (0, 1, "<=", 3)]
    no_acotado = []
    for tipo, restr in (("Maximizar", infactible),
                        ("Maximizar", empate),
                        ("Maximizar", no_acotado)):
        sens = analizar_sensibilidad(1, 1, tipo, restr)
        assert not sens["disponible"]
        assert sens["mensaje"]


def test_vertice_degenerado_sigue_siendo_unico():
    degenerado = [(1, 0, "<=", 1), (0, 1, "<=", 1), (1, 1, "<=", 2)]
    base = resolver_grafico_datos(1, 1, "Maximizar", degenerado)
    assert base["estado"] == "Unica"
    sens = analizar_sensibilidad(1, 1, "Maximizar", degenerado)
    assert sens["disponible"]
