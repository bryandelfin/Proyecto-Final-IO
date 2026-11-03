# Módulo de Formulario y Ventana Principal para Programación Dinámica
import tkinter as tk
from tkinter import ttk, messagebox
import sys, os

# Configuración de rutas para importar módulos locales
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from logica_programacion_dinamica import resolver_programacion_dinamica
from panel_tablas import PanelTablasDinamicas

# Variable global requerida por main.py
root = tk.Tk()

# Configuración de la ventana principal
root.title("Programación Dinámica - Modelo de Inventarios de Café")
root.geometry("1250x700")
root.resizable(True, True)

# Configuración de grid principal
root.columnconfigure(0, weight=0)
root.columnconfigure(1, weight=3)
root.rowconfigure(0, weight=1)

# Frame izquierdo - Panel de entrada con scroll
contenedor_izq = ttk.LabelFrame(root, text="Modelo de Programación Dinámica - Compras de Café", padding=0)
contenedor_izq.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)
contenedor_izq.columnconfigure(0, weight=1)
contenedor_izq.rowconfigure(0, weight=1)

canvas_form = tk.Canvas(contenedor_izq, bg="#F7F5EF", highlightthickness=0)
scroll_form = ttk.Scrollbar(contenedor_izq, orient="vertical", command=canvas_form.yview)
canvas_form.configure(yscrollcommand=scroll_form.set)
canvas_form.grid(row=0, column=0, sticky="nsew")
scroll_form.grid(row=0, column=1, sticky="ns")

frame_izq = tk.Frame(canvas_form, bg="#F7F5EF", padx=8, pady=8)
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

# Frame derecho para las tablas y la solución óptima global
contenedor_der = ttk.LabelFrame(root, text="Paso a Paso y Solución Óptima", padding=2)
contenedor_der.grid(row=0, column=1, sticky="nsew", padx=2, pady=2)
contenedor_der.columnconfigure(0, weight=1)
contenedor_der.rowconfigure(0, weight=1)

gestor_tablas = PanelTablasDinamicas(contenedor_der)

# ==========================================
# 1. CONFIGURACIÓN GENERAL
# ==========================================
frame_config_general = ttk.LabelFrame(frame_izq, text=" Configuración General ", padding=8)
frame_config_general.grid(row=0, column=0, columnspan=2, sticky="ew", pady=4, padx=2)
frame_config_general.columnconfigure(1, weight=1)

tk.Label(frame_config_general, text="Nombre del problema:", font=("Segoe UI", 8)).grid(row=0, column=0, sticky="w", pady=2)
entry_nombre_problema = tk.Entry(frame_config_general, width=18)
entry_nombre_problema.grid(row=0, column=1, sticky="ew", padx=2, pady=2)
entry_nombre_problema.insert(0, "Compra de Café Verde")

tk.Label(frame_config_general, text="Nombre base etapa:", font=("Segoe UI", 8)).grid(row=1, column=0, sticky="w", pady=2)
entry_nombre_etapa = tk.Entry(frame_config_general, width=18)
entry_nombre_etapa.grid(row=1, column=1, sticky="ew", padx=2, pady=2)
entry_nombre_etapa.insert(0, "Trimestre")

tk.Label(frame_config_general, text="Unidad del producto:", font=("Segoe UI", 8)).grid(row=2, column=0, sticky="w", pady=2)
entry_unidad_producto = tk.Entry(frame_config_general, width=18)
entry_unidad_producto.grid(row=2, column=1, sticky="ew", padx=2, pady=2)
entry_unidad_producto.insert(0, "libras")

tk.Label(frame_config_general, text="Unidad monetaria:", font=("Segoe UI", 8)).grid(row=3, column=0, sticky="w", pady=2)
entry_unidad_monetaria = tk.Entry(frame_config_general, width=18)
entry_unidad_monetaria.grid(row=3, column=1, sticky="ew", padx=2, pady=2)
entry_unidad_monetaria.insert(0, "COP")

tk.Label(frame_config_general, text="Objetivo:", font=("Segoe UI", 8)).grid(row=4, column=0, sticky="w", pady=2)
comboOp = ttk.Combobox(frame_config_general, values=["Minimizar", "Maximizar"], state="readonly", width=15)
comboOp.grid(row=4, column=1, sticky="ew", padx=2, pady=2)
comboOp.set("Minimizar")

