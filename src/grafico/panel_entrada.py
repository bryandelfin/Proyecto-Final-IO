# Importación de módulos necesarios
from tkinter import *
from tkinter import ttk, messagebox
import sys, os

# Configuración de rutas para importar módulos locales
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from logica_restricciones import crear_restricciones_dinamicas, entradas_restricciones
from plano_cartesiano import resolver_y_dibujar, crear_plano
from ejemplos import EJEMPLOS

# Variable global para mantener referencia a la ventana principal
root = Tk()

def limpiar_todo(canvas_widget, frame_contenedor):
    """
    Limpia todos los campos de entrada, resetea las restricciones y limpia el canvas.
    
    Args:
        canvas_widget: Widget Canvas donde se dibuja el plano cartesiano
        frame_contenedor: Frame que contiene las restricciones dinámicas
    """
    # Limpiar campos de función objetivo
    entry_nombre1.delete(0, END)
    entry_valor1.delete(0, END)
    entry_nombre2.delete(0, END)
    entry_valor2.delete(0, END)
    
    # Resetear comboboxes
    comboOp.set("Maximizar")
    combo_restricciones.set("1")
    
    # Limpiar canvas y volver a dibujar plano
    canvas_widget.delete("all")
    crear_plano(canvas_widget)
    
    # Limpiar contenedor de restricciones
    for widget in frame_contenedor.winfo_children():
        widget.destroy()
    
    # Limpiar lista de entradas de restricciones
    entradas_restricciones.clear()

def cargar_ejemplo_seleccionado(canvas_widget, frame_contenedor):
    """
    Carga el ejemplo seleccionado en el combobox de ejemplos.
    Limpia todo, llena los campos, genera restricciones y resuelve automáticamente.
    
    Args:
        canvas_widget: Widget Canvas donde se dibuja el plano cartesiano
        frame_contenedor: Frame que contiene las restricciones dinámicas
    """
    try:
        # Obtener índice del ejemplo seleccionado
        seleccion = combo_ejemplos.current()
        if seleccion < 0 or seleccion >= len(EJEMPLOS):
            messagebox.showwarning("Advertencia", "Seleccione un ejemplo válido")
            return
        
        ejemplo = EJEMPLOS[seleccion]
        
        # Limpiar todo primero
        limpiar_todo(canvas_widget, frame_contenedor)
        
        # Llenar función objetivo
        comboOp.set(ejemplo["tipo_opt"])
        entry_nombre1.insert(0, ejemplo["x1_nombre"])
        entry_valor1.insert(0, str(ejemplo["x1_valor"]))
        entry_nombre2.insert(0, ejemplo["x2_nombre"])
        entry_valor2.insert(0, str(ejemplo["x2_valor"]))
        
        # Generar restricciones
        num_restricciones = len(ejemplo["restricciones"])
        combo_restricciones.set(str(num_restricciones))
        crear_restricciones_dinamicas(frame_contenedor, combo_restricciones)
        
        # Rellenar valores de las restricciones
        for i, restriccion in enumerate(ejemplo["restricciones"]):
            if i < len(entradas_restricciones):
                a, b, op, c = restriccion
                entry_v1, entry_v2, combo_des, entry_c = entradas_restricciones[i]
                entry_v1.delete(0, END)
                entry_v1.insert(0, str(a))
                entry_v2.delete(0, END)
                entry_v2.insert(0, str(b))
                combo_des.set(op)
                entry_c.delete(0, END)
                entry_c.insert(0, str(c))
        
        # Resolver y dibujar automáticamente
        resolver_y_dibujar(canvas_widget)
        
    except Exception as e:
        messagebox.showerror("Error", f"Error al cargar ejemplo: {str(e)}")

# Configuración de la ventana principal
root.title("Método Gráfico")
root.geometry("1200x650")
root.resizable(True, True)

# Configuración de grid
root.columnconfigure(0, weight=0)
root.columnconfigure(1, weight=3)
root.rowconfigure(0, weight=1)

# Frame izquierdo - Panel de entrada (más compacto)
frame_izq = ttk.LabelFrame(root, text="Modelo Matemático", padding=6)
frame_izq.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)
frame_izq.columnconfigure(1, weight=1)

# Canvas para el plano cartesiano
canvas = Canvas(root, bg="white", highlightthickness=1, highlightbackground="gray")
canvas.grid(row=0, column=1, sticky="nsew", padx=2, pady=2)

# Encabezado
label_titulo = Label(frame_izq, text="Gestión de Ganancias", font=("Arial", 8, "bold"))
label_titulo.grid(row=0, column=0, columnspan=2, pady=2)

# Separador
separador1 = ttk.Separator(frame_izq, orient="horizontal")
separador1.grid(row=1, column=0, columnspan=2, sticky="ew", pady=4)

# Función Objetivo
label_objetivo_titulo = Label(frame_izq, text="Función Objetivo", font=("Arial", 8, "bold"))
label_objetivo_titulo.grid(row=2, column=0, columnspan=2, pady=2)

