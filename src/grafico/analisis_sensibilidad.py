# Análisis de sensibilidad para el método gráfico.
# Todo el cálculo se hace re-resolviendo el modelo gráfico con datos modificados.
# No usa SciPy ni ninguna librería de optimización: la librería queda solo para verificar.

import math

_TOL = 1e-5


def _cumple_restriccion(a, b, op, c, px, py, tol=_TOL):
    valor = a * px + b * py
    if op == "<=":
        return valor <= c + tol
    if op == ">=":
        return valor >= c - tol
    return abs(valor - c) <= tol


def resolver_grafico_datos(c1, c2, tipo_opt, restricciones):
    """Resuelve el método gráfico con datos explícitos (sin depender de Tkinter).

    Es la misma lógica de vértices y detección de casos que usa el método
    gráfico; se separa aquí para poder cambiar los datos y volver a resolver,
    que es como se obtiene la sensibilidad en el método gráfico.
    """
    restricciones = list(restricciones)
    restricciones_completas = restricciones + [(1.0, 0.0, ">=", 0.0),
                                                (0.0, 1.0, ">=", 0.0)]
    lineas = [(a, b, c) for a, b, op, c in restricciones_completas]

    puntos = []
    n = len(lineas)
    for i in range(n):
        for j in range(i + 1, n):
            a1, b1, c1_l = lineas[i]
            a2, b2, c2_l = lineas[j]
            det = (a1 * b2) - (a2 * b1)

            if abs(det) > 1e-5:
                x = (c1_l * b2 - c2_l * b1) / det
                y = (a1 * c2_l - a2 * c1_l) / det
                if x >= -1e-5 and y >= -1e-5:
                    puntos.append((max(0.0, x), max(0.0, y)))

    puntos_factibles = []
    for px, py in puntos:
        if all(_cumple_restriccion(a, b, op, c, px, py)
               for a, b, op, c in restricciones_completas):
            redondeado = (round(px, 10), round(py, 10))
            repetido = any(
                abs(redondeado[0] - rx) < 1e-7 and abs(redondeado[1] - ry) < 1e-7
                for rx, ry in puntos_factibles
            )
            if not repetido:
                puntos_factibles.append(redondeado)

    if not puntos_factibles:
        return {
            "estado": "Infactible",
            "tipo_opt": tipo_opt,
            "restricciones": restricciones,
            "restricciones_completas": restricciones_completas,
            "puntos_factibles": [],
            "puntos_optimos": [],
            "mejor_z": 0.0,
            "direcciones_recesion": [],
        }

    evaluaciones = [(punto, c1 * punto[0] + c2 * punto[1])
                    for punto in puntos_factibles]

    def es_direccion_recesion(dx, dy):
        for a, b, op, c in restricciones_completas:
            valor = a * dx + b * dy
            if op == "<=" and valor > 1e-7:
                return False
            if op == ">=" and valor < -1e-7:
                return False
            if op == "=" and abs(valor) > 1e-7:
                return False
        return True

    candidatas = [(1.0, 0.0), (0.0, 1.0)]
    for a, b, op, c in restricciones_completas:
        if abs(a) + abs(b) > 1e-9:
            candidatas.append((b, -a))
            candidatas.append((-b, a))

    direcciones_recesion = []
    es_no_acotado = False
    for dx, dy in candidatas:
        if abs(dx) + abs(dy) < 1e-9 or not es_direccion_recesion(dx, dy):
            continue

        norma = math.hypot(dx, dy)
        if norma > 1e-12:
            direccion = (dx / norma, dy / norma)
            if not any(abs(direccion[0] - d[0]) < 1e-9 and
                       abs(direccion[1] - d[1]) < 1e-9
                       for d in direcciones_recesion):
                direcciones_recesion.append(direccion)

        mejora = c1 * dx + c2 * dy
        if (tipo_opt == "Maximizar" and mejora > 1e-7) or (
            tipo_opt == "Minimizar" and mejora < -1e-7
        ):
            es_no_acotado = True

    if es_no_acotado:
        return {
            "estado": "No Acotado",
            "tipo_opt": tipo_opt,
            "restricciones": restricciones,
            "restricciones_completas": restricciones_completas,
            "puntos_factibles": puntos_factibles,
            "puntos_optimos": [],
            "mejor_z": 0.0,
            "direcciones_recesion": direcciones_recesion,
        }

    mejor_z = (max(z for _, z in evaluaciones) if tipo_opt == "Maximizar"
               else min(z for _, z in evaluaciones))

    tol = 1e-9 * max(1.0, abs(mejor_z))
    puntos_optimos = [p for p, z in evaluaciones if abs(z - mejor_z) < tol]
    puntos_optimos = list(set(puntos_optimos))
    estado = "Empate" if len(puntos_optimos) > 1 else "Unica"

    return {
        "estado": estado,
        "tipo_opt": tipo_opt,
        "restricciones": restricciones,
        "restricciones_completas": restricciones_completas,
        "puntos_factibles": puntos_factibles,
        "puntos_optimos": puntos_optimos,
        "mejor_z": mejor_z,
        "direcciones_recesion": direcciones_recesion,
    }


