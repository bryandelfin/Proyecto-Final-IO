# Importación de módulos necesarios
from tkinter import *
from tkinter import ttk, messagebox
from logica_programacion_dinamica import resolver_programacion_dinamica
from panel_tablas import PanelTablasDinamicas
import sys, os

# Configuración de rutas para importar módulos locales
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Variable global para mantener referencia a la ventana principal
root = Tk()

# Configuración de la ventana principal
root.title("Programación Dinámica - Modelo de Inventarios de Café")
root.geometry("1250x700")
root.resizable(True, True)

# Configuración de grid
root.columnconfigure(0, weight=0)
root.columnconfigure(1, weight=3)
root.rowconfigure(0, weight=1)

# Frame izquierdo - Panel de entrada con scroll
contenedor_izq = ttk.LabelFrame(root, text="Modelo de Programación Dinámica - Compras de Café", padding=0)
contenedor_izq.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)
contenedor_izq.columnconfigure(0, weight=1)
contenedor_izq.rowconfigure(0, weight=1)

canvas_form = Canvas(contenedor_izq, bg="#F7F5EF", highlightthickness=0)
scroll_form = ttk.Scrollbar(contenedor_izq, orient="vertical", command=canvas_form.yview)
canvas_form.configure(yscrollcommand=scroll_form.set)
canvas_form.grid(row=0, column=0, sticky="nsew")
scroll_form.grid(row=0, column=1, sticky="ns")

frame_izq = Frame(canvas_form, bg="#F7F5EF", padx=6, pady=6)
frame_izq.columnconfigure(1, weight=1)
ventana_form = canvas_form.create_window((0, 0), window=frame_izq, anchor="nw")

def _ajustar_form(_event=None):
    canvas_form.configure(scrollregion=canvas_form.bbox("all"))
    canvas_form.itemconfigure(ventana_form, width=canvas_form.winfo_width())

def _rueda_form(event):
    widget = root.winfo_containing(event.x_root, event.y_root)
    while widget is not None:
        if widget is contenedor_izq:
            canvas_form.yview_scroll(int(-1 * (event.delta / 120)), "units")
            return "break"
        widget = getattr(widget, "master", None)

frame_izq.bind("<Configure>", _ajustar_form)
canvas_form.bind("<Configure>", _ajustar_form)
root.bind_all("<MouseWheel>", _rueda_form)

# Encabezado
label_titulo = Label(frame_izq, text="Configuración del Modelo de Inventario", font=("Arial", 9, "bold"))
label_titulo.grid(row=0, column=0, columnspan=2, pady=2)

separador1 = ttk.Separator(frame_izq, orient="horizontal")
separador1.grid(row=1, column=0, columnspan=2, sticky="ew", pady=4)

# --- DATOS GENERALES ---
label_gen_titulo = Label(frame_izq, text="Datos Generales", font=("Arial", 8, "bold"))
label_gen_titulo.grid(row=2, column=0, columnspan=2, pady=2)

Label(frame_izq, text="Nombre del problema:", font=("Arial", 8)).grid(row=3, column=0, sticky="w", padx=2, pady=1)
entry_nombre_problema = Entry(frame_izq, width=15)
entry_nombre_problema.grid(row=3, column=1, sticky="ew", padx=2, pady=1)
entry_nombre_problema.insert(0, "Compra de Café Verde")

Label(frame_izq, text="Nombre base etapa (ej. Trimestre):", font=("Arial", 8)).grid(row=4, column=0, sticky="w", padx=2, pady=1)
entry_nombre_etapa = Entry(frame_izq, width=15)
entry_nombre_etapa.grid(row=4, column=1, sticky="ew", padx=2, pady=1)
entry_nombre_etapa.insert(0, "Trimestre")

Label(frame_izq, text="Unidad del producto (ej. libras):", font=("Arial", 8)).grid(row=5, column=0, sticky="w", padx=2, pady=1)
entry_unidad_producto = Entry(frame_izq, width=15)
entry_unidad_producto.grid(row=5, column=1, sticky="ew", padx=2, pady=1)
entry_unidad_producto.insert(0, "libras")

