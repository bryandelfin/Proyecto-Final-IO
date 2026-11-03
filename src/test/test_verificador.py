# Pruebas automáticas del módulo de verificación (y del software que verifica).
# Ejecutar desde la raíz del proyecto:   python -m pytest src/test -v
# No necesitan interfaz gráfica: se simulan los campos de entrada de Tkinter.
import os
import sys
import types

import pytest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "grafico"))
sys.path.insert(0, os.path.join(RAIZ, "dinamica"))

pytest.importorskip("scipy")      # la verificación necesita SciPy
import verificador as vf



# Ayudas: ejecutar el método gráfico real sin abrir ventanas

class _Campo:                      # imita un Entry/Combobox de Tkinter
    def __init__(self, v): self.v = v
    def get(self): return str(self.v)


def resolver_grafico_headless(c1, c2, tipo, restricciones):
    panel = types.ModuleType("panel_entrada")
    panel.entry_valor1, panel.entry_valor2 = _Campo(c1), _Campo(c2)
    panel.comboOp = _Campo(tipo)
    panel.entry_nombre1, panel.entry_nombre2 = _Campo("x1"), _Campo("x2")
    lista = types.ModuleType("logica_restricciones")
    lista.entradas_restricciones = [(_Campo(a), _Campo(b), _Campo(op), _Campo(r))
                                    for a, b, op, r in restricciones]
    sys.modules["panel_entrada"] = panel
    sys.modules["logica_restricciones"] = lista
    sys.modules.pop("logica_metodo_grafico", None)
    import logica_metodo_grafico
    return logica_metodo_grafico.resolver_modelo_grafico()


# Problema real 1 (informe): mezcla Arábica/Robusta, miles de lb y miles de USD
COFFEE = [(1, 1, ">=", 44), (2, -3, ">=", 0), (-1, 4, ">=", 0), (1, 0, "<=", 36)]


# MÉTODO GRÁFICO

def test_grafico_caso_real_coffee_holding():
    res = resolver_grafico_headless(3.157, 1.5803, "Minimizar", COFFEE)
    ok, msg = vf.verificar_grafico(3.157, 1.5803, "Minimizar", COFFEE, res)
    assert ok, msg
    assert res["mejor_z"] == pytest.approx(111.15808, rel=1e-5)   # 26,4 y 17,6


def test_grafico_infactible():
    restr = [(1, 1, "<=", 1), (1, 1, ">=", 5)]
    res = resolver_grafico_headless(1, 1, "Maximizar", restr)
    ok, msg = vf.verificar_grafico(1, 1, "Maximizar", restr, res)
    assert ok, msg


def test_grafico_no_acotado():
    restr = [(1, -1, "<=", 1), (1, 0, ">=", 0)]
    res = resolver_grafico_headless(1, 1, "Maximizar", restr)
    ok, msg = vf.verificar_grafico(1, 1, "Maximizar", restr, res)
    assert ok, msg


def test_grafico_optimos_alternativos():
    restr = [(1, 1, "<=", 4), (1, 0, "<=", 3), (0, 1, "<=", 3)]
    res = resolver_grafico_headless(1, 1, "Maximizar", restr)   # z=4 en toda la arista
    ok, msg = vf.verificar_grafico(1, 1, "Maximizar", restr, res)
    assert ok, msg
    assert res["estado"] == "Empate"


def test_verificador_detecta_resultado_incorrecto():
    falso = {"estado": "Unica", "mejor_z": 999.0, "puntos_optimos": []}
    ok, _ = vf.verificar_grafico(3.157, 1.5803, "Minimizar", COFFEE, falso)
    assert ok is False


# PROGRAMACIÓN DINÁMICA  (inventario pequeño de 4 etapas)

from logica_programacion_dinamica import resolver_programacion_dinamica

D = [2, 3, 2, 3]; C = [10, 12, 9, 11]; H = [1, 1, 1, 1]
S0, SFIN, SMIN, SMAX, XMAX = 5, 4, 3, 8, 5


def etapas_inventario(final_min=SFIN):
    etapas = []
    for t in range(len(D)):
        def trans(s, x, t=t):
            s2 = s + x - D[t]
            if not (SMIN <= s2 <= SMAX):
                raise ValueError("inventario fuera de límites")
            if t == len(D) - 1 and s2 < final_min:
                raise ValueError("inventario final insuficiente")
            return s2
        etapas.append({"nombre": f"Mes {t+1}",
                       "estados": list(range(SMIN, SMAX + 1)),
                       "decisiones": list(range(XMAX + 1)),
                       "f_costo": lambda s, x, t=t: C[t] * x + H[t] * (s + x - D[t]),
                       "transicion": trans})
    return etapas


def test_dp_enumeracion_coincide():
    et = etapas_inventario()
    res = resolver_programacion_dinamica(et, "Minimizar", S0)
    ok, msg = vf.verificar_dp_enumeracion(et, "Minimizar", S0, res)
    assert ok, msg


def test_dp_milp_coincide():
    et = etapas_inventario()
    res = resolver_programacion_dinamica(et, "Minimizar", S0)
    ok, msg = vf.verificar_dp_inventario(D, C, H, S0, SFIN, SMIN, SMAX, XMAX, res)
    assert ok, msg


def test_dp_infactible_coincide():
    et = etapas_inventario(final_min=20)            # imposible: s_max = 8
    res = resolver_programacion_dinamica(et, "Minimizar", S0)
    assert res["estado"] == "Infactible"
    ok1, m1 = vf.verificar_dp_enumeracion(et, "Minimizar", S0, res)
    ok2, m2 = vf.verificar_dp_inventario(D, C, H, S0, 20, SMIN, SMAX, XMAX, res)
    assert ok1 and ok2, (m1, m2)


# Casos que hoy FALLAN en logica_metodo_grafico.py (detección de no acotado):
def test_grafico_min_no_acotado():
    restr = [(1, -1, "<=", 1)]
    res = resolver_grafico_headless(-1, -1, "Minimizar", restr)
    ok, msg = vf.verificar_grafico(-1, -1, "Minimizar", restr, res)
    assert ok, msg


def test_grafico_max_acotado_con_coeficiente_negativo():
    restr = [(-1, 1, "<=", 2), (1, 0, "<=", 3), (0, 1, "<=", 3)]
    res = resolver_grafico_headless(1, 1, "Maximizar", restr)   # óptimo z = 6
    ok, msg = vf.verificar_grafico(1, 1, "Maximizar", restr, res)
    assert ok, msg
