# Módulo para dibujo y visualización del plano cartesiano
# Método Gráfico - Investigación de Operaciones

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
    max_x = 10.0
    max_y = 10.0

    for px, py in puntos_factibles:
        max_x = max(max_x, px)
        max_y = max(max_y, py)

    for a, b, op, c in restricciones:
        if a != 0: max_x = max(max_x, abs(c / a))
        if b != 0: max_y = max(max_y, abs(c / b))

    max_x *= 1.25
    max_y *= 1.25

    margen = 50
    escala_x = (ancho_canvas - 2 * margen) / max(max_x, 1.0)
    escala_y = (alto_canvas - 2 * margen) / max(max_y, 1.0)
    
    escala = min(escala_x, escala_y)
    escala = max(escala, 1.0)

    origen_x = margen
    origen_y = alto_canvas - margen

    return escala, origen_x, origen_y

def convertir_coordenadas(x, y, origen_x, origen_y, escala):
    pixel_x = origen_x + (x * escala)
    pixel_y = origen_y - (y * escala)
    return pixel_x, pixel_y

def crear_plano(canvas, restricciones=None, puntos_factibles=None):
    """
    Crea el plano cartesiano con ejes, malla y etiquetas con escala adaptativa.
    """
    ancho, alto = obtener_limites_canvas(canvas)
    canvas.delete("all")
    
    if restricciones is None:
        restricciones = []
    if puntos_factibles is None:
        puntos_factibles = []
        
    escala, origen_x, origen_y = calcular_escala_y_origen(restricciones, puntos_factibles, ancho, alto)
    
    # Dibujar malla adaptativa
    paso_unidades = max(1, int(50 / escala))
    
    x_val = 0
    while True:
        px, _ = convertir_coordenadas(x_val, 0, origen_x, origen_y, escala)
        if px > ancho - 40:
            break
        if px >= origen_x:
            canvas.create_line(px, 0, px, alto, fill="#f0f0f0", tags="grid")
            if x_val > 0:
                canvas.create_text(px, origen_y + 12, text=str(x_val), fill="gray", font=("Arial", 7))
        x_val += paso_unidades

    y_val = 0
    while True:
        _, py = convertir_coordenadas(0, y_val, origen_x, origen_y, escala)
        if py < 40:
            break
        if py <= origen_y:
            canvas.create_line(0, py, ancho, py, fill="#f0f0f0", tags="grid")
            if y_val > 0:
                canvas.create_text(origen_x - 15, py, text=str(y_val), fill="gray", font=("Arial", 7))
        y_val += paso_unidades

    # Eje X
    canvas.create_line(origen_x, origen_y, ancho - 20, origen_y, fill="black", arrow=LAST, width=2)
    canvas.create_text(ancho - 10, origen_y + 15, text="X1", fill="black", font=("Arial", 10, "bold"))
    
    # Eje Y
    canvas.create_line(origen_x, origen_y, origen_x, 20, fill="black", arrow=LAST, width=2)
    canvas.create_text(origen_x - 15, 15, text="X2", fill="black", font=("Arial", 10, "bold"))
    
    return escala, origen_x, origen_y

def dibujar_restriccion(canvas, a, b, c, origen_x, origen_y, escala, color="green"):
    """
    Dibuja una recta de restricción en el plano cartesiano adaptada a la escala.
    """
    # Caso especial: restricción vertical (b == 0)
    if abs(b) < 1e-12 and abs(a) > 1e-12:
        x1 = c / a
        p1 = convertir_coordenadas(x1, -100, origen_x, origen_y, escala)
        p2 = convertir_coordenadas(x1, 1000, origen_x, origen_y, escala)
        canvas.create_line(p1[0], p1[1], p2[0], p2[1], fill=color, width=2)
        return
    
    # Caso especial: restricción horizontal (a == 0)
    if abs(a) < 1e-12 and abs(b) > 1e-12:
        y1 = c / b
        p1 = convertir_coordenadas(-100, y1, origen_x, origen_y, escala)
        p2 = convertir_coordenadas(1000, y1, origen_x, origen_y, escala)
        canvas.create_line(p1[0], p1[1], p2[0], p2[1], fill=color, width=2)
        return
    # Caso especial: recta pasa por el origen (c == 0)
    if abs(c) < 1e-12 and abs(a) > 1e-12 and abs(b) > 1e-12:
        # Dibujar recta que pasa por (0,0) en ambas direcciones
        p1 = convertir_coordenadas(0, 0, origen_x, origen_y, escala)
        # Dirección perpendicular para trazar la recta
        p2 = convertir_coordenadas(-b * 1000, a * 1000, origen_x, origen_y, escala)
        p3 = convertir_coordenadas(b * 1000, -a * 1000, origen_x, origen_y, escala)
        canvas.create_line(p2[0], p2[1], p3[0], p3[1], fill=color, width=2)
        return
    
    # Caso general: calcular intersecciones con ejes
    puntos_recta = []
    if abs(b) > 1e-12:
        y_corte = c / b
        puntos_recta.append((0, y_corte))
    if abs(a) > 1e-12:
        x_corte = c / a
        puntos_recta.append((x_corte, 0))
        
    if len(puntos_recta) >= 2:
        p1 = convertir_coordenadas(puntos_recta[0][0], puntos_recta[0][1], origen_x, origen_y, escala)
        p2 = convertir_coordenadas(puntos_recta[1][0], puntos_recta[1][1], origen_x, origen_y, escala)
        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]
        ext = 5.0
        p_ini = (p1[0] - dx * ext, p1[1] - dy * ext)
        p_fin = (p2[0] + dx * ext, p2[1] + dy * ext)
        canvas.create_line(p_ini[0], p_ini[1], p_fin[0], p_fin[1], fill=color, width=2)
    elif len(puntos_recta) == 1:
        x0, y0 = puntos_recta[0]
        p1 = convertir_coordenadas(x0, y0, origen_x, origen_y, escala)
        if abs(b) > 1e-12:
            p2 = convertir_coordenadas(x0 + 100, y0 - (a/b)*100, origen_x, origen_y, escala)
            canvas.create_line(p1[0], p1[1], p2[0], p2[1], fill=color, width=2)