Label(frame_izq, text="Unidad monetaria (ej. USD/COP):", font=("Arial", 8)).grid(row=6, column=0, sticky="w", padx=2, pady=1)
entry_unidad_monetaria = Entry(frame_izq, width=15)
entry_unidad_monetaria.grid(row=6, column=1, sticky="ew", padx=2, pady=1)
entry_unidad_monetaria.insert(0, "COP")

Label(frame_izq, text="Objetivo:", font=("Arial", 8)).grid(row=7, column=0, sticky="w", padx=2, pady=1)
comboOp = ttk.Combobox(frame_izq, values=["Minimizar", "Maximizar"], state="readonly", width=12)
comboOp.grid(row=7, column=1, sticky="ew", padx=2, pady=1)
comboOp.set("Minimizar")

separador2 = ttk.Separator(frame_izq, orient="horizontal")
separador2.grid(row=8, column=0, columnspan=2, sticky="ew", pady=4)

# --- PARÁMETROS GLOBALES ---
label_glob_titulo = Label(frame_izq, text="Parámetros Globales de Inventario", font=("Arial", 8, "bold"))
label_glob_titulo.grid(row=9, column=0, columnspan=2, pady=2)

Label(frame_izq, text="Inventario inicial (I0):", font=("Arial", 8)).grid(row=10, column=0, sticky="w", padx=2, pady=1)
entry_inv_inicial = Entry(frame_izq, width=15)
entry_inv_inicial.grid(row=10, column=1, sticky="ew", padx=2, pady=1)
entry_inv_inicial.insert(0, "10")

Label(frame_izq, text="Inventario final requerido (IN):", font=("Arial", 8)).grid(row=11, column=0, sticky="w", padx=2, pady=1)
entry_inv_final = Entry(frame_izq, width=15)
entry_inv_final.grid(row=11, column=1, sticky="ew", padx=2, pady=1)
entry_inv_final.insert(0, "5")

Label(frame_izq, text="Capacidad máx. almacenamiento:", font=("Arial", 8)).grid(row=12, column=0, sticky="w", padx=2, pady=1)
entry_capacidad_max = Entry(frame_izq, width=15)
entry_capacidad_max.grid(row=12, column=1, sticky="ew", padx=2, pady=1)
entry_capacidad_max.insert(0, "50")

Label(frame_izq, text="Paso de discretización:", font=("Arial", 8)).grid(row=13, column=0, sticky="w", padx=2, pady=1)
entry_paso = Entry(frame_izq, width=15)
entry_paso.grid(row=13, column=1, sticky="ew", padx=2, pady=1)
entry_paso.insert(0, "1")

separador3 = ttk.Separator(frame_izq, orient="horizontal")
separador3.grid(row=14, column=0, columnspan=2, sticky="ew", pady=4)

# --- CONFIGURACIÓN DE ETAPAS ---
label_etapas_titulo = Label(frame_izq, text="Estructura de Etapas (1 a 8)", font=("Arial", 8, "bold"))
label_etapas_titulo.grid(row=15, column=0, columnspan=2, pady=2)

Label(frame_izq, text="No. Etapas:", font=("Arial", 8)).grid(row=16, column=0, sticky="w", padx=2, pady=1)
combo_etapas = ttk.Combobox(frame_izq, values=["1","2","3","4","5","6","7","8"], state="readonly", width=12)
combo_etapas.grid(row=16, column=1, sticky="ew", padx=2, pady=1)
combo_etapas.set("4")

buttonGenerarEtapas = ttk.Button(frame_izq, text="Generar Campos por Etapa", command=lambda: crear_etapas_dinamicas())
buttonGenerarEtapas.grid(row=17, column=0, columnspan=2, sticky="ew", padx=2, pady=3)

separador4 = ttk.Separator(frame_izq, orient="horizontal")
separador4.grid(row=18, column=0, columnspan=2, sticky="ew", pady=4)