# Tipo de optimización
label_objetivo = Label(frame_izq, text="Objetivo:", font=("Arial", 8))
label_objetivo.grid(row=3, column=0, sticky="w", padx=2, pady=1)
comboOp = ttk.Combobox(frame_izq, values=["Maximizar", "Minimizar"], state="readonly", width=12)
comboOp.grid(row=3, column=1, sticky="ew", padx=2, pady=1)
comboOp.set("Maximizar")

# Variable 1
label_var1 = Label(frame_izq, text="Variable 1", font=("Arial", 8, "bold"))
label_var1.grid(row=4, column=0, columnspan=2, pady=2)
label_nombre1 = Label(frame_izq, text="Nombre:", font=("Arial", 8))
label_nombre1.grid(row=5, column=0, sticky="w", padx=2, pady=1)
entry_nombre1 = Entry(frame_izq, width=12)
entry_nombre1.grid(row=5, column=1, sticky="ew", padx=2, pady=1)
label_valor1 = Label(frame_izq, text="Valor:", font=("Arial", 8))
label_valor1.grid(row=6, column=0, sticky="w", padx=2, pady=1)
entry_valor1 = Entry(frame_izq, width=12)
entry_valor1.grid(row=6, column=1, sticky="ew", padx=2, pady=1)

# Variable 2
label_var2 = Label(frame_izq, text="Variable 2", font=("Arial", 8, "bold"))
label_var2.grid(row=7, column=0, columnspan=2, pady=2)
label_nombre2 = Label(frame_izq, text="Nombre:", font=("Arial", 8))
label_nombre2.grid(row=8, column=0, sticky="w", padx=2, pady=1)
entry_nombre2 = Entry(frame_izq, width=12)
entry_nombre2.grid(row=8, column=1, sticky="ew", padx=2, pady=1)
label_valor2 = Label(frame_izq, text="Valor:", font=("Arial", 8))
label_valor2.grid(row=9, column=0, sticky="w", padx=2, pady=1)
entry_valor2 = Entry(frame_izq, width=12)
entry_valor2.grid(row=9, column=1, sticky="ew", padx=2, pady=1)

# Separador
separador2 = ttk.Separator(frame_izq, orient="horizontal")
separador2.grid(row=10, column=0, columnspan=2, sticky="ew", pady=4)

# Restricciones
label_restricciones_titulo = Label(frame_izq, text="Restricciones", font=("Arial", 8, "bold"))
label_restricciones_titulo.grid(row=11, column=0, columnspan=2, pady=2)
label_num_restr = Label(frame_izq, text="No. Restr.:", font=("Arial", 8))
label_num_restr.grid(row=12, column=0, sticky="w", padx=2, pady=1)
combo_restricciones = ttk.Combobox(frame_izq, values=["1","2","3","4","5","6","7","8"], state="readonly", width=12)
combo_restricciones.grid(row=12, column=1, sticky="ew", padx=2, pady=1)
combo_restricciones.set("1")
buttonGenerar = ttk.Button(frame_izq, text="Generar", command=lambda: crear_restricciones_dinamicas(frame_contenedor_restricciones, combo_restricciones))
buttonGenerar.grid(row=13, column=0, columnspan=2, sticky="ew", padx=2, pady=1)

# Contenedor de restricciones
frame_contenedor_restricciones = ttk.LabelFrame(frame_izq, text="", padding=2)
frame_contenedor_restricciones.grid(row=14, column=0, columnspan=2, sticky="ew", pady=2)

# Separador
separador3 = ttk.Separator(frame_izq, orient="horizontal")
separador3.grid(row=15, column=0, columnspan=2, sticky="ew", pady=4)

# Ejemplos
label_ejemplos = Label(frame_izq, text="Ejemplos", font=("Arial", 8, "bold"))
label_ejemplos.grid(row=16, column=0, columnspan=2, pady=2)
combo_ejemplos = ttk.Combobox(frame_izq, values=[e["nombre"] for e in EJEMPLOS], state="readonly", width=25)
combo_ejemplos.grid(row=17, column=0, columnspan=2, sticky="ew", padx=2, pady=1)
combo_ejemplos.current(0)
buttonCargarEjemplo = ttk.Button(frame_izq, text="Cargar Ejemplo", command=lambda: cargar_ejemplo_seleccionado(canvas, frame_contenedor_restricciones))
buttonCargarEjemplo.grid(row=18, column=0, columnspan=2, sticky="ew", padx=2, pady=1)

# Separador
separador4 = ttk.Separator(frame_izq, orient="horizontal")
separador4.grid(row=19, column=0, columnspan=2, sticky="ew", pady=4)

# Botones de acción
buttonResolver = ttk.Button(frame_izq, text="Resolver", command=lambda: resolver_y_dibujar(canvas))
buttonResolver.grid(row=20, column=0, sticky="ew", padx=1, pady=1)
buttonLimpiar = ttk.Button(frame_izq, text="Limpiar", command=lambda: limpiar_todo(canvas, frame_contenedor_restricciones))
buttonLimpiar.grid(row=20, column=1, sticky="ew", padx=1, pady=1)

# Inicializar plano cartesiano
crear_plano(canvas)

# Iniciar aplicación
if __name__ == "__main__":
    root.mainloop()