# ==========================================
# 2. PARÁMETROS GLOBALES DE INVENTARIO
# ==========================================
frame_inv = ttk.LabelFrame(frame_izq, text=" Parámetros de Inventario ", padding=8)
frame_inv.grid(row=1, column=0, columnspan=2, sticky="ew", pady=4, padx=2)
frame_inv.columnconfigure(1, weight=1)

tk.Label(frame_inv, text="Inventario inicial (I0):", font=("Segoe UI", 8)).grid(row=0, column=0, sticky="w", pady=2)
entry_inv_inicial = tk.Entry(frame_inv, width=18)
entry_inv_inicial.grid(row=0, column=1, sticky="ew", padx=2, pady=2)
entry_inv_inicial.insert(0, "10")

tk.Label(frame_inv, text="Inventario final (IN):", font=("Segoe UI", 8)).grid(row=1, column=0, sticky="w", pady=2)
entry_inv_final = tk.Entry(frame_inv, width=18)
entry_inv_final.grid(row=1, column=1, sticky="ew", padx=2, pady=2)
entry_inv_final.insert(0, "5")

tk.Label(frame_inv, text="Capacidad máx. (M):", font=("Segoe UI", 8)).grid(row=2, column=0, sticky="w", pady=2)
entry_capacidad_max = tk.Entry(frame_inv, width=18)
entry_capacidad_max.grid(row=2, column=1, sticky="ew", padx=2, pady=2)
entry_capacidad_max.insert(0, "50")

tk.Label(frame_inv, text="Paso discretización:", font=("Segoe UI", 8)).grid(row=3, column=0, sticky="w", pady=2)
entry_paso = tk.Entry(frame_inv, width=18)
entry_paso.grid(row=3, column=1, sticky="ew", padx=2, pady=2)
entry_paso.insert(0, "1")

# ==========================================
# 3. ESTRUCTURA DE ETAPAS
# ==========================================
frame_num_etapas = ttk.LabelFrame(frame_izq, text=" Estructura de Etapas ", padding=8)
frame_num_etapas.grid(row=2, column=0, columnspan=2, sticky="ew", pady=4, padx=2)
frame_num_etapas.columnconfigure(1, weight=1)

tk.Label(frame_num_etapas, text="No. Etapas (1-8):", font=("Segoe UI", 8)).grid(row=0, column=0, sticky="w", pady=2)
combo_etapas = ttk.Combobox(frame_num_etapas, values=["1","2","3","4","5","6","7","8"], state="readonly", width=15)
combo_etapas.grid(row=0, column=1, sticky="ew", padx=2, pady=2)
combo_etapas.set("4")

buttonGenerarEtapas = ttk.Button(frame_num_etapas, text="Generar Campos por Etapa")
buttonGenerarEtapas.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(6, 2))

# Contenedor dinámico de etapas
frame_contenedor_etapas = tk.Frame(frame_izq, bg="#F7F5EF")
frame_contenedor_etapas.grid(row=3, column=0, columnspan=2, sticky="ew", pady=4)
frame_contenedor_etapas.columnconfigure(0, weight=1)

entradas_etapas = []

