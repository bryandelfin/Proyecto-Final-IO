# Módulo de lógica para el método gráfico
# Método Gráfico - Investigación de Operaciones

import panel_entrada
from logica_restricciones import entradas_restricciones

def resolver_modelo_grafico():
    try:
        c1 = float(panel_entrada.entry_valor1.get())
        c2 = float(panel_entrada.entry_valor2.get())
        tipo_opt = panel_entrada.combo.get()
    except ValueError:
        raise ValueError("Ingrese valores numéricos válidos en la Función Objetivo.")

    restricciones = []
    for i, (entry_v1, entry_v2, combo_desigualdad, entry_lado_derecho) in enumerate(entradas_restricciones):
        try:
            a = float(entry_v1.get())
            b = float(entry_v2.get())
            op = combo_desigualdad.get()
            c = float(entry_lado_derecho.get())
            restricciones.append((a, b, op, c))
        except ValueError:
            raise ValueError(f"Verifique los valores numéricos en la Restricción {i+1}.")
    
    # Validar que existan restricciones
    if not restricciones:
        raise ValueError("No hay restricciones definidas. Pulsa 'Generar' primero.")

    restricciones_completas = restricciones + [(1, 0, ">=", 0), (0, 1, ">=", 0)]
    lineas = [(a, b, c) for a, b, op, c in restricciones_completas]

    # Encontrar intersecciones
    puntos = []
    n = len(lineas)
    for i in range(n):
        for j in range(i + 1, n):
            a1, b1, c1_l = lineas[i]
            a2, b2, c2_l = lineas[j]
            det = (a1 * b2) - (a2 * b1)
            
            if abs(det) > 1e-5:
                # Calcular punto de intersección
                x = (c1_l * b2 - c2_l * b1) / det
                y = (a1 * c2_l - a2 * c1_l) / det
                if x >= -1e-5 and y >= -1e-5:
                    puntos.append((round(max(0, x), 4), round(max(0, y), 4)))

    # Filtrar puntos factibles
    puntos_factibles = []
    for px, py in puntos:
        factible = True
        for a, b, op, c in restricciones_completas:
            val = a * px + b * py
            if op == "<=" and val > c + 1e-5:
                factible = False
                break
            elif op == ">=" and val < c - 1e-5:
                factible = False
                break
            elif op == "=" and abs(val - c) > 1e-5:
                factible = False
                break
        # Evitar puntos duplicados
        if factible and (px, py) not in puntos_factibles:
            puntos_factibles.append((px, py))

    # CASO: INFACTIBLE
    if not puntos_factibles:
        return {
            "estado": "Infactible",
            "restricciones": restricciones,
            "puntos_factibles": [],
            "puntos_optimos": [],
            "mejor_z": 0
        }

    # Evaluar Z en los vértices factibles
    evaluaciones = []
    for px, py in puntos_factibles:
        z = c1 * px + c2 * py
        evaluaciones.append(((px, py), z))

    # Detección de No Acotado
    es_no_acotado = False
    if tipo_opt == "Maximizar":
        tiene_cota_superior = any(op == "<=" and (a > 0 or b > 0) for a, b, op, c in restricciones)
        if not tiene_cota_superior or any(a < 0 and op == "<=" for a, b, op, c in restricciones):
            es_no_acotado = True

    if es_no_acotado:
        return {
            "estado": "No Acotado",
            "restricciones": restricciones,
            "puntos_factibles": puntos_factibles,
            "puntos_optimos": [],
            "mejor_z": 0
        }

    mejor_z = max(z for _, z in evaluaciones) if tipo_opt == "Maximizar" else min(z for _, z in evaluaciones)

    tol = 1e-4
    puntos_optimos = [p for p, z in evaluaciones if abs(z - mejor_z) < tol]
    puntos_optimos = list(set(puntos_optimos))

    estado = "Empate" if len(puntos_optimos) > 1 else "Unica"

    nombre_v1 = panel_entrada.entry_nombre1.get().strip() or "X1"
    nombre_v2 = panel_entrada.entry_nombre2.get().strip() or "X2"
    
    return {
        "estado": estado,
        "tipo_opt": tipo_opt,
        "restricciones": restricciones,
        "puntos_factibles": puntos_factibles,
        "puntos_optimos": puntos_optimos,
        "mejor_z": mejor_z,
        "nombre_v1": nombre_v1,
        "nombre_v2": nombre_v2
    }
