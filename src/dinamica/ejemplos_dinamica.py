# Ejemplos precargados para Programación Dinámica (modelo de inventarios).
# Módulo nuevo: no modifica la lógica ni el formulario existentes.
import tkinter as tk
from tkinter import ttk, messagebox

from logica_programacion_dinamica import resolver_programacion_dinamica


# Ejemplo 1: Editable/Factible (se pueden cambiar los valores después de cargarlo)
EJEMPLO_EDITABLE = {
    "nombre": "Ejemplo 1 Coffee Holding Co.",
    "nombre_problema": "Compra de Café Verde - Ejemplo Editable",
    "nombre_etapa": "Trimestre",
    "unidad_producto": "libras",
    "unidad_monetaria": "COP",
    "tipo_opt": "Minimizar",
    "inv_inicial": 96,
    "inv_final": 87,
    "capacidad_max": 120,
    "paso": 1,
    "etapas": [
        {"demanda": 92, "precio": 172480, "almacenar": 3937.2, "compra_max": 195},
        {"demanda": 103, "precio": 152680, "almacenar": 3636.8, "compra_max": 195},
        {"demanda": 90, "precio": 157960, "almacenar": 3716.9, "compra_max": 195}
    ],
}

# Ejemplo 2: Infactible (la demanda supera la capacidad máxima + compra máxima)
EJEMPLO_INFACTIBLE = {
    "nombre": "Ejemplo 2 (Infactible)",
    "nombre_problema": "Compra de Café Verde - Caso Infactible",
    "nombre_etapa": "Trimestre",
    "unidad_producto": "libras",
    "unidad_monetaria": "COP",
    "tipo_opt": "Minimizar",
    "inv_inicial": 10,
    "inv_final": 0,
    "capacidad_max": 50,
    "paso": 1,
    "etapas": [
        {"demanda": 100, "precio": 15, "almacenar": 2, "compra_max": 40},
        {"demanda": 10, "precio": 15, "almacenar": 2, "compra_max": 40},
    ],
}

# Lista de todos los ejemplos disponibles en el combobox
EJEMPLOS = [
    EJEMPLO_EDITABLE,
    EJEMPLO_INFACTIBLE,
]


def construir_etapas_data(ejemplo, capacidad_max, paso):
    """Construye las etapas que consume el algoritmo de programación dinámica.

    Replica la estructura que arma el formulario, pero a partir de los datos de
    un ejemplo. Se usa para cargar el ejemplo y para verificar los casos sin
    necesidad de abrir la interfaz gráfica.
    """
    estados_posibles = []
    valor = 0.0
    while valor <= capacidad_max + 1e-5:
        estados_posibles.append(round(valor, 4))
        valor += paso

    final_min = float(ejemplo["inv_final"])
    total_etapas = len(ejemplo["etapas"])

    etapas_data = []
    for indice, etapa in enumerate(ejemplo["etapas"]):
        demanda = float(etapa["demanda"])
        precio = float(etapa["precio"])
        almacenar = float(etapa["almacenar"])
        compra_max = float(etapa["compra_max"])
        es_ultima_etapa = (indice == total_etapas - 1)

        def f_costo(s, x, demanda_etapa=demanda, precio_etapa=precio,
                    almacen_etapa=almacenar):
            costo_compra = precio_etapa * x
            inv_restante = s + x - demanda_etapa
            costo_almacenamiento = almacen_etapa * inv_restante
            return costo_compra + costo_almacenamiento

        def transicion(s, x, demanda_etapa=demanda, final_objetivo=final_min,
                       ultima=es_ultima_etapa):
            s_sig = s + x - demanda_etapa
            if ultima and s_sig < final_objetivo - 1e-5:
                raise ValueError("inventario final insuficiente")
            return s_sig

        def decisiones(s, compra_maxima=compra_max, cap_max=capacidad_max,
                       demanda_etapa=demanda, incremento=paso,
                       final_objetivo=final_min, ultima=es_ultima_etapa):
            permitidas = []
            x_val = 0.0
            while x_val <= compra_maxima + 1e-5:
                s_sig = s + x_val - demanda_etapa
                cumple_final = (not ultima) or (s_sig >= final_objetivo - 1e-5)
                if 0 <= s_sig <= cap_max and cumple_final:
                    permitidas.append(round(x_val, 4))
                x_val += incremento
            return permitidas

        etapas_data.append({
            "nombre": f"{ejemplo['nombre_etapa']} {indice + 1}",
            "estados": estados_posibles,
            "decisiones": decisiones,
            "f_costo": f_costo,
            "transicion": transicion,
        })

    return etapas_data