def _punto_optimo(resultado):
    optimos = resultado.get("puntos_optimos", [])
    return optimos[0] if optimos else None


def _indices_activos(resultado):
    """Índices de restricciones (incluidas no negatividad) activas en el óptimo."""
    punto = _punto_optimo(resultado)
    if punto is None:
        return []
    px, py = punto
    activos = []
    for indice, (a, b, op, c) in enumerate(resultado["restricciones_completas"]):
        valor = a * px + b * py
        holgura = 1e-7 * max(1.0, abs(c), abs(valor))
        if abs(valor - c) <= holgura:
            activos.append(indice)
    return activos


def _resolver_con_lado_derecho(c1, c2, tipo_opt, restricciones, indice, nuevo_valor):
    modificadas = list(restricciones)
    a, b, op, c = modificadas[indice]
    modificadas[indice] = (a, b, op, nuevo_valor)
    return resolver_grafico_datos(c1, c2, tipo_opt, modificadas)


def _misma_base(resultado, base_activa):
    if resultado.get("estado") != "Unica":
        return False
    return frozenset(_indices_activos(resultado)) == base_activa


def _buscar_limite_base(c1, c2, tipo_opt, restricciones, indice, base_activa,
                        direccion):
    """Busca el límite del lado derecho manteniendo la misma base óptima."""
    b0 = float(restricciones[indice][3])
    if abs(restricciones[indice][0]) < 1e-12 and abs(restricciones[indice][1]) < 1e-12:
        return None

    paso = max(1.0, abs(b0) * 0.25, 0.5)
    ultimo_bueno = b0
    actual = b0

    for _ in range(80):
        actual += direccion * paso

        if abs(actual) > 1e12:
            return None

        try:
            resultado = _resolver_con_lado_derecho(
                c1, c2, tipo_opt, restricciones, indice, actual
            )
        except Exception:
            resultado = None

        if resultado is not None and _misma_base(resultado, base_activa):
            ultimo_bueno = actual
            paso *= 2.0
            continue

        malo = actual
        bueno = ultimo_bueno
        for _ in range(80):
            medio = (bueno + malo) / 2.0
            try:
                resultado_medio = _resolver_con_lado_derecho(
                    c1, c2, tipo_opt, restricciones, indice, medio
                )
            except Exception:
                resultado_medio = None

            if resultado_medio is not None and _misma_base(resultado_medio, base_activa):
                bueno = medio
            else:
                malo = medio

        return bueno

    return None


def _rangos_lado_derecho(c1, c2, tipo_opt, restricciones, base):
    base_activa = frozenset(_indices_activos(base))
    rangos = []

    for indice, (a, b, op, c) in enumerate(restricciones):
        if abs(a) < 1e-12 and abs(b) < 1e-12:
            rangos.append({"indice": indice + 1, "actual": c, "min": None,
                           "max": None})
            continue

        maximo = _buscar_limite_base(
            c1, c2, tipo_opt, restricciones, indice, base_activa, 1.0
        )
        minimo = _buscar_limite_base(
            c1, c2, tipo_opt, restricciones, indice, base_activa, -1.0
        )
        rangos.append({
            "indice": indice + 1,
            "actual": c,
            "min": minimo,
            "max": maximo,
        })

    return rangos


