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
    # Eje X
    canvas.create_line(origen_x, origen_y, ancho, origen_y, fill="black", arrow=LAST, width=2)
    canvas.create_text(ancho - 10, origen_y + 10, text="X1", fill="black", font=("Arial", 12, "bold"))
    # Eje Y
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

    
    for i, (a, b, op, c) in enumerate(resultado["restricciones"]):
        color = colores[i % len(colores)]
        dibujar_restriccion(canvas, a, b, c, color=color)

    
    for px, py in resultado["puntos_factibles"]:
        cx, cy = convertir_coordenadas(px, py, alto, ancho, escala)
        canvas.create_oval(cx - 3, cy - 3, cx + 3, cy + 3, fill="blue", outline="black")

    
    opt_x, opt_y = resultado["mejor_punto"]
    px_opt, py_opt = convertir_coordenadas(opt_x, opt_y, alto, ancho, escala)
    
    radio = 6
    canvas.create_oval(px_opt - radio, py_opt - radio, px_opt + radio, py_opt + radio, fill="red", outline="black", width=2)
    canvas.create_text(px_opt + 20, py_opt - 12, text=f"Óptimo ({opt_x}, {opt_y})", fill="red", font=("Arial", 10, "bold"))

    
    mensaje = (
        f"¡Solución Óptima Encontrada ({resultado['tipo_opt']})!\n\n"
        f"• {resultado['nombre_v1']} = {opt_x}\n"
        f"• {resultado['nombre_v2']} = {opt_y}\n"
        f"• Valor Óptimo (Z) = {round(resultado['mejor_z'], 4)}"
    )
    messagebox.showinfo("Resultado - Método Gráfico", mensaje)