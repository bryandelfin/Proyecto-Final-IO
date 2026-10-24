from tkinter import *
from tkinter import ttk

root = Tk()
root.title("Metodo grafico")
root.geometry("1300x600")

root.columnconfigure(0, weight=1) 
root.columnconfigure(1, weight=3)
root.rowconfigure(0, weight=3)  
root.rowconfigure(1, weight=1)

frame_izq = ttk.LabelFrame(root, text="Modelo Matematico", padding=10)
frame_izq.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

#Canvas
canvas =Canvas(root, bg="white")
canvas.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
#Encabezado
label = Label(frame_izq, text="Gestión de Ganancias")
label.grid(row=0, column=1)
# division
separador = ttk.Separator(frame_izq, orient="horizontal")
separador.grid(row=2, column=0, columnspan=2, sticky="ew", pady=10)
label = Label(frame_izq, text="Funcion Objetivo")
label.grid(row=3, column=1)

#Eleccion de tipo de optimizacion
label = Label(frame_izq, text="Objetivo")
label.grid(row=4, column=0)
combo = ttk.Combobox(frame_izq, values=["Maximizar", "Minimizar"])  
combo.grid(row=4, column=1)
#Variable 1 con entradas de nombre y valor
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
#Variable 2 con entradas de nombre y valor
label = Label(frame_izq, text="Variable 2")
label.grid(row=8, column=1)
label = Label(frame_izq, text="Nombre:")
label.grid(row=9, column=0)
entry_nombre2 = Entry(frame_izq)
entry_nombre2.grid(row=9, column=1)
label = Label(frame_izq, text="Valor:")
label.grid(row=10, column=0)
entry_valor2 = Entry(frame_izq )
entry_valor2.grid(row=10, column=1)
# division
separador = ttk.Separator(frame_izq, orient="horizontal")
separador.grid(row=11, column=0, columnspan=2, sticky="ew", pady=10)
#Restricciones
label = Label(frame_izq, text="Restricciones")
label.grid(row=14, column=1)
label = Label(frame_izq, text="No. Restricciones")
label.grid(row=16, column=0)
combo = ttk.Combobox(frame_izq, values=["1","2","3","4","5","6","7","8"])
combo.grid(row=16, column=1)
buttonGenerar = Button(frame_izq, text="Generar")
buttonGenerar.grid(row=17, column=1)
# division
separador = ttk.Separator(frame_izq, orient="horizontal")
separador.grid(row=18, column=0, columnspan=2, sticky="ew", pady=10)
#Botones
buttonResolver = Button(frame_izq, text="Resolver")
buttonResolver.grid(row=19, column=1)
buttonLimpiar = Button(frame_izq, text="Limpiar")
buttonLimpiar.grid(row=26, column=1)
buttonCargarEjemplo = Button(frame_izq, text="Cargar Ejemplo")
buttonCargarEjemplo.grid(row=27, column=1)
root.mainloop()