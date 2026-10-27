from tkinter import *
from tkinter import messagebox
from logica_metodo_grafico import resolver_modelo_grafico

def obtener_limites_canvas(canvas):
    canvas.update_idletasks()
    ancho = canvas.winfo_width()
    if ancho < 10: ancho = 800
    alto = canvas.winfo_height()
    if alto < 10: alto = 600
    return ancho, alto

def calcular_escala_y_origen(restricciones, puntos_factibles, ancho_canvas, alto_canvas):
    # Encontrar el valor máximo en X y Y entre los puntos factibles y los interceptos con los ejes
    max_x = 10.0
    max_y = 10.0

    for px, py in puntos_factibles:
        max_x = max(max_x, px)
        max_y = max(max_y, py)

    for a, b, op, c in restricciones:
        if a != 0: max_x = max(max_x, abs(c / a))
        if b != 0: max_y = max(max_y, abs(c / b))

    # Dejar un margen del 20% alrededor del gráfico
    max_x *= 1.25
    max_y *= 1.25

    # Calcular escala de píxeles por unidad para que encaje en el canvas dejando un padding de 50px
    margen = 50
    escala_x = (ancho_canvas - 2 * margen) / max(max_x, 1.0)
    escala_y = (alto_canvas - 2 * margen) / max(max_y, 1.0)
    
    # Usar la misma escala para X e Y para no distorsionar las proporciones geométricas
    escala = min(escala_x, escala_y)
    escala = max(escala, 1.0) # Escala mínima de seguridad

    # El origen (0,0) estará abajo a la izquierda con un pequeño margen
    origen_x = margen
    origen_y = alto_canvas - margen

    return escala, origen_x, origen_y

def convertir_coordenadas(x, y, origen_x, origen_y, escala):
    pixel_x = origen_x + (x * escala)
    pixel_y = origen_y - (y * escala)
    return pixel_x, pixel_y

def crear_plano(canvas, restricciones, puntos_factibles):
    ancho, alto = obtener_limites_canvas(canvas)
    canvas.delete("all")

    escala, origen_x, origen_y = calcular_escala_y_origen(restricciones, puntos_factibles, ancho, alto)

    # Dibujar cuadrícula de referencia
    paso_logico = max(1, int(100 / escala))
    
    # Ejes principales
    canvas.create_line(origen_x, origen_y, ancho - 20, origen_y, fill="black", arrow=LAST, width=2)
    canvas.create_text(ancho - 10, origen_y + 15, text="X1", fill="black", font=("Arial", 11, "bold"))
    
    canvas.create_line(origen_x, origen_y, origen_x, 20, fill="black", arrow=LAST, width=2)
    canvas.create_text(origen_x - 15, 15, text="X2", fill="black", font=("Arial", 11, "bold"))

    return escala, origen_x, origen_y

def dibujar_restriccion(canvas, a, b, c, alto, ancho, origen_x, origen_y, escala, color="green"):
    # Encontrar puntos de corte con los ejes o fronteras del canvas visible
    x_max_visible = (ancho - origen_x) / escala
    y_max_visible = origen_y / escala

    puntos_linea = []

    if b == 0 and a != 0:
        x_val = c / a
        if 0 <= x_val <= x_max_visible * 2:
            p1 = convertir_coordenadas(x_val, 0, origen_x, origen_y, escala)
            p2 = convertir_coordenadas(x_val, y_max_visible * 2, origen_x, origen_y, escala)
            canvas.create_line(p1[0], p1[1], p2[0], p2[1], fill=color, width=2)
        return

    if a == 0 and b != 0:
        y_val = c / b
        if 0 <= y_val <= y_max_visible * 2:
            p1 = convertir_coordenadas(0, y_val, origen_x, origen_y, escala)
            p2 = convertir_coordenadas(x_max_visible * 2, y_val, origen_x, origen_y, escala)
            canvas.create_line(p1[0], p1[1], p2[0], p2[1], fill=color, width=2)
        return

    # Corte con eje X (cuando y = 0)
    if a != 0:
        x_corte = c / a
        if x_corte >= 0:
            puntos_linea.append(convertir_coordenadas(x_corte, 0, origen_x, origen_y, escala))

    # Corte con eje Y (cuando x = 0)
    if b != 0:
        y_corte = c / b
        if y_corte >= 0:
            puntos_linea.append(convertir_coordenadas(0, y_corte, origen_x, origen_y, escala))

    # Si cruza ambos ejes dentro del rango positivo
    if len(puntos_linea) == 2:
        canvas.create_line(puntos_linea[0][0], puntos_linea[0][1], puntos_linea[1][0], puntos_linea[1][1], fill=color, width=2)
    elif len(puntos_linea) == 1:
        # Extender hacia un punto aleatorio superior si la línea solo corta un eje
        p_extra = convertir_coordenadas(x_max_visible, max(0, (c - a * x_max_visible) / b), origen_x, origen_y, escala)
        canvas.create_line(puntos_linea[0][0], puntos_linea[0][1], p_extra[0], p_extra[1], fill=color, width=2)