def resolver_ejemplo(ejemplo):
    """Resuelve un ejemplo directamente (sin interfaz) y devuelve el resultado."""
    etapas_data = construir_etapas_data(
        ejemplo,
        float(ejemplo["capacidad_max"]),
        float(ejemplo["paso"]),
    )
    return resolver_programacion_dinamica(
        etapas_data=etapas_data,
        tipo_opt=ejemplo["tipo_opt"],
        capacidad_inicial=float(ejemplo["inv_inicial"]),
    )


def _set_entry(entry, valor):
    entry.delete(0, tk.END)
    entry.insert(0, str(valor))


def cargar_ejemplo_dinamica(contexto, indice):
    """Carga un ejemplo en el formulario y resuelve el modelo automáticamente.

    Args:
        contexto (dict): Referencias a los widgets y funciones del formulario.
        indice (int): Posición del ejemplo dentro de EJEMPLOS.

    Returns:
        dict | None: El ejemplo cargado, o None si no se pudo cargar.
    """
    if not isinstance(indice, int) or not 0 <= indice < len(EJEMPLOS):
        messagebox.showwarning("Advertencia", "Seleccione un ejemplo válido")
        return None

    ejemplo = EJEMPLOS[indice]

    try:
        _set_entry(contexto["entry_nombre_problema"], ejemplo["nombre_problema"])
        _set_entry(contexto["entry_nombre_etapa"], ejemplo["nombre_etapa"])
        _set_entry(contexto["entry_unidad_producto"], ejemplo["unidad_producto"])
        _set_entry(contexto["entry_unidad_monetaria"], ejemplo["unidad_monetaria"])
        _set_entry(contexto["entry_inv_inicial"], ejemplo["inv_inicial"])
        _set_entry(contexto["entry_inv_final"], ejemplo["inv_final"])
        _set_entry(contexto["entry_capacidad_max"], ejemplo["capacidad_max"])
        _set_entry(contexto["entry_paso"], ejemplo["paso"])

        contexto["comboOp"].set(ejemplo["tipo_opt"])
        contexto["combo_etapas"].set(str(len(ejemplo["etapas"])))

        # Regenera los campos por etapa y rellena cada uno con los datos del ejemplo
        contexto["crear_etapas_dinamicas"]()

        for entrada, etapa in zip(contexto["entradas_etapas"], ejemplo["etapas"]):
            _set_entry(entrada["demanda"], etapa["demanda"])
            _set_entry(entrada["precio"], etapa["precio"])
            _set_entry(entrada["almacenar"], etapa["almacenar"])
            _set_entry(entrada["compra_max"], etapa["compra_max"])

        contexto["resolver_modelo"]()
        return ejemplo
    except Exception as error:
        messagebox.showerror("Error", f"Error al cargar ejemplo: {error}")
        return None


def agregar_seccion_ejemplos(parent, contexto, fila=5):
    """Agrega el combobox y el botón para cargar ejemplos en el formulario."""
    frame_ejemplos = ttk.LabelFrame(parent, text=" Ejemplos ", padding=8)
    frame_ejemplos.grid(row=fila, column=0, columnspan=2, sticky="ew", padx=2, pady=4)
    frame_ejemplos.columnconfigure(0, weight=1)

    combo_ejemplos = ttk.Combobox(
        frame_ejemplos,
        values=[ejemplo["nombre"] for ejemplo in EJEMPLOS],
        state="readonly",
        width=25,
    )
    combo_ejemplos.grid(row=0, column=0, sticky="ew", padx=2, pady=2)
    combo_ejemplos.current(0)

    def _cargar_seleccionado():
        cargar_ejemplo_dinamica(contexto, combo_ejemplos.current())

    boton_cargar = ttk.Button(
        frame_ejemplos,
        text="Cargar Ejemplo",
        command=_cargar_seleccionado,
    )
    boton_cargar.grid(row=1, column=0, sticky="ew", padx=2, pady=2)

    return frame_ejemplos, combo_ejemplos
