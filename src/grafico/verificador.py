# Verificación aparte de los resultados (método gráfico y programación dinámica).
# SciPy se usa SOLO aquí para comprobar; ningún método lo usa para resolver.
# Cada función devuelve (ok, mensaje): True si coincide, False si no, None si no se pudo.


def _iguales(a, b, tol=1e-4):
    return bool(abs(a - b) <= tol * max(1.0, abs(a), abs(b)))


def verificar_grafico(c1, c2, tipo_opt, restricciones, resultado):
    try:
        from scipy.optimize import linprog
    except ImportError:
        return None, "SciPy no está instalado."

    es_max = tipo_opt.lower().startswith("max")
    a_ub, b_ub, a_eq, b_eq = [], [], [], []
    for a, b, op, lado in restricciones:
        if op == "<=":
            a_ub.append([a, b]); b_ub.append(lado)
        elif op == ">=":
            a_ub.append([-a, -b]); b_ub.append(-lado)   # se pasa a <= multiplicando por -1
        else:
            a_eq.append([a, b]); b_eq.append(lado)

    obj = [-c1, -c2] if es_max else [c1, c2]            # linprog solo minimiza
    r = linprog(obj, A_ub=a_ub or None, b_ub=b_ub or None,
                A_eq=a_eq or None, b_eq=b_eq or None, bounds=(0, None))

    esperado = {0: "optimo", 2: "infactible", 3: "no acotado"}.get(r.status, "otro")
    obtenido = {"Unica": "optimo", "Empate": "optimo", "Infactible": "infactible",
                "No Acotado": "no acotado"}.get(resultado.get("estado"), "otro")

    if esperado != obtenido:
        return False, f"El software dice {resultado.get('estado')} y la verificación dice {esperado}."
    if esperado != "optimo":
        return True, f"Los dos coinciden: el problema es {esperado}."

    z_ver = -r.fun if es_max else r.fun
    z_sw = resultado["mejor_z"]
    if not _iguales(z_ver, z_sw):
        return False, f"Z del software = {z_sw:.4f}, Z de la verificación = {z_ver:.4f}."

    # los puntos óptimos que muestra el software deben cumplir las restricciones
    for x1, x2 in resultado.get("puntos_optimos", []):
        for a, b, op, lado in restricciones:
            v = a * x1 + b * x2
            if (op == "<=" and v > lado + 1e-3) or (op == ">=" and v < lado - 1e-3) \
                    or (op == "=" and abs(v - lado) > 1e-3):
                return False, f"El punto ({x1}, {x2}) no cumple una restricción."
    return True, f"Z del software = {z_sw:.4f} y Z de la verificación = {z_ver:.4f}."


def verificar_dp_enumeracion(etapas_data, tipo_opt, estado_inicial, resultado,
                             max_nodos=2_000_000):
    # Prueba todas las combinaciones de decisiones (sirve para problemas pequeños)
    es_max = tipo_opt.lower().startswith("max")
    mejor = [None]
    contador = [0]

    def explorar(i, s, acum):
        if i == len(etapas_data):
            if mejor[0] is None or (acum > mejor[0] if es_max else acum < mejor[0]):
                mejor[0] = acum
            return
        e = etapas_data[i]
        decisiones = e["decisiones"](s) if callable(e["decisiones"]) else e["decisiones"]
        for x in decisiones:
            contador[0] += 1
            if contador[0] > max_nodos:
                raise OverflowError
            try:
                costo = e["f_costo"](s, x)
                s_sig = e["transicion"](s, x)
            except Exception:
                continue        # decisión no factible
            explorar(i + 1, s_sig, acum + costo)

    try:
        explorar(0, estado_inicial, 0.0)
    except OverflowError:
        return None, "Hay demasiadas combinaciones para verificar por enumeración."

    if mejor[0] is None:
        ok = resultado.get("estado") == "Infactible"
        return ok, "No hay plan factible." if ok else "El software halló un plan y la enumeración no."
    if resultado.get("estado") == "Infactible":
        return False, "El software dice infactible pero sí existe un plan."
    ok = _iguales(mejor[0], resultado["valor_optimo"])
    return ok, f"Software = {resultado['valor_optimo']:.4f}, enumeración = {mejor[0]:.4f}."


def verificar_dp_inventario(demandas, costos_compra, costos_mant, inv_inicial,
                            inv_final_min, inv_min, inv_max, compra_max,
                            resultado, paso=1.0):
    # Modelo de compras e inventario resuelto como programa lineal entero
    # (solo para comprobar): s(t+1) = s(t) + x(t) - d(t)
    try:
        import numpy as np
        from scipy.optimize import milp, LinearConstraint, Bounds
    except ImportError:
        return None, "SciPy no está instalado."

    T = len(demandas)
    if not isinstance(compra_max, (list, tuple)):
        compra_max = [compra_max] * T

    d_acum = np.cumsum(demandas)
    # costo de la compra x(k) = su precio + el almacenamiento que genera en los meses siguientes
    coef = np.array([costos_compra[k] + sum(costos_mant[k:]) for k in range(T)], float)
    constante = sum(costos_mant[t] * (inv_inicial - d_acum[t]) for t in range(T))

    matriz = np.tril(np.ones((T, T))) * paso          # inventario acumulado en cada mes
    inf = np.array([inv_min] * (T - 1) + [max(inv_min, inv_final_min)], float) - inv_inicial + d_acum
    sup = np.array([inv_max] * T, float) - inv_inicial + d_acum
    tope = np.floor(np.array(compra_max, float) / paso + 1e-9)

    r = milp(coef * paso, constraints=LinearConstraint(matriz, inf, sup),
             integrality=np.ones(T), bounds=Bounds(0, tope))

    if not r.success:
        ok = resultado.get("estado") == "Infactible"
        return ok, "Los dos dicen infactible." if ok else "La verificación dice infactible pero el software halló plan."
    if resultado.get("estado") == "Infactible":
        return False, ("El software dice infactible pero la verificación halló un plan. "
                       "Revise que demanda e inventario inicial sean múltiplos del paso.")
    z_ver = r.fun + constante
    ok = _iguales(z_ver, resultado["valor_optimo"])
    return ok, f"Costo del software = {resultado['valor_optimo']:.4f}, de la verificación = {z_ver:.4f}."
