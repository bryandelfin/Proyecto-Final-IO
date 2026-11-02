# Módulo exclusivo para la visualización de tablas paso a paso (Treeview)
import tkinter as tk
from tkinter import ttk

class PanelTablasDinamicas:
    def __init__(self, parent_frame):
        """
        parent_frame: El marco derecho de la ventana principal donde se incrustarán las tablas.
        """
        self.parent_frame = parent_frame
        self.setup_ui()

    def setup_ui(self):
        """Configura un Canvas con Scrollbar para hacer la vista derecha totalmente responsiva y deslizable."""
        # Limpiar por si ya existía algo previamente
        for widget in self.parent_frame.winfo_children():
            widget.destroy()

        self.canvas = tk.Canvas(self.parent_frame, bg="#F7F5EF", highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.parent_frame, orient="vertical", command=self.canvas.yview)
        
        self.scrollable_frame = ttk.Frame(self.canvas, padding=15)
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.window_id = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Ajustar ancho del canvas dinámicamente al redimensionar la ventana
        self.canvas.bind('<Configure>', lambda event: self.canvas.itemconfig(self.window_id, width=event.width))

        # Mensaje inicial de guía
        self.label_inicial = ttk.Label(
            self.scrollable_frame, 
            text="Configure los parámetros en el panel izquierdo y haga clic en 'Resolver DP'\npara visualizar el desglose paso a paso por etapas.", 
            font=("Segoe UI", 10),
            foreground="#555555"
        )
        self.label_inicial.pack(pady=40, padx=20)

    def mostrar_tablas(self, resultado_dp):
        """Genera dinámicamente una tabla (Treeview) por cada etapa evaluada (Procedimiento Hacia Atrás)."""
        # Limpiar contenido anterior
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        tablas_etapas = resultado_dp.get("tablas_etapas", [])
        
        if not tablas_etapas:
            lbl = ttk.Label(self.scrollable_frame, text="No hay datos de etapas para mostrar.", font=("Segoe UI", 10))
            lbl.pack(pady=20)
            return

        # Título de la sección
        lbl_titulo = ttk.Label(
            self.scrollable_frame, 
            text="Paso a Paso y Evaluación por Etapas", 
            font=("Segoe UI", 11, "bold"),
            foreground="#1D3557"
        )
        lbl_titulo.pack(anchor="w", pady=(0, 15))

        # Iterar sobre cada etapa para crear su respectiva tarjeta y tabla
        for etapa_info in tablas_etapas:
            etapa_num = etapa_info["etapa"]
            etapa_nombre = etapa_info["nombre"]
            filas = etapa_info["filas"]

            # Contenedor visual (LabelFrame) con padding para diferenciar cada etapa
            lf_etapa = ttk.LabelFrame(self.scrollable_frame, text=f" {etapa_nombre} (Etapa {etapa_num}) ", padding=10)
            lf_etapa.pack(fill="x", expand=True, pady=8)
            lf_etapa.columnconfigure(0, weight=1)

            # Definición de columnas para el Treeview
            columns = ("estado", "decision", "estado_sig", "val_acumulado", "optimo_etapa")
            tree = ttk.Treeview(lf_etapa, columns=columns, show="headings", height=min(max(len(filas), 3), 6))
            
            # Encabezados de la tabla
            tree.heading("estado", text="Estado (s)")
            tree.heading("decision", text="Decisión (x)")
            tree.heading("estado_sig", text="Estado Sig. (s_sig)")
            tree.heading("val_acumulado", text="Valor Acumulado")
            tree.heading("optimo_etapa", text="Óptimo f*_k(s)")

            # Anchos y alineación de columnas
            tree.column("estado", width=80, anchor="center")
            tree.column("decision", width=90, anchor="center")
            tree.column("estado_sig", width=100, anchor="center")
            tree.column("val_acumulado", width=110, anchor="center")
            tree.column("optimo_etapa", width=100, anchor="center")

            # Scrollbar interno para la tabla si contiene muchas evaluaciones
            tree_scroll = ttk.Scrollbar(lf_etapa, orient="vertical", command=tree.yview)
            tree.configure(yscrollcommand=tree_scroll.set)

            tree.grid(row=0, column=0, sticky="nsew")
            tree_scroll.grid(row=0, column=1, sticky="ns")

            # Insertar los datos evaluados en el Treeview
            for fila in filas:
                s = fila["estado"]
                val_opt = fila["valor_optimo"]
                evaluaciones = fila["evaluaciones"]

                if not evaluaciones:
                    tree.insert("", "end", values=(s, "-", "-", "-", val_opt))
                else:
                    for ev in evaluaciones:
                        dec = ev["decision"]
                        s_sig = ev["estado_sig"] if ev["estado_sig"] is not None else "Infactible"
                        v_ac = ev["valor_acumulado"]
                        tree.insert("", "end", values=(s, dec, s_sig, v_ac, val_opt))