# Módulo para dibujo y visualización del plano cartesiano
# Método Gráfico - Investigación de Operaciones

from tkinter import *
from tkinter import messagebox
from logica_metodo_grafico import resolver_modelo_grafico

def convertir_coordenadas(x, y, alto, ancho, escala=30):
    """
    Convierte coordenadas cartesianas (x,y) a coordenadas de píxeles en el canvas.
    
    Args:
        x: Coordenada X en el plano cartesiano
        y: Coordenada Y en el plano cartesiano
        alto: Altura del canvas
        ancho: Ancho del canvas
        escala: Factor de escala (píxeles por unidad)
    
    Returns:
        tuple: (pixel_x, pixel_y)
    """
    origen_x = 40
    origen_y = alto - 40
    
    pixel_x = origen_x + (x * escala)
    pixel_y = origen_y - (y * escala)
    return pixel_x, pixel_y

def crear_plano(canvas):
    """
    Crea el plano cartesiano con ejes, malla y etiquetas.
    
    Args:
        canvas: Widget Canvas donde se dibujará el plano
    """
    canvas.update_idletasks()
    ancho = canvas.winfo_width() or 800
    alto = canvas.winfo_height() or 600
    canvas.delete("all")
    escala = 30
    
    # Dibujar malla
    for x in range(0, ancho, escala):
        canvas.create_line(x, 0, x, alto, fill="lightgray", tags="grid")
    
    for y in range(0, alto, escala):
        canvas.create_line(0, y, ancho, y, fill="lightgray", tags="grid")
    
    origen_x = 40
    origen_y = alto - 40
    
    # Dibujar eje X
    canvas.create_line(origen_x, origen_y, ancho, origen_y, fill="black", arrow=LAST, width=2)
    canvas.create_text(ancho - 10, origen_y + 10, text="X1", fill="black", font=("Arial", 12, "bold"))
    
    # Dibujar eje Y
    canvas.create_line(origen_x, origen_y, origen_x, 0, fill="black", arrow=LAST, width=2)
    canvas.create_text(origen_x - 10, 10, text="X2", fill="black", font=("Arial", 12, "bold"))

def dibujar_restriccion(canvas, a, b, c, color="green"):
    """
    Dibuja una recta de restricción en el plano cartesiano.
    
    Args:
        canvas: Widget Canvas donde se dibujará
        a: Coeficiente de X1
        b: Coeficiente de X2
        c: Lado derecho de la restricción
        color: Color de la recta
    """
    canvas.update_idletasks()
    ancho = canvas.winfo_width() or 800
    alto = canvas.winfo_height() or 600
    escala = 30
    
    # Caso especial: restricción vertical (b == 0)
    if abs(b) < 1e-12 and abs(a) > 1e-12:
        x1 = c / a
        p1 = convertir_coordenadas(x1, 0, alto, ancho, escala)
        p2 = convertir_coordenadas(x1, 1000, alto, ancho, escala)
        canvas.create_line(p1[0], p1[1], p2[0], p2[1], fill=color, width=2)
        return
    
    # Caso especial: restricción horizontal (a == 0)
    if abs(a) < 1e-12 and abs(b) > 1e-12:
        y1 = c / b
        p1 = convertir_coordenadas(0, y1, alto, ancho, escala)
        p2 = convertir_coordenadas(1000, y1, alto, ancho, escala)
        canvas.create_line(p1[0], p1[1], p2[0], p2[1], fill=color, width=2)
        return
    
    # Caso especial: recta pasa por el origen (c == 0)
    if abs(c) < 1e-12 and abs(a) > 1e-12 and abs(b) > 1e-12:
        # Dibujar recta que pasa por (0,0) en ambas direcciones
        p1 = convertir_coordenadas(0, 0, alto, ancho, escala)
        # Dirección perpendicular para trazar la recta
        p2 = convertir_coordenadas(-b * 1000, a * 1000, alto, ancho, escala)
        p3 = convertir_coordenadas(b * 1000, -a * 1000, alto, ancho, escala)
        canvas.create_line(p2[0], p2[1], p3[0], p3[1], fill=color, width=2)
        return
    
    # Caso general: calcular intersecciones con ejes
    if abs(b) > 1e-12 and abs(a) > 1e-12:
        corte_y = c / b
        corte_x = c / a
        punto_inicio = convertir_coordenadas(0, corte_y, alto, ancho, escala)
        punto_final = convertir_coordenadas(corte_x, 0, alto, ancho, escala)
        canvas.create_line(punto_inicio[0], punto_inicio[1], punto_final[0], punto_final[1], fill=color, width=2)
        return


def resolver_y_dibujar(canvas):
    """
    Resuelve el modelo, dibuja las restricciones, puntos factibles y solución óptima.
    
    Args:
        canvas: Widget Canvas donde se dibujará todo
    """
    # Crear plano cartesiano limpio
    crear_plano(canvas)
    
    try:
        # Resolver modelo
        resultado = resolver_modelo_grafico()
    except ValueError as e:
        messagebox.showerror("Error de validación", str(e))
        return
    
    ancho = canvas.winfo_width() or 800
    alto = canvas.winfo_height() or 600
    escala = 30
    colores = ["green", "blue", "red", "orange", "purple", "brown"]
    
    # Dibujar restricciones
    for i, (a, b, op, c) in enumerate(resultado["restricciones"]):
        color = colores[i % len(colores)]
        dibujar_restriccion(canvas, a, b, c, color=color)
    
    # Dibujar puntos factibles
    for px, py in resultado["puntos_factibles"]:
        cx, cy = convertir_coordenadas(px, py, alto, ancho, escala)
        canvas.create_oval(cx - 3, cy - 3, cx + 3, cy + 3, fill="blue", outline="black")
    
    # Dibujar punto óptimo
    opt_x, opt_y = resultado["mejor_punto"]
    px_opt, py_opt = convertir_coordenadas(opt_x, opt_y, alto, ancho, escala)
    
    radio = 6
    canvas.create_oval(px_opt - radio, py_opt - radio, px_opt + radio, py_opt + radio, 
                       fill="red", outline="black", width=2)
    canvas.create_text(px_opt + 25, py_opt - 12, 
                       text=f"Óptimo ({opt_x}, {opt_y})", 
                       fill="red", font=("Arial", 9, "bold"))
    
    # Mostrar resultado
    mensaje = (
        f"¡Solución Óptima Encontrada ({resultado['tipo_opt']})!\n\n"
        f"• {resultado['nombre_v1']} = {opt_x}\n"
        f"• {resultado['nombre_v2']} = {opt_y}\n"
        f"• Valor Óptimo (Z) = {round(resultado['mejor_z'], 4)}"
    )
    messagebox.showinfo("Resultado - Método Gráfico", mensaje)
