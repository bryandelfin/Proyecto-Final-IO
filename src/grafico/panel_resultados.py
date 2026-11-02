# Panel de resultados en tabla
# Método Gráfico - Investigación de Operaciones
#
# Este módulo sustituye las ventanas emergentes de solución por un frame
# con una tabla de puntos factibles y su evaluación en la función objetivo.

import tkinter as tk
from tkinter import ttk, messagebox

import plano_cartesiano
from logica_metodo_grafico import resolver_modelo_grafico


class _MessageboxSilencioso:
    """Silencia únicamente los avisos de solución de plano_cartesiano."""

    @staticmethod
    def showerror(*args, **kwargs):
        pass

    @staticmethod
    def showwarning(*args, **kwargs):
        pass

    @staticmethod
    def showinfo(*args, **kwargs):
        pass


def crear_panel_resultados(parent):
    """Crea el frame inferior con la tabla de resultados."""
    frame = ttk.LabelFrame(parent, text="Resultados", padding=4)
    frame.columnconfigure(0, weight=1)
    frame.rowconfigure(2, weight=1)

    resumen = ttk.Label(frame, text="Sin resultados todavía.", anchor="w")
    resumen.grid(row=0, column=0, columnspan=2, sticky="ew", padx=2, pady=(0, 2))

    detalle = ttk.Label(
        frame,
        text="",
        anchor="w",
        justify="left",
        font=("Segoe UI", 9),
        wraplength=1000,
    )
    detalle.grid(row=1, column=0, columnspan=2, sticky="ew", padx=2, pady=(0, 4))

    columnas = ("punto", "x1", "x2", "z")
    tabla = ttk.Treeview(frame, columns=columnas, show="headings", height=5)
    tabla.heading("punto", text="Punto")
    tabla.heading("x1", text="X1")
    tabla.heading("x2", text="X2")
    tabla.heading("z", text="Z = f(X1, X2)")
    tabla.column("punto", anchor="center", width=60, stretch=False)
    tabla.column("x1", anchor="center", width=140)
    tabla.column("x2", anchor="center", width=140)
    tabla.column("z", anchor="center", width=160)
    tabla.tag_configure("optimo", foreground="#B00020", font=("Segoe UI", 9, "bold"))

    scroll = ttk.Scrollbar(frame, orient="vertical", command=tabla.yview)
    tabla.configure(yscrollcommand=scroll.set)

    tabla.grid(row=2, column=0, sticky="nsew")
    scroll.grid(row=2, column=1, sticky="ns")

    frame.tabla = tabla
    frame.resumen = resumen
    frame.detalle = detalle
    return frame


def _obtener_coeficientes():
    try:
        import panel_entrada

        return (
            float(panel_entrada.entry_valor1.get()),
            float(panel_entrada.entry_valor2.get()),
        )
    except (ValueError, AttributeError):
        return None


def _formatear(valor):
    if valor is None:
        return "—"
    return f"{round(valor, 4):g}"


def limpiar_resultados(frame, mensaje="Sin resultados todavía."):
    frame.tabla.delete(*frame.tabla.get_children())
    frame.resumen.configure(text=mensaje, foreground="#2B2D42")
    frame.detalle.configure(text="")


def _nombre_variable(nombre, indice):
    """Devuelve un nombre descriptivo; nunca muestra X1/X2 en el texto de solución."""
    limpio = (nombre or "").strip()
    if not limpio or limpio.upper() in ("X1", "X2"):
        return f"Variable {indice}"
    return limpio


def _detalle_compra(resultado):
    """Texto con la cantidad a comprar de cada variable, usando sus nombres."""
    estado = resultado.get("estado", "")
    optimos = resultado.get("puntos_optimos", [])
    if estado not in ("Unica", "Empate") or not optimos:
        return ""

    nombre_v1 = _nombre_variable(resultado.get("nombre_v1"), 1)
    nombre_v2 = _nombre_variable(resultado.get("nombre_v2"), 2)

    lineas = []
    if estado == "Unica":
        x, y = optimos[0]
        lineas.append("Cantidad a comprar:")
        lineas.append(f"• {nombre_v1}: {_formatear(x)}")
        lineas.append(f"• {nombre_v2}: {_formatear(y)}")
    else:
        lineas.append("Opciones óptimas (cantidad a comprar):")
        for i, (x, y) in enumerate(sorted(optimos), start=1):
            lineas.append(f"Opción {i}:")
            lineas.append(f"• {nombre_v1}: {_formatear(x)}")
            lineas.append(f"• {nombre_v2}: {_formatear(y)}")
    return "\n".join(lineas)


def mostrar_resultados(frame, resultado, c1, c2):
    tabla = frame.tabla
    resumen = frame.resumen
    tabla.delete(*tabla.get_children())

    estado = resultado.get("estado", "")
    puntos = resultado.get("puntos_factibles", [])
    optimos = {(round(x, 4), round(y, 4)) for x, y in resultado.get("puntos_optimos", [])}
    mejor_z = resultado.get("mejor_z")
    tipo_opt = resultado.get("tipo_opt", "")

    if estado == "Infactible":
        mensaje = "Modelo INFACTIBLE: no existe una región que cumpla todas las restricciones."
        color = "#B00020"
    elif estado == "No Acotado":
        mensaje = "Modelo NO ACOTADO: la función objetivo puede crecer indefinidamente."
        color = "#B26A00"
    elif estado == "Empate":
        mensaje = f"Múltiples soluciones óptimas ({tipo_opt}). Z óptimo = {_formatear(mejor_z)}"
        color = "#1D3557"
    elif estado == "Unica":
        mensaje = f"Solución óptima única ({tipo_opt}). Z óptimo = {_formatear(mejor_z)}"
        color = "#1D3557"
    else:
        mensaje = ""
        color = "#2B2D42"

    resumen.configure(text=mensaje, foreground=color)
    frame.detalle.configure(text=_detalle_compra(resultado))

    for i, (px, py) in enumerate(sorted(puntos), start=1):
        z = (c1 * px + c2 * py) if c1 is not None and c2 is not None else None
        es_optimo = (round(px, 4), round(py, 4)) in optimos
        tabla.insert(
            "",
            "end",
            values=(i, _formatear(px), _formatear(py), _formatear(z)),
            tags=("optimo",) if es_optimo else (),
        )


def resolver_y_mostrar(canvas, frame_resultados):
    """Resuelve, dibuja y llena la tabla sin mostrar ventanas emergentes de solución."""
    try:
        resultado = resolver_modelo_grafico()
    except ValueError as error:
        messagebox.showerror("Error de validación", str(error))
        limpiar_resultados(frame_resultados, "Corrige los datos para ver los resultados.")
        return

    messagebox_original = plano_cartesiano.messagebox
    plano_cartesiano.messagebox = _MessageboxSilencioso
    try:
        plano_cartesiano.resolver_y_dibujar(canvas)
    finally:
        plano_cartesiano.messagebox = messagebox_original

    coeficientes = _obtener_coeficientes()
    if coeficientes is None:
        c1 = c2 = None
    else:
        c1, c2 = coeficientes

    mostrar_resultados(frame_resultados, resultado, c1, c2)
