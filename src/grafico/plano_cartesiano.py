from tkinter import *
from tkinter import messagebox
from logica_metodo_grafico import resolver_modelo_grafico

def convertir_coordenadas(x, y, alto, ancho, escala=30):
    origen_x = 40
    origen_y = alto - 40
    pixel_x = origen_x + (x * escala)
    pixel_y = origen_y - (y * escala)
    return pixel_x, pixel_y

def crear_plano(canvas):
    canvas.update_idletasks()
    ancho = canvas.winfo_width() or 800
    alto = canvas.winfo_height() or 600
    canvas.delete("all")
    escala = 30 

    for x in range(0, ancho, escala):
        canvas.create_line(x, 0, x, alto, fill="lightgray", tags="grid")

    for y in range(0, alto, escala):
        canvas.create_line(0, y, ancho, y, fill="lightgray", tags="grid")

    origen_x = 40
    origen_y = alto - 40
    canvas.create_line(origen_x, origen_y, ancho, origen_y, fill="black", arrow=LAST, width=2)
    canvas.create_text(ancho - 10, origen_y + 10, text="X1", fill="black", font=("Arial", 12, "bold"))
    canvas.create_line(origen_x, origen_y, origen_x, 0, fill="black", arrow=LAST, width=2)
    canvas.create_text(origen_x - 10, 10, text="X2", fill="black", font=("Arial", 12, "bold"))

def dibujar_restriccion(canvas, a, b, c, color="green"):
    canvas.update_idletasks()
    ancho = canvas.winfo_width() or 800
    alto = canvas.winfo_height() or 600
    escala = 30

    if b == 0 and a != 0:
        x1 = c / a 
        p1 = convertir_coordenadas(x1, 0, alto, ancho, escala)
        p2 = convertir_coordenadas(x1, 1000, alto, ancho, escala)
        canvas.create_line(p1[0], p1[1], p2[0], p2[1], fill=color, width=2)
        return
    if a == 0 and b != 0:
        y1 = c / b 
        p1 = convertir_coordenadas(0, y1, alto, ancho, escala)
        p2 = convertir_coordenadas(1000, y1, alto, ancho, escala)
        canvas.create_line(p1[0], p1[1], p2[0], p2[1], fill=color, width=2)
        return
    
    corte_y = c / b
    corte_x = c / a
    punto_inicio = convertir_coordenadas(0, corte_y, alto, ancho, escala)
    punto_final = convertir_coordenadas(corte_x, 0, alto, ancho, escala)
    canvas.create_line(punto_inicio[0], punto_inicio[1], punto_final[0], punto_final[1], fill=color, width=2)

def resolver_y_dibujar(canvas):
    crear_plano(canvas)
    
    try:
        resultado = resolver_modelo_grafico()
    except ValueError as e:
        messagebox.showerror("Error de validación", str(e))
        return

    ancho = canvas.winfo_width() or 800
    alto = canvas.winfo_height() or 600
    escala = 30
    colores = ["green", "blue", "red", "orange", "purple", "brown"]

    # 1. Dibujar restricciones
    for i, (a, b, op, c) in enumerate(resultado["restricciones"]):
        color = colores[i % len(colores)]
        dibujar_restriccion(canvas, a, b, c, color=color)

    # 2. Dibujar vértices factibles generales
    for px, py in resultado["puntos_factibles"]:
        cx, cy = convertir_coordenadas(px, py, alto, ancho, escala)
        canvas.create_oval(cx - 3, cy - 3, cx + 3, cy + 3, fill="blue", outline="black")

    # 3. Manejo de solución única o empates (múltiples soluciones óptimas)
    puntos_optimos = resultado["puntos_optimos"]
    hay_empate = len(puntos_optimos) > 1

    if hay_empate:
        # Si hay empate entre 2 vértices, resaltar la línea que los conecta (segmento óptimo)
        if len(puntos_optimos) == 2:
            p1_x, p1_y = puntos_optimos[0]
            p2_x, p2_y = puntos_optimos[1]
            c1_x, c1_y = convertir_coordenadas(p1_x, p1_y, alto, ancho, escala)
            c2_x, c2_y = convertir_coordenadas(p2_x, p2_y, alto, ancho, escala)
            canvas.create_line(c1_x, c1_y, c2_x, c2_y, fill="red", width=4)

        # Destacar todos los vértices óptimos implicados
        for px, py in puntos_optimos:
            px_opt, py_opt = convertir_coordenadas(px, py, alto, ancho, escala)
            canvas.create_oval(px_opt - 6, py_opt - 6, px_opt + 6, py_opt + 6, fill="red", outline="black", width=2)
            canvas.create_text(px_opt + 20, py_opt - 12, text=f"Óptimo ({px}, {py})", fill="red", font=("Arial", 9, "bold"))
        
        mensaje = (
            f"¡Múltiples Soluciones Óptimas (Empate Detectado)!\n\n"
            f"Hay {len(puntos_optimos)} vértices óptimos que comparten el mismo valor de Z:\n"
        )
        for idx, (px, py) in enumerate(puntos_optimos, 1):
            mensaje += f"• Vértice {idx}: {resultado['nombre_v1']}={px}, {resultado['nombre_v2']}={py}\n"
        mensaje += f"\n• Valor Óptimo (Z) = {round(resultado['mejor_z'], 4)}\n"
        mensaje += "Cualquier punto en el segmento que los une también es solución óptima."
        
    else:
        # Solución óptima única
        opt_x, opt_y = puntos_optimos[0]
        px_opt, py_opt = convertir_coordenadas(opt_x, opt_y, alto, ancho, escala)
        
        canvas.create_oval(px_opt - 6, py_opt - 6, px_opt + 6, py_opt + 6, fill="red", outline="black", width=2)
        canvas.create_text(px_opt + 20, py_opt - 12, text=f"Óptimo ({opt_x}, {opt_y})", fill="red", font=("Arial", 10, "bold"))

        mensaje = (
            f"¡Solución Óptima Única Encontrada ({resultado['tipo_opt']})!\n\n"
            f"• {resultado['nombre_v1']} = {opt_x}\n"
            f"• {resultado['nombre_v2']} = {opt_y}\n"
            f"• Valor Óptimo (Z) = {round(resultado['mejor_z'], 4)}"
        )

    messagebox.showinfo("Resultado - Método Gráfico", mensaje)