# Módulo de lógica para Programación Dinámica (Procedimiento Hacia Atrás / Backward)
# Investigación de Operaciones - Adaptable a problemas de etapas deterministas

import math

def resolver_programacion_dinamica(etapas_data, tipo_opt="Maximizar", capacidad_inicial=0):
    """
    Resuelve un problema de Programación Dinámica hacia atrás de 1 a 8 etapas.
    
    Args:
        etapas_data (list): Lista de diccionarios por etapa (de la etapa 1 a la N).
            Cada elemento representa una etapa y contiene:
            {
                "nombre": "Etapa 1",
                "estados": [list de estados de entrada posibles (ej. 0..Capacidad)],
                "decisiones": [list de decisiones posibles para cada estado],
                "f_costo": función(estado, decision) -> rendimiento/costo inmediato,
                "transicion": función(estado, decision) -> nuevo_estado (recurso restante/acumulado)
            }
        tipo_opt (str): "Maximizar" o "Minimizar".
        capacidad_inicial (float/int): Estado inicial de la etapa 1.

    Returns:
        dict: {
            "estado": "Exitoso" | "Infactible",
            "tipo_opt": tipo_opt,
            "valor_optimo": float,
            "tablas_etapas": list, # Resultados detallados por etapa (evaluadas de N a 1)
            "ruta_optima": list    # Trayectoria de decisiones óptimas desde Etapa 1 a N
        }
    """
    N = len(etapas_data)
    if N < 1 or N > 8:
        raise ValueError("El número de etapas debe estar comprendido entre 1 y 8.")

    es_max = (tipo_opt.lower() == "maximizar")
    val_invalido = float('-inf') if es_max else float('inf')

    # Almacenará la función de valor óptimo f_k*(s) para cada etapa k
    # f_opt_siguiente[estado] = valor_optimo
    f_opt_siguiente = {}

    tablas_resultados = []

    # PROCEDIMIENTO HACIA ATRÁS (Backward): Evaluar desde la etapa N hasta la 1
    for i in range(N - 1, -1, -1):
        etapa_num = i + 1
        etapa_info = etapas_data[i]
        
        estados = etapa_info.get("estados", [])
        decisiones_fn = etapa_info.get("decisiones") # Puede ser lista fija o función (estado) -> lista
        f_costo = etapa_info.get("f_costo")
        transicion = etapa_info.get("transicion")

        f_opt_actual = {}
        tabla_etapa = {
            "etapa": etapa_num,
            "nombre": etapa_info.get("nombre", f"Etapa {etapa_num}"),
            "filas": []
        }

        for s in estados:
            decisiones_posibles = decisiones_fn(s) if callable(decisiones_fn) else decisiones_fn
            
            mejor_val = val_invalido
            mejores_decisiones = []
            evaluaciones_estado = []

            for x in decisiones_posibles:
                try:
                    # 1. Rendimiento / Costo de la etapa actual
                    r_cx = f_costo(s, x)
                    # 2. Estado siguiente resultante (función de transición)
                    s_sig = transicion(s, x)
                except Exception:
                    # Decisión fuera de límites de la función de transición/costo
                    evaluaciones_estado.append({
                        "decision": x,
                        "estado_sig": None,
                        "valor_acumulado": "Infactible",
                        "factible": False
                    })
                    continue

                # Si es la última etapa (N), no hay f_{k+1}*
                if i == N - 1:
                    val_acumulado = r_cx
                    factible = True
                else:
                    # En etapas previas, buscar el valor acumulado f_{k+1}*(s_sig)
                    if s_sig in f_opt_siguiente and f_opt_siguiente[s_sig] != val_invalido:
                        val_acumulado = r_cx + f_opt_siguiente[s_sig]
                        factible = True
                    else:
                        val_acumulado = val_invalido
                        factible = False

                if factible:
                    evaluaciones_estado.append({
                        "decision": x,
                        "estado_sig": s_sig,
                        "valor_acumulado": round(val_acumulado, 4),
                        "factible": True
                    })

                    # Comparar óptimos considerando tolerancia numérica de punto flotante
                    tol = 1e-5
                    if es_max:
                        if val_acumulado > mejor_val + tol:
                            mejor_val = val_acumulado
                            mejores_decisiones = [x]
                        elif abs(val_acumulado - mejor_val) <= tol:
                            mejores_decisiones.append(x) # ¡Empate / Óptimos alternativos!
                    else:
                        if val_acumulado < mejor_val - tol:
                            mejor_val = val_acumulado
                            mejores_decisiones = [x]
                        elif abs(val_acumulado - mejor_val) <= tol:
                            mejores_decisiones.append(x) # ¡Empate / Óptimos alternativos!
                else:
                    evaluaciones_estado.append({
                        "decision": x,
                        "estado_sig": s_sig,
                        "valor_acumulado": "Infactible",
                        "factible": False
                    })

            # Registrar resultado del estado s
            es_factible_estado = (mejor_val != val_invalido)
            es_empate = len(mejores_decisiones) > 1

            if es_factible_estado:
                f_opt_actual[s] = mejor_val
                val_opt_str = round(mejor_val, 4)
            else:
                f_opt_actual[s] = val_invalido
                val_opt_str = "Infactible"

            tabla_etapa["filas"].append({
                "estado": s,
                "evaluaciones": evaluaciones_estado,
                "valor_optimo": val_opt_str,
                "decisiones_optimas": mejores_decisiones if es_factible_estado else [],
                "factible": es_factible_estado,
                "es_empate": es_empate
            })

        # Guardar resultados de la etapa actual para consulta de la etapa anterior (Backward)
        f_opt_siguiente = f_opt_actual
        tablas_resultados.append(tabla_etapa)

    # Las tablas se generaron en orden N -> 1, invertimos para presentarlas secuencialmente 1 -> N
    tablas_resultados.reverse()

    # Reconstrucción del Camino / Solución Óptima desde la Etapa 1
    estado_corr = capacidad_inicial
    ruta_optima = []
    hay_empate_global = False
    estado_general = "Exitoso"

    for t in tablas_resultados:
        etapa_idx = t["etapa"]
        # Buscar la fila del estado actual
        fila_estado = next((f for f in t["filas"] if f["estado"] == estado_corr), None)

        if not fila_estado or not fila_estado["factible"]:
            estado_general = "Infactible"
            break

        decisiones_opt = fila_estado["decisiones_optimas"]
        if fila_estado["es_empate"]:
            hay_empate_global = True

        # Tomamos la primera decisión óptima para avanzar en el trazado
        d_opt = decisiones_opt[0]
        ruta_optima.append({
            "etapa": etapa_idx,
            "estado": estado_corr,
            "decision_optima": d_opt,
            "todas_decisiones_optimas": decisiones_opt,
            "empate": fila_estado["es_empate"]
        })

        # Transición al siguiente estado
        etapa_data_corr = etapas_data[etapa_idx - 1]
        estado_corr = etapa_data_corr["transicion"](estado_corr, d_opt)

    val_final = f_opt_siguiente.get(capacidad_inicial, val_invalido)
    if val_final == val_invalido:
        estado_general = "Infactible"

    if estado_general == "Exitoso" and hay_empate_global:
        estado_general = "Empate"

    return {
        "estado": estado_general,
        "tipo_opt": tipo_opt,
        "valor_optimo": round(val_final, 4) if estado_general != "Infactible" else 0,
        "tablas_etapas": tablas_resultados,
        "ruta_optima": ruta_optima
    }