# Contenedor dinámico de etapas
frame_contenedor_etapas = Frame(frame_izq, bg="#F7F5EF")
frame_contenedor_etapas.grid(row=19, column=0, columnspan=2, sticky="ew")
frame_contenedor_etapas.columnconfigure(0, weight=1)

entradas_etapas = []

def crear_etapas_dinamicas():
    """Limpia y genera los campos de entrada por cada etapa (Demanda, Precio, Almacenamiento, Compra Máxima)."""
    for widget in frame_contenedor_etapas.winfo_children():
        widget.destroy()
    entradas_etapas.clear()
    
    try:
        num = int(combo_etapas.get())
    except ValueError:
        num = 1
        
    base_nombre = entry_nombre_etapa.get().strip() or "Etapa"
    
    for i in range(num):
        sub_frame = ttk.LabelFrame(frame_contenedor_etapas, text=f" {base_nombre} {i+1} ", padding=5)
        sub_frame.grid(row=i, column=0, sticky="ew", pady=3, padx=2)
        sub_frame.columnconfigure(1, weight=1)
        
        # Demanda
        Label(sub_frame, text="Demanda (d):", font=("Arial", 7)).grid(row=0, column=0, sticky="w")
        ent_dem = Entry(sub_frame, width=10)
        ent_dem.grid(row=0, column=1, sticky="ew", padx=2)
        ent_dem.insert(0, "10")
        
        # Precio de compra por unidad
        Label(sub_frame, text="Precio compra (p):", font=("Arial", 7)).grid(row=1, column=0, sticky="w")
        ent_pre = Entry(sub_frame, width=10)
        ent_pre.grid(row=1, column=1, sticky="ew", padx=2)
        ent_pre.insert(0, "15")
        
        # Costo de almacenar por unidad
        Label(sub_frame, text="Costo almacenar (h):", font=("Arial", 7)).grid(row=2, column=0, sticky="w")
        ent_alm = Entry(sub_frame, width=10)
        ent_alm.grid(row=2, column=1, sticky="ew", padx=2)
        ent_alm.insert(0, "2")
        
        # Compra máxima posible
        Label(sub_frame, text="Compra máxima (M):", font=("Arial", 7)).grid(row=3, column=0, sticky="w")
        ent_max = Entry(sub_frame, width=10)
        ent_max.grid(row=3, column=1, sticky="ew", padx=2)
        ent_max.insert(0, "40")
        
        entradas_etapas.append({
            "demanda": ent_dem,
            "precio": ent_pre,
            "almacenar": ent_alm,
            "compra_max": ent_max
        })

# Generar etapas por defecto al iniciar
crear_etapas_dinamicas()

separador5 = ttk.Separator(frame_izq, orient="horizontal")
separador5.grid(row=20, column=0, columnspan=2, sticky="ew", pady=4)

