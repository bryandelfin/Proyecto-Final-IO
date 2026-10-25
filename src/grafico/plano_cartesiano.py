from tkinter import *
from tkinter import messagebox
from logica_restricciones import entradas_restricciones

def convertir_coordenadas(x, y, alto, ancho, escala=30):
    origen_x = 40
    origen_y = alto - 40

    pixel_x = origen_x + (x * escala)
    pixel_y = origen_y - (y * escala)
    return pixel_x, pixel_y
def crear_plano(canvas):
    canvas.update_idletasks()  # para que el canvas tenga los tamaños correctos
    ancho=canvas.winfo_width() or 800
    alto=canvas.winfo_height() or 600
    canvas.delete("all")
    #cuadritos
    escala = 30 

    for x in range(0, ancho, escala):
        canvas.create_line(x, 0, x, alto, fill="lightgray", tags="grid")

    for y in range(0, alto, escala):
        canvas.create_line(0, y, ancho, y, fill="lightgray", tags="grid")

    origen_x = 40
    origen_y = alto - 40
    #Eje x
    canvas.create_line(origen_x, origen_y, ancho, origen_y,fill="black", arrow=LAST, width=2)
    canvas.create_text(ancho - 10, origen_y + 10, text="X1", fill="black", font=("Arial", 12, "bold"))
    #Eje y
    canvas.create_line(origen_x, origen_y, origen_x, 0, fill="black", arrow=LAST, width=2)
    canvas.create_text(origen_x - 10, 10, text="X2", fill="black", font=("Arial", 12, "bold"))
def dibujar_restricciones(canvas, a, b, c, color="green"):
    canvas.update_idletasks()  # para que el canvas tenga los tamaños correctos
    ancho = canvas.winfo_width() or 800
    alto = canvas.winfo_height() or 600
    escala = 30
    if c == 0:
        p1= convertir_coordenadas(0, 0, alto, ancho, escala)
        if a == 0 and b == 0:
            return
        if a == 0:
            p2= convertir_coordenadas(0, 1000, alto, ancho, escala)
            canvas.create_line(p1[0], p1[1], p2[0], p2[1], fill=color, width=2)
            return
        if b == 0:
            p2= convertir_coordenadas(1000, 0, alto, ancho, escala)
            canvas.create_line(p1[0], p1[1], p2[0], p2[1], fill=color, width=2)
            return
        else:
            x1_cualquiera = 500
            x2_cualquiera = (- a * x1_cualquiera) / b
            p2= convertir_coordenadas(x1_cualquiera, x2_cualquiera, alto, ancho, escala)

        
        canvas.create_line(p1[0], p1[1], p2[0], p2[1], fill=color, width=2)
        return
    else:
        #division entre 0
        if b == 0 and a != 0:
            x1 = c / a 
            p1= convertir_coordenadas(x1, 0, alto, ancho, escala)
            p2= convertir_coordenadas(x1, 1000, alto, ancho, escala)
            canvas.create_line(p1[0], p1[1], p2[0], p2[1], fill=color, width=2)
            return
        if a == 0 and b != 0:
            y1 = c / b 
            p1= convertir_coordenadas(0, y1, alto, ancho, escala)
            p2= convertir_coordenadas(1000, y1, alto, ancho, escala)
            canvas.create_line(p1[0], p1[1], p2[0], p2[1], fill=color, width=2)
            return
        
        corte_y= c / b
        corte_x= c / a

        punto_inicio= convertir_coordenadas(0, corte_y, alto, ancho, escala)
        punto_final= convertir_coordenadas(corte_x, 0, alto, ancho, escala)

        canvas.create_line(punto_inicio[0], punto_inicio[1], punto_final[0], punto_final[1], fill=color, width=2)

def resolver_y_dibujar(canvas):
    crear_plano(canvas)
    if not entradas_restricciones:
        messagebox.showwarning("Advertencia", "No hay restricciones definidas.", "Pulsa 'Generar' primero para crear las restricciones.")
        return
    colores = ["green", "blue", "red", "orange", "purple", "yellow"]
    for i, (entry_v1, entry_v2, combo_desigualdad, entry_lado_derecho) in enumerate(entradas_restricciones):
        try:
            a = float(entry_v1.get())
            b = float(entry_v2.get())
            c = float(entry_lado_derecho.get())
            color = colores[i % len(colores)]

            dibujar_restricciones(canvas, a, b, c, color=color)
        except ValueError:
            continue