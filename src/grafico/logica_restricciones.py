from tkinter import Label, Entry
from tkinter import ttk

# Creamos una lista interna o la recibimos
entradas_restricciones = []

def crear_restricciones_dinamicas(frame_contenedor, combo_restricciones):
    global entradas_restricciones
    for widget in frame_contenedor.winfo_children():
        widget.destroy()
    entradas_restricciones.clear()
    try:
        num = int(combo_restricciones.get())
    except ValueError:
        return
    for i in range(num):
        label = Label(frame_contenedor, text=f"Restric. {i+1}:")
        label.grid(row=i, column=0, columnspan=2)
        entry_v1=Entry(frame_contenedor, width=5)
        entry_v1.grid(row=i, column=2)
        label=Label(frame_contenedor, text="X1 +")
        label.grid(row=i, column=3)
        entry_v2=Entry(frame_contenedor, width=5)
        entry_v2.grid(row=i, column=4)
        label=Label(frame_contenedor, text="X2")
        label.grid(row=i, column=5)
        combo_desigualdad = ttk.Combobox(frame_contenedor, values=["<=", ">=", "="], width=3, state="readonly")
        combo_desigualdad.grid(row=i, column=6)
        combo_desigualdad.set("<=")
        entry_lado_derecho=Entry(frame_contenedor, width=5)
        entry_lado_derecho.grid(row=i, column=7)
        entradas_restricciones.append((entry_v1, entry_v2, combo_desigualdad, entry_lado_derecho))