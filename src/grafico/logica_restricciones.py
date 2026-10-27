# Módulo para generación dinámica de entradas de restricciones
# Método Gráfico - Investigación de Operaciones

from tkinter import Label, Entry
from tkinter import ttk

# Lista global para almacenar las entradas de restricciones dinámicamente
# Cada elemento es una tupla (entry_v1, entry_v2, combo_desigualdad, entry_lado_derecho)
entradas_restricciones = []

def crear_restricciones_dinamicas(frame_contenedor, combo_restricciones):
    """
    Crea dinámicamente los campos de entrada para las restricciones según el número seleccionado.
    
    Args:
        frame_contenedor: Frame donde se agregarán los campos de restricciones
        combo_restricciones: Combobox que contiene el número de restricciones a generar
    """
    global entradas_restricciones
    
    # Limpiar restricciones existentes
    for widget in frame_contenedor.winfo_children():
        widget.destroy()
    entradas_restricciones.clear()
    
    try:
        # Obtener número de restricciones
        num = int(combo_restricciones.get())
    except ValueError:
        return
    
    # Crear campos para cada restricción
    for i in range(num):
        # Etiqueta de restricción
        label_restr = Label(frame_contenedor, text=f"R{i+1}:", font=("Arial", 7))
        label_restr.grid(row=i, column=0, padx=1, pady=1)
        
        # Coeficiente de X1
        entry_v1 = Entry(frame_contenedor, width=4)
        entry_v1.grid(row=i, column=1, padx=1, pady=1)
        
        # Símbolo +
        label_x1 = Label(frame_contenedor, text="X1+", font=("Arial", 7))
        label_x1.grid(row=i, column=2, padx=1, pady=1)
        
        # Coeficiente de X2
        entry_v2 = Entry(frame_contenedor, width=4)
        entry_v2.grid(row=i, column=3, padx=1, pady=1)
        
        # Símbolo X2
        label_x2 = Label(frame_contenedor, text="X2", font=("Arial", 7))
        label_x2.grid(row=i, column=4, padx=1, pady=1)
        
        # Operador de desigualdad
        combo_desigualdad = ttk.Combobox(frame_contenedor, values=["<=", ">=", "="], width=3, state="readonly")
        combo_desigualdad.grid(row=i, column=5, padx=1, pady=1)
        combo_desigualdad.set("<=")
        
        # Lado derecho
        entry_lado_derecho = Entry(frame_contenedor, width=4)
        entry_lado_derecho.grid(row=i, column=6, padx=1, pady=1)
        
        # Guardar referencias
        entradas_restricciones.append((entry_v1, entry_v2, combo_desigualdad, entry_lado_derecho))