def resolver_y_dibujar(canvas):
    """
    Resuelve el modelo, dibuja restricciones, región factible y óptimos,
    mostrando avisos claros para casos especiales (Infactible, No Acotado, Empate).
    """
    try:
        resultado = resolver_modelo_grafico()
    except ValueError as e:
        messagebox.showerror("Error de validación", str(e))
        return
    
    restricciones = resultado.get("restricciones", [])
    puntos_factibles = resultado.get("puntos_factibles", [])
    estado = resultado.get("estado", "")
    tipo_opt = resultado.get("tipo_opt", "")
    
    # Crear plano con escala adaptativa
    escala, origen_x, origen_y = crear_plano(canvas, restricciones, puntos_factibles)
    colores = ["green", "blue", "orange", "purple", "brown", "magenta"]
    
    # 1. Dibujar restricciones
    for i, (a, b, op, c) in enumerate(restricciones):
        color = colores[i % len(colores)]
        dibujar_restriccion(canvas, a, b, c, origen_x, origen_y, escala, color=color)
    
    # 2. Caso Infactible
    if estado == "Infactible":
        messagebox.showerror("Caso Especial Detectado", "¡El modelo es INFACTIBLE!\nNo existe ninguna región que cumpla todas las restricciones simultáneamente.")
        return

    # 3. Dibujar puntos factibles
    for px, py in puntos_factibles:
        cx, cy = convertir_coordenadas(px, py, origen_x, origen_y, escala)
        canvas.create_oval(cx - 3, cy - 3, cx + 3, cy + 3, fill="blue", outline="black")

    # 4. Caso No Acotado
    if estado == "No Acotado":
        messagebox.showwarning("Caso Especial Detectado", "¡El modelo es NO ACOTADO!\nLa función objetivo puede crecer infinitamente sin violar las restricciones.")
        return

    puntos_optimos = resultado.get("puntos_optimos", [])
    mejor_z = resultado.get("mejor_z", 0)
    nombre_v1 = resultado.get("nombre_v1", "X1")
    nombre_v2 = resultado.get("nombre_v2", "X2")

    # 5. Caso Empate (Múltiples óptimos)
    if estado == "Empate":
        if len(puntos_optimos) >= 2:
            p1_x, p1_y = puntos_optimos[0]
            p2_x, p2_y = puntos_optimos[-1]
            c1_x, c1_y = convertir_coordenadas(p1_x, p1_y, origen_x, origen_y, escala)
            c2_x, c2_y = convertir_coordenadas(p2_x, p2_y, origen_x, origen_y, escala)
            canvas.create_line(c1_x, c1_y, c2_x, c2_y, fill="red", width=4)

        for px, py in puntos_optimos:
            px_opt, py_opt = convertir_coordenadas(px, py, origen_x, origen_y, escala)
            canvas.create_oval(px_opt - 6, py_opt - 6, px_opt + 6, py_opt + 6, fill="red", outline="black", width=2)
            canvas.create_text(px_opt + 30, py_opt - 12, text=f"Óptimo ({px}, {py})", fill="red", font=("Arial", 9, "bold"))
        
        mensaje = f"¡Empate Detectado (Múltiples Soluciones Óptimas / Óptimos Alternativos)!\n\nValor Óptimo (Z) = {round(mejor_z, 4)}"
        messagebox.showinfo("Resultado - Método Gráfico", mensaje)

    # 6. Caso Solución Única
    elif estado == "Unica" and puntos_optimos:
        opt_x, opt_y = puntos_optimos[0]
        px_opt, py_opt = convertir_coordenadas(opt_x, opt_y, origen_x, origen_y, escala)
        canvas.create_oval(px_opt - 6, py_opt - 6, px_opt + 6, py_opt + 6, fill="red", outline="black", width=2)
        canvas.create_text(px_opt + 30, py_opt - 12, text=f"Óptimo ({opt_x}, {opt_y})", fill="red", font=("Arial", 10, "bold"))

        mensaje = (
            f"¡Solución Óptima Única Encontrada ({tipo_opt})!\n\n"
            f"• {nombre_v1} = {opt_x}\n"
            f"• {nombre_v2} = {opt_y}\n"
            f"• Valor Óptimo (Z) = {round(mejor_z, 4)}"
        )
        messagebox.showinfo("Resultado - Método Gráfico", mensaje)