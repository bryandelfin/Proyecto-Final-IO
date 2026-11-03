# Ventana de bienvenida - Menú principal
# Método Gráfico - Investigación de Operaciones

import tkinter as tk
from tkinter import ttk

# Paleta del menú
COLOR_DORADO = "#B8912F"
COLOR_DORADO_HOVER = "#D4AF37"
COLOR_FONDO = "#F7F5EF"
COLOR_TEXTO = "#2B2D42"


class Menu:
    """Menú de bienvenida que pregunta qué desea calcular el usuario."""

    def __init__(self, root, callback):
        self.root = root
        self.callback = callback
        self._configurar_ventana()
        self._configurar_estilos()
        self._construir_interfaz()

    def _configurar_ventana(self):
        self.root.title("Bienvenida - Método Gráfico IO")
        self.root.geometry("720x430")
        self.root.minsize(640, 380)
        self.root.configure(bg=COLOR_FONDO)

    def _configurar_estilos(self):
        style = ttk.Style()
        style.configure(
            "Gold.TButton",
            background=COLOR_DORADO,
            foreground="#FFFFFF",
            font=("Segoe UI", 9, "bold"),
            padding=(14, 6),
            borderwidth=0,
        )
        style.map(
            "Gold.TButton",
            background=[("active", COLOR_DORADO_HOVER), ("pressed", "#9C7A24")],
        )

    def _construir_interfaz(self):
        contenedor = tk.Frame(self.root, bg=COLOR_FONDO)
        contenedor.pack(fill="both", expand=True)
        contenedor.columnconfigure(0, weight=1)

        # Título alineado a la izquierda
        titulo = tk.Label(
            contenedor,
            text="Bienvenido \n¿Qué deseas calcular hoy?",
            font=("Segoe UI", 20, "bold"),
            fg=COLOR_TEXTO,
            bg=COLOR_FONDO,
            anchor="w",
            justify="left",
        )
        titulo.grid(row=0, column=0, sticky="w", padx=40, pady=(40, 0))

        # Acento dorado minimalista debajo del título
        acento = tk.Frame(contenedor, bg=COLOR_DORADO, height=3, width=90)
        acento.grid(row=1, column=0, sticky="w", padx=40, pady=(10, 30))
        acento.grid_propagate(False)

        # Lista de opciones
        opciones = tk.Frame(contenedor, bg=COLOR_FONDO)
        opciones.grid(row=2, column=0, sticky="ew", padx=40)
        opciones.columnconfigure(0, weight=1)

        self._crear_fila(opciones, 0, "Cuánto comprar - (Programación Dinámica)", "comprar")
        ttk.Separator(opciones, orient="horizontal").grid(
            row=1, column=0, columnspan=2, sticky="ew", pady=12
        )
        self._crear_fila(opciones, 2, "Cuánto producir - (Método Gráfico)", "producir")
        ttk.Separator(opciones, orient="horizontal").grid(
            row=3, column=0, columnspan=2, sticky="ew", pady=12
        )

    def _crear_fila(self, parent, fila, texto, tipo):
        tk.Label(
            parent,
            text=f"•  {texto}",
            font=("Segoe UI", 13),
            fg=COLOR_TEXTO,
            bg=COLOR_FONDO,
            anchor="w",
        ).grid(row=fila, column=0, sticky="w", pady=6)

        ttk.Button(
            parent,
            text="Continuar",
            style="Gold.TButton",
            command=lambda: self._elegir(tipo),
        ).grid(row=fila, column=1, sticky="e", padx=(20, 0), pady=6)

    def _elegir(self, tipo):
        self.root.destroy()
        self.callback(tipo)
