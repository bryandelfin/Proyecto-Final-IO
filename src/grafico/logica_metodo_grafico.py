# Módulo de lógica para el método gráfico
# Método Gráfico - Investigación de Operaciones

import panel_entrada
from logica_restricciones import entradas_restricciones

def resolver_modelo_grafico():
    """
    Resuelve el modelo matemático mediante el método gráfico.
    Calcula la región factible, encuentra los vértices y determina la solución óptima.
    
    Returns:
        dict: Diccionario con tipo de optimización, restricciones, puntos factibles, 
              punto óptimo, valor óptimo y nombres de variables
    
    Raises:
        ValueError: Si hay errores en los datos ingresados o no hay región factible
    """
    # Obtener datos de la función objetivo
    try:
        c1 = float(panel_entrada.entry_valor1.get())
        c2 = float(panel_entrada.entry_valor2.get())
        tipo_opt = panel_entrada.comboOp.get()  # "Maximizar" o "Minimizar"
    except ValueError:
        raise ValueError("Ingrese valores numéricos válidos en la Función Objetivo.")
    
    # Obtener restricciones
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
        raise ValueError("No hay restricciones definidas. Pulse 'Generar' primero.")
    
    # Agregar restricciones de no negatividad (X1 >= 0, X2 >= 0)
    restricciones_completas = restricciones + [(1, 0, ">=", 0), (0, 1, ">=", 0)]
    lineas = [(a, b, c) for a, b, op, c in restricciones_completas]
    
    # Calcular intersecciones entre todas las rectas
    puntos = []
    n = len(lineas)
    for i in range(n):
        for j in range(i + 1, n):
            a1, b1, c1_l = lineas[i]
            a2, b2, c2_l = lineas[j]
            det = (a1 * b2) - (a2 * b1)
            
            # Si el determinante no es cero, las líneas no son paralelas
            if abs(det) > 1e-5:
                # Calcular punto de intersección
                x = (c1_l * b2 - c2_l * b1) / det
                y = (a1 * c2_l - a2 * c1_l) / det
                # Validar que estén en el primer cuadrante o cerca de él
                if x >= -1e-5 and y >= -1e-5:
                    puntos.append((round(max(0, x), 4), round(max(0, y), 4)))
    
    # Verificar cuáles puntos son factibles (cumplen todas las restricciones)
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
    
    # Verificar si existe región factible
    if not puntos_factibles:
        raise ValueError("No se encontró una región factible que cumpla todas las restricciones.")
    
    # Encontrar el punto óptimo evaluando la función objetivo
    mejor_punto = None
    mejor_z = None
    
    for px, py in puntos_factibles:
        z = c1 * px + c2 * py
        if mejor_z is None:
            mejor_punto = (px, py)
            mejor_z = z
        else:
            if tipo_opt == "Maximizar" and z > mejor_z:
                mejor_z = z
                mejor_punto = (px, py)
            elif tipo_opt == "Minimizar" and z < mejor_z:
                mejor_z = z
                mejor_punto = (px, py)
    
    # Obtener nombres de las variables
    nombre_v1 = panel_entrada.entry_nombre1.get().strip() or "X1"
    nombre_v2 = panel_entrada.entry_nombre2.get().strip() or "X2"
    
    return {
        "tipo_opt": tipo_opt,
        "restricciones": restricciones,
        "puntos_factibles": puntos_factibles,
        "mejor_punto": mejor_punto,
        "mejor_z": mejor_z,
        "nombre_v1": nombre_v1,
        "nombre_v2": nombre_v2
    }
