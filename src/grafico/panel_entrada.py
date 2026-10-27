from tkinter import *
from tkinter import ttk, messagebox
import sys, os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from logica_restricciones import crear_restricciones_dinamicas
from plano_cartesiano import resolver_y_dibujar

root = Tk()
root.title("Metodo grafico")
root.geometry("1300x600")

root.columnconfigure(0, weight=1) 
root.columnconfigure(1, weight=3)
root.rowconfigure(0, weight=3)  
root.rowconfigure(1, weight=1)

frame_izq = ttk.LabelFrame(root, text="Modelo Matematico", padding=10)
frame_izq.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

# Canvas
canvas = Canvas(root, bg="white")
canvas.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

# Encabezado
label = Label(frame_izq, text="Gestión de Ganancias")
label.grid(row=0, column=1)

separador = ttk.Separator(frame_izq, orient="horizontal")
separador.grid(row=2, column=0, columnspan=2, sticky="ew", pady=10)

label = Label(frame_izq, text="Funcion Objetivo")
label.grid(row=3, column=1)

# Eleccion de tipo de optimizacion
label = Label(frame_izq, text="Objetivo")
label.grid(row=4, column=0)
combo = ttk.Combobox(frame_izq, values=["Maximizar", "Minimizar"], state="readonly")  
combo.grid(row=4, column=1)
combo.set("Maximizar")

# Variable 1
label = Label(frame_izq, text="Variable 1")
label.grid(row=5, column=1)
label = Label(frame_izq, text="Nombre:")
label.grid(row=6, column=0)
entry_nombre1 = Entry(frame_izq)
entry_nombre1.grid(row=6, column=1)
label = Label(frame_izq, text="Valor:")
label.grid(row=7, column=0)
entry_valor1 = Entry(frame_izq)
entry_valor1.grid(row=7, column=1)

# Variable 2
label = Label(frame_izq, text="Variable 2")
label.grid(row=8, column=1)
label = Label(frame_izq, text="Nombre:")
label.grid(row=9, column=0)
entry_nombre2 = Entry(frame_izq)
entry_nombre2.grid(row=9, column=1)
label = Label(frame_izq, text="Valor:")
label.grid(row=10, column=0)
entry_valor2 = Entry(frame_izq)
entry_valor2.grid(row=10, column=1)

separador = ttk.Separator(frame_izq, orient="horizontal")
separador.grid(row=11, column=0, columnspan=2, sticky="ew", pady=10)

# Restricciones
label = Label(frame_izq, text="Restricciones")
label.grid(row=14, column=1)
label = Label(frame_izq, text="No. Restricciones")
label.grid(row=16, column=0)
combo_restricciones = ttk.Combobox(frame_izq, values=["1","2","3","4","5","6","7","8"], state="readonly")
combo_restricciones.grid(row=16, column=1)
combo_restricciones.set("1")

buttonGenerar = Button(frame_izq, text="Generar", command=lambda: crear_restricciones_dinamicas(frame_contenedor_restricciones, combo_restricciones))
buttonGenerar.grid(row=17, column=1)

# Contenedor de restricciones
frame_contenedor_restricciones = ttk.LabelFrame(frame_izq)
frame_contenedor_restricciones.grid(row=18, column=0, columnspan=2, sticky="ew", pady=10)

separador = ttk.Separator(frame_izq, orient="horizontal")
separador.grid(row=19, column=0, columnspan=2, sticky="ew", pady=5)

# --- Funciones para Limpiar y Cargar Ejemplos ---
def limpiar_campos():
    entry_nombre1.delete(0, END)
    entry_valor1.delete(0, END)
    entry_nombre2.delete(0, END)
    entry_valor2.delete(0, END)
    combo.set("Maximizar")
    combo_restricciones.set("1")
    for widget in frame_contenedor_restricciones.winfo_children():
        widget.destroy()
    from logica_restricciones import entradas_restricciones
    entradas_restricciones.clear()
    canvas.delete("all")