#Frame derecho de las tablas
contenedor_der = ttk.LabelFrame(root, text="Paso a Paso (Tablas por Etapa)", padding=2)
contenedor_der.grid(row=0, column=1, sticky="nsew", padx=2, pady=2)
contenedor_der.columnconfigure(0, weight=1)
contenedor_der.rowconfigure(0, weight=1)
gestor_tablas = PanelTablasDinamicas(contenedor_der)
def resolver_modelo():
    """Valida los campos, construye la estructura de datos, ejecuta la lógica y pinta las tablas."""
    try:
        # 1. Validaciones globales y numéricas (las que ya tenías)
        try:
            inv_inicial = float(entry_inv_inicial.get())
            inv_final = float(entry_inv_final.get())
            capacidad_max = float(entry_capacidad_max.get())
            paso = float(entry_paso.get())
        except ValueError:
            messagebox.showerror("Error de Validación", "Los parámetros globales deben ser numéricos.")
            return

        if paso <= 0:
            messagebox.showerror("Error de Validación", "El paso debe ser mayor que cero.")
            return

        num_etapas = int(combo_etapas.get())
        tipo_opt = comboOp.get()

        # 2. Construir los estados basados en el paso y la capacidad máxima
        # Genera una lista de estados: [0, paso, 2*paso, ..., capacidad_max]
        estados_posibles = []
        val_actual = 0.0
        while val_actual <= capacidad_max + 1e-5:
            estados_posibles.append(round(val_actual, 4))
            val_actual += paso

        # 3. Construir la lista de etapas para el algoritmo de PD
        etapas_data = []
        for idx, et in enumerate(entradas_etapas):
            d = float(et["demanda"].get())
            p = float(et["precio"].get())
            h = float(et["almacenar"].get())
            m = float(et["compra_max"].get())

            # Definición de la función de costo inmediato para inventarios:
            # Costo = (Precio * Compra) + (Costo_Almacenar * Inventario_Resultante)
            def f_costo_inventario(s, x, demanda_etapa=d, precio_etapa=p, almacen_etapa=h):
                costo_compra = precio_etapa * x
                # El inventario al final de la etapa es s + x - demanda
                inv_restante = s + x - demanda_etapa
                costo_almacenamiento = almacen_etapa * inv_restante
                return costo_compra + costo_almacenamiento

            # Función de transición: s_siguiente = s_actual + compra - demanda
            def transicion_inventario(s, x, demanda_etapa=d):
                return s + x - demanda_etapa

            # Decisiones posibles (compras x) limitadas por la compra máxima 'm' y la capacidad
            def decisiones_permitidas(s, compra_max=m, cap_max=capacidad_max, demanda_etapa=d):
                # Rango lógico de compra: de 0 hasta la compra máxima permitida en la etapa
                # asegurando que el estado siguiente no supere la capacidad máxima de almacenamiento
                decisiones = []
                x_val = 0.0
                while x_val <= compra_max + 1e-5:
                    s_sig = s + x_val - demanda_etapa
                    if 0 <= s_sig <= cap_max:
                        decisiones.append(round(x_val, 4))
                    x_val += paso
                return decisiones

            etapas_data.append({
                "nombre": f"{entry_nombre_etapa.get().strip() or 'Etapa'} {idx+1}",
                "estados": estados_posibles,
                "decisiones": decisiones_permitidas,
                "f_costo": f_costo_inventario,
                "transicion": transicion_inventario
            })

        # 4. Ejecutar el motor de Programación Dinámica
        resultado = resolver_programacion_dinamica(
            etapas_data=etapas_data,
            tipo_opt=tipo_opt,
            capacidad_inicial=inv_inicial
        )

        if resultado["estado"] == "Infactible":
            messagebox.showwarning("Modelo Infactible", "El modelo no encontró una solución factible con los parámetros y restricciones dadas.")
            return

        # 5. Enviar el resultado al componente de tablas para que las pinte en el lado derecho
        gestor_tablas.mostrar_tablas(resultado)

    except Exception as e:
        messagebox.showerror("Error de Ejecución", f"Ocurrió un error al procesar el modelo: {str(e)}")
# Botones de acción principales
buttonResolver = ttk.Button(frame_izq, text="Resolver DP", command=resolver_modelo)
buttonResolver.grid(row=21, column=0, sticky="ew", padx=1, pady=1)

def limpiar_campos():
    entry_inv_inicial.delete(0, END)
    entry_inv_inicial.insert(0, "10")
    entry_inv_final.delete(0, END)
    entry_inv_final.insert(0, "5")
    entry_capacidad_max.delete(0, END)
    entry_capacidad_max.insert(0, "50")
    entry_paso.delete(0, END)
    entry_paso.insert(0, "1")
    crear_etapas_dinamicas()

buttonLimpiar = ttk.Button(frame_izq, text="Limpiar", command=limpiar_campos)
buttonLimpiar.grid(row=21, column=1, sticky="ew", padx=1, pady=1)

# Botón para regresar al menú de bienvenida
def volver_al_menu():
    root.volver_al_menu = True
    root.destroy()

buttonVolver = ttk.Button(root, text="← Volver al menú", command=volver_al_menu)
buttonVolver.place(relx=1.0, x=-12, y=10, anchor="ne")

# Iniciar aplicación
if __name__ == "__main__":
    root.mainloop()