def _rango_coeficiente(base, c1, c2, indice_coeficiente):
    """Rango de c1 (índice 0) o c2 (índice 1) que conserva el mismo óptimo."""
    punto = _punto_optimo(base)
    if punto is None:
        return None, None

    px, py = punto
    criticos = set()

    for qx, qy in base.get("puntos_factibles", []):
        if abs(px - qx) < 1e-9 and abs(py - qy) < 1e-9:
            continue

        if indice_coeficiente == 0:
            numerador = px - qx
            termino = c2 * (py - qy)
        else:
            numerador = py - qy
            termino = c1 * (px - qx)

        if abs(numerador) > 1e-9:
            critico = -termino / numerador
            if math.isfinite(critico):
                criticos.add(round(critico, 9))

    for dx, dy in base.get("direcciones_recesion", []):
        if indice_coeficiente == 0:
            if abs(dx) > 1e-9:
                critico = -c2 * dy / dx
                if math.isfinite(critico):
                    criticos.add(round(critico, 9))
        else:
            if abs(dy) > 1e-9:
                critico = -c1 * dx / dy
                if math.isfinite(critico):
                    criticos.add(round(critico, 9))

    actual = c1 if indice_coeficiente == 0 else c2
    menores = [valor for valor in criticos if valor < actual - 1e-7]
    mayores = [valor for valor in criticos if valor > actual + 1e-7]

    minimo = max(menores) if menores else None
    maximo = min(mayores) if mayores else None
    return minimo, maximo


def _precio_sombra(c1, c2, tipo_opt, restricciones, base, indice,
                   base_activa, activos):
    a, b, op, c = restricciones[indice]
    if indice not in activos or (abs(a) < 1e-12 and abs(b) < 1e-12):
        return 0.0

    delta = max(1e-3, abs(c) * 1e-4)
    z0 = base["mejor_z"]

    for signo in (1.0, -1.0):
        try:
            resultado = _resolver_con_lado_derecho(
                c1, c2, tipo_opt, restricciones, indice, c + signo * delta
            )
        except Exception:
            continue

        if resultado.get("estado") == "Unica":
            return (resultado["mejor_z"] - z0) / (signo * delta)

    return None


def _formatear(valor, decimales=4):
    if valor is None:
        return "sin límite"
    redondeado = round(valor, decimales)
    if abs(redondeado) < 10 ** (-decimales):
        redondeado = 0.0
    return f"{redondeado:g}"


def _frase_precio_sombra(precio, activa):
    if precio is None:
        return "No se pudo determinar un precio sombra con un cambio pequeño."
    if not activa:
        return "No limita la solución actual: su precio sombra es 0."
    if abs(precio) < 1e-7:
        return "Está activa, pero su efecto marginal sobre Z es nulo."
    if precio > 0:
        return (f"Cada unidad adicional del lado derecho aumenta Z en "
                f"{_formatear(abs(precio))}; esta restricción condiciona la decisión.")
    return (f"Cada unidad adicional del lado derecho reduce Z en "
            f"{_formatear(abs(precio))}; esta restricción condiciona la decisión.")


def analizar_sensibilidad(c1, c2, tipo_opt, restricciones):
    """Calcula precios sombra y rangos re-resolviendo el modelo gráfico."""
    restricciones = list(restricciones)
    base = resolver_grafico_datos(c1, c2, tipo_opt, restricciones)

    if base["estado"] != "Unica":
        mensajes = {
            "Infactible": "El modelo es infactible: no hay solución óptima que analizar.",
            "No Acotado": "El modelo es no acotado: no hay un óptimo finito que analizar.",
            "Empate": ("Hay múltiples soluciones óptimas; los precios sombra y los "
                       "rangos no son únicos. Se requiere un óptimo único."),
        }
        return {
            "disponible": False,
            "mensaje": mensajes.get(base["estado"], "No hay solución óptima única."),
            "resultado": base,
        }

    activos = set(_indices_activos(base))
    base_activa = frozenset(activos)

    rangos_lado_derecho = _rangos_lado_derecho(
        c1, c2, tipo_opt, restricciones, base
    )

    precios_sombra = []
    for indice, (a, b, op, c) in enumerate(restricciones):
        precio = _precio_sombra(
            c1, c2, tipo_opt, restricciones, base, indice, base_activa, activos
        )
        es_activa = indice in activos
        precios_sombra.append({
            "indice": indice + 1,
            "operador": op,
            "lado_derecho": c,
            "precio": precio,
            "activa": es_activa,
            "frase": _frase_precio_sombra(precio, es_activa),
        })

    minimo_c1, maximo_c1 = _rango_coeficiente(base, c1, c2, 0)
    minimo_c2, maximo_c2 = _rango_coeficiente(base, c1, c2, 1)
    rangos_coeficientes = [
        {"indice": 1, "actual": c1, "min": minimo_c1, "max": maximo_c1},
        {"indice": 2, "actual": c2, "min": minimo_c2, "max": maximo_c2},
    ]

    return {
        "disponible": True,
        "mensaje": "",
        "resultado": base,
        "precios_sombra": precios_sombra,
        "rangos_coeficientes": rangos_coeficientes,
        "rangos_lado_derecho": rangos_lado_derecho,
    }