contador_ejemplo = 0

def cargar_ejemplo():
    global contador_ejemplo
    limpiar_campos()
    
    if contador_ejemplo % 3 == 0:
        combo.set("Maximizar")
        entry_nombre1.insert(0, "Café Privada")
        entry_valor1.insert(0, "0.80")
        entry_nombre2.insert(0, "Café Propia")
        entry_valor2.insert(0, "1.20")
        
        combo_restricciones.set("4")
        crear_restricciones_dinamicas(frame_contenedor_restricciones, combo_restricciones)
        
        from logica_restricciones import entradas_restricciones
        datos_ej1 = [
            ("1.19", "1.19", "<=", "500"),
            ("0.42", "0.50", "<=", "208"),
            ("0.33", "0.42", "<=", "208"),
            ("1.0", "0.0", "<=", "300")
        ]
        for idx, (v1, v2, op, ld) in enumerate(datos_ej1):
            entradas_restricciones[idx][0].insert(0, v1)
            entradas_restricciones[idx][1].insert(0, v2)
            entradas_restricciones[idx][2].set(op)
            entradas_restricciones[idx][3].insert(0, ld)
        messagebox.showinfo("Ejemplo Cargado", "Se cargó el Problema 1: Producción de Café.")

    elif contador_ejemplo % 3 == 1:
        combo.set("Maximizar")
        entry_nombre1.insert(0, "X1")
        entry_valor1.insert(0, "3")
        entry_nombre2.insert(0, "X2")
        entry_valor2.insert(0, "5")
        
        combo_restricciones.set("2")
        crear_restricciones_dinamicas(frame_contenedor_restricciones, combo_restricciones)
        
        from logica_restricciones import entradas_restricciones
        datos_ej2 = [
            ("1", "1", "<=", "4"),
            ("1", "1", ">=", "8")
        ]
        for idx, (v1, v2, op, ld) in enumerate(datos_ej2):
            entradas_restricciones[idx][0].insert(0, v1)
            entradas_restricciones[idx][1].insert(0, v2)
            entradas_restricciones[idx][2].set(op)
            entradas_restricciones[idx][3].insert(0, ld)
        messagebox.showinfo("Ejemplo Cargado", "Se cargó un caso de estudio: INFACTIBLE.")

    else:
        combo.set("Maximizar")
        entry_nombre1.insert(0, "X1")
        entry_valor1.insert(0, "2")
        entry_nombre2.insert(0, "X2")
        entry_valor2.insert(0, "1")
        
        combo_restricciones.set("2")
        crear_restricciones_dinamicas(frame_contenedor_restricciones, combo_restricciones)
        
        from logica_restricciones import entradas_restricciones
        datos_ej3 = [
            ("-1", "1", "<=", "2"),
            ("0", "1", ">=", "3")
        ]
        for idx, (v1, v2, op, ld) in enumerate(datos_ej3):
            entradas_restricciones[idx][0].insert(0, v1)
            entradas_restricciones[idx][1].insert(0, v2)
            entradas_restricciones[idx][2].set(op)
            entradas_restricciones[idx][3].insert(0, ld)
        messagebox.showinfo("Ejemplo Cargado", "Se cargó un caso de estudio: NO ACOTADO.")

    contador_ejemplo += 1

# --- Botones ---
buttonResolver = Button(frame_izq, text="Resolver", command=lambda: resolver_y_dibujar(canvas))
buttonResolver.grid(row=26, column=0)

buttonLimpiar = Button(frame_izq, text="Limpiar", command=limpiar_campos)
buttonLimpiar.grid(row=26, column=1)

buttonCargarEjemplo = Button(frame_izq, text="Cargar Ejemplo", command=cargar_ejemplo)
buttonCargarEjemplo.grid(row=26, column=2)

root.mainloop()