def crear_etapas_dinamicas():
    for widget in frame_contenedor_etapas.winfo_children():
        widget.destroy()
    entradas_etapas.clear()
    
    try:
        num = int(combo_etapas.get())
    except ValueError:
        num = 1
        
    base_nombre = entry_nombre_etapa.get().strip() or "Etapa"
    
    for i in range(num):
        sub_frame = ttk.LabelFrame(frame_contenedor_etapas, text=f" {base_nombre} {i+1} ", padding=6)
        sub_frame.grid(row=i, column=0, sticky="ew", pady=3, padx=2)
        sub_frame.columnconfigure(1, weight=1)
        
        tk.Label(sub_frame, text="Demanda (d):", font=("Segoe UI", 7)).grid(row=0, column=0, sticky="w")
        ent_dem = tk.Entry(sub_frame, width=12)
        ent_dem.grid(row=0, column=1, sticky="ew", padx=2)
        ent_dem.insert(0, "10")
        
        tk.Label(sub_frame, text="Precio compra (p):", font=("Segoe UI", 7)).grid(row=1, column=0, sticky="w")
        ent_pre = tk.Entry(sub_frame, width=12)
        ent_pre.grid(row=1, column=1, sticky="ew", padx=2)
        ent_pre.insert(0, "15")
        
        tk.Label(sub_frame, text="Costo almacenar (h):", font=("Segoe UI", 7)).grid(row=2, column=0, sticky="w")
        ent_alm = tk.Entry(sub_frame, width=12)
        ent_alm.grid(row=2, column=1, sticky="ew", padx=2)
        ent_alm.insert(0, "2")
        
        tk.Label(sub_frame, text="Compra máxima (M):", font=("Segoe UI", 7)).grid(row=3, column=0, sticky="w")
        ent_max = tk.Entry(sub_frame, width=12)
        ent_max.grid(row=3, column=1, sticky="ew", padx=2)
        ent_max.insert(0, "40")
        
        entradas_etapas.append({
            "demanda": ent_dem,
            "precio": ent_pre,
            "almacenar": ent_alm,
            "compra_max": ent_max
        })

buttonGenerarEtapas.configure(command=crear_etapas_dinamicas)
crear_etapas_dinamicas()

# ==========================================
# 4. BOTONES DE ACCIÓN PRINCIPALES
# ==========================================
frame_botones = tk.Frame(frame_izq, bg="#F7F5EF")
frame_botones.grid(row=4, column=0, columnspan=2, sticky="ew", pady=10)
frame_botones.columnconfigure(0, weight=1)
frame_botones.columnconfigure(1, weight=1)

def resolver_modelo():
    try:
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

        estados_posibles = []
        val_actual = 0.0
        while val_actual <= capacidad_max + 1e-5:
            estados_posibles.append(round(val_actual, 4))
            val_actual += paso

        etapas_data = []
        for idx, et in enumerate(entradas_etapas):
            d = float(et["demanda"].get())
            p = float(et["precio"].get())
            h = float(et["almacenar"].get())
            m = float(et["compra_max"].get())

            def f_costo_inventario(s, x, demanda_etapa=d, precio_etapa=p, almacen_etapa=h):
                costo_compra = precio_etapa * x
                inv_restante = s + x - demanda_etapa
                costo_almacenamiento = almacen_etapa * inv_restante
                return costo_compra + costo_almacenamiento

            def transicion_inventario(s, x, demanda_etapa=d):
                return s + x - demanda_etapa

            def decisiones_permitidas(s, compra_max=m, cap_max=capacidad_max, demanda_etapa=d):
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

        resultado = resolver_programacion_dinamica(
            etapas_data=etapas_data,
            tipo_opt=tipo_opt,
            capacidad_inicial=inv_inicial
        )

        if resultado["estado"] == "Infactible":
            messagebox.showwarning("Modelo Infactible", "El modelo no encontró una solución factible con los parámetros y restricciones dadas.")
            return

        gestor_tablas.mostrar_tablas(resultado)

    except Exception as e:
        messagebox.showerror("Error de Ejecución", f"Ocurrió un error al procesar el modelo: {str(e)}")

def limpiar_campos():
    entry_inv_inicial.delete(0, tk.END)
    entry_inv_inicial.insert(0, "10")
    entry_inv_final.delete(0, tk.END)
    entry_inv_final.insert(0, "5")
    entry_capacidad_max.delete(0, tk.END)
    entry_capacidad_max.insert(0, "50")
    entry_paso.delete(0, tk.END)
    entry_paso.insert(0, "1")
    crear_etapas_dinamicas()

buttonResolver = ttk.Button(frame_botones, text="Resolver DP", command=resolver_modelo)
buttonResolver.grid(row=0, column=0, sticky="ew", padx=(0, 2))

buttonLimpiar = ttk.Button(frame_botones, text="Limpiar", command=limpiar_campos)
buttonLimpiar.grid(row=0, column=1, sticky="ew", padx=(2, 0))

# Botón para regresar al menú
def volver_al_menu():
    root.volver_al_menu = True
    root.destroy()

buttonVolver = ttk.Button(root, text="← Volver al menú", command=volver_al_menu)
buttonVolver.place(relx=1.0, x=-12, y=10, anchor="ne")