def resolver_y_dibujar(canvas):
    ancho, alto = obtener_limites_canvas(canvas)
    
    try:
        resultado = resolver_modelo_grafico()
    except ValueError as e:
        messagebox.showerror("Error de validación", str(e))
        return

    restricciones = resultado["restricciones"]
    puntos_factibles = resultado["puntos_factibles"]

    # Crear plano con escala adaptativa basada en los datos reales del problema
    escala, origen_x, origen_y = crear_plano(canvas, restricciones, puntos_factibles)

    colores = ["green", "blue", "orange", "purple", "brown", "magenta"]

    # 1. Dibujar restricciones adaptadas
    for i, (a, b, op, c) in enumerate(restricciones):
        color = colores[i % len(colores)]
        dibujar_restriccion(canvas, a, b, c, alto, ancho, origen_x, origen_y, escala, color=color)

    estado = resultado["estado"]

    if estado == "Infactible":
        messagebox.showerror("Caso Especial Detectado", "¡El modelo es INFACTIBLE!\nNo existe ninguna región que cumpla todas las restricciones simultáneamente.")
        return

    if estado == "No Acotado":
        for px, py in puntos_factibles:
            cx, cy = convertir_coordenadas(px, py, origen_x, origen_y, escala)
            canvas.create_oval(cx - 3, cy - 3, cx + 3, cy + 3, fill="blue", outline="black")
        messagebox.showwarning("Caso Especial Detectado", "¡El modelo es NO ACOTADO!\nLa función objetivo puede crecer infinitamente sin violar las restricciones.")
        return

    # 2. Rellenar o marcar región factible y vértices
    for px, py in puntos_factibles:
        cx, cy = convertir_coordenadas(px, py, origen_x, origen_y, escala)
        canvas.create_oval(cx - 4, cy - 4, cx + 4, cy + 4, fill="blue", outline="black")

    puntos_optimos = resultado["puntos_optimos"]

    if estado == "Empate":
        if len(puntos_optimos) == 2:
            p1_x, p1_y = puntos_optimos[0]
            p2_x, p2_y = puntos_optimos[1]
            c1_x, c1_y = convertir_coordenadas(p1_x, p1_y, origen_x, origen_y, escala)
            c2_x, c2_y = convertir_coordenadas(p2_x, p2_y, origen_x, origen_y, escala)
            canvas.create_line(c1_x, c1_y, c2_x, c2_y, fill="red", width=4)

        for px, py in puntos_optimos:
            px_opt, py_opt = convertir_coordenadas(px, py, origen_x, origen_y, escala)
            canvas.create_oval(px_opt - 6, py_opt - 6, px_opt + 6, py_opt + 6, fill="red", outline="black", width=2)
            canvas.create_text(px_opt + 25, py_opt - 12, text=f"Óptimo ({px}, {py})", fill="red", font=("Arial", 9, "bold"))
        
        mensaje = f"¡Empate Detectado (Múltiples Soluciones Óptimas)!\n\nValor Óptimo (Z) = {round(resultado['mejor_z'], 4)}"
        messagebox.showinfo("Resultado - Método Gráfico", mensaje)

    else:
        opt_x, opt_y = puntos_optimos[0]
        px_opt, py_opt = convertir_coordenadas(opt_x, opt_y, origen_x, origen_y, escala)
        canvas.create_oval(px_opt - 6, py_opt - 6, px_opt + 6, py_opt + 6, fill="red", outline="black", width=2)
        canvas.create_text(px_opt + 25, py_opt - 12, text=f"Óptimo ({opt_x}, {opt_y})", fill="red", font=("Arial", 10, "bold"))

        mensaje = (
            f"¡Solución Óptima Única Encontrada ({resultado['tipo_opt']})!\n\n"
            f"• {resultado['nombre_v1']} = {opt_x}\n"
            f"• {resultado['nombre_v2']} = {opt_y}\n"
            f"• Valor Óptimo (Z) = {round(resultado['mejor_z'], 4)}"
        )
        messagebox.showinfo("Resultado - Método Gráfico", mensaje)