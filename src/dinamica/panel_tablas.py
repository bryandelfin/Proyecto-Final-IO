# Módulo exclusivo para la visualización de tablas paso a paso (Treeview) y Solución Óptima
import tkinter as tk
from tkinter import ttk

class PanelTablasDinamicas:
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame
        self.setup_ui()

    def setup_ui(self):
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

        self.canvas.bind('<Configure>', lambda event: self.canvas.itemconfig(self.window_id, width=event.width))

        self.label_inicial = ttk.Label(
            self.scrollable_frame, 
            text="Configure los parámetros en el panel izquierdo y haga clic en 'Resolver DP'\npara visualizar el desglose paso a paso y la solución óptima.", 
            font=("Segoe UI", 10),
            foreground="#555555"
        )
        self.label_inicial.pack(pady=40, padx=20)

    def mostrar_tablas(self, resultado_dp):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        tablas_etapas = resultado_dp.get("tablas_etapas", [])
        ruta_optima = resultado_dp.get("ruta_optima", [])
        valor_optimo = resultado_dp.get("valor_optimo", 0)
        tipo_opt = resultado_dp.get("tipo_opt", "Optimización")

        if not tablas_etapas:
            lbl = ttk.Label(self.scrollable_frame, text="No hay datos de etapas para mostrar.", font=("Segoe UI", 10))
            lbl.pack(pady=20)
            return

        # ==========================================
        # 1. TARJETA DE SOLUCIÓN ÓPTIMA GLOBAL
        # ==========================================
        frame_resumen = ttk.LabelFrame(self.scrollable_frame, text=" 🏆 Solución Óptima Global ", padding=12)
        frame_resumen.pack(fill="x", expand=True, pady=(0, 15))
        frame_resumen.columnconfigure(1, weight=1)

        ttk.Label(frame_resumen, text=f"Resultado ({tipo_opt}):", font=("Segoe UI", 9, "bold")).grid(row=0, column=0, sticky="w", padx=5, pady=2)
        lbl_val = ttk.Label(frame_resumen, text=f"{valor_optimo}", font=("Segoe UI", 11, "bold"), foreground="#B8912F")
        lbl_val.grid(row=0, column=1, sticky="w", padx=5, pady=2)

        ttk.Label(frame_resumen, text="Ruta de Decisiones:", font=("Segoe UI", 9, "bold")).grid(row=1, column=0, sticky="nw", padx=5, pady=2)
        
        # Detalle de la ruta paso a paso
        texto_ruta = ""
        for paso in ruta_optima:
            et = paso["etapa"]
            st = paso["estado"]
            dec = paso["decision_optima"]
            texto_ruta += f"• Etapa {et}: Estando en s = {st} ➔ Tomar decisión x = {dec}\n"
        
        if not texto_ruta:
            texto_ruta = "No se pudo determinar una ruta óptima factible."

        lbl_ruta = ttk.Label(frame_resumen, text=texto_ruta.strip(), font=("Segoe UI", 9), foreground="#2B2D42")
        lbl_ruta.grid(row=1, column=1, sticky="w", padx=5, pady=2)

        # ==========================================
        # 2. DESGLOSE PASO A PASO POR ETAPAS
        # ==========================================
        lbl_titulo = ttk.Label(
            self.scrollable_frame, 
            text="Evaluación Detallada por Etapas (Procedimiento Hacia Atrás)", 
            font=("Segoe UI", 11, "bold"),
            foreground="#1D3557"
        )
        lbl_titulo.pack(anchor="w", pady=(5, 10))

        for etapa_info in tablas_etapas:
            etapa_num = etapa_info["etapa"]
            etapa_nombre = etapa_info["nombre"]
            filas = etapa_info["filas"]

            lf_etapa = ttk.LabelFrame(self.scrollable_frame, text=f" {etapa_nombre} (Etapa {etapa_num}) ", padding=10)
            lf_etapa.pack(fill="x", expand=True, pady=8)
            lf_etapa.columnconfigure(0, weight=1)

            columns = ("estado", "decision", "estado_sig", "val_acumulado", "optimo_etapa")
            tree = ttk.Treeview(lf_etapa, columns=columns, show="headings", height=min(max(len(filas) * 2, 4), 8))
            
            tree.heading("estado", text="Estado (s)")
            tree.heading("decision", text="Decisión (x)")
            tree.heading("estado_sig", text="Estado Sig. (s_sig)")
            tree.heading("val_acumulado", text="Valor Acumulado")
            tree.heading("optimo_etapa", text="Óptimo f*_k(s)")

            tree.column("estado", width=80, anchor="center")
            tree.column("decision", width=90, anchor="center")
            tree.column("estado_sig", width=100, anchor="center")
            tree.column("val_acumulado", width=110, anchor="center")
            tree.column("optimo_etapa", width=100, anchor="center")

            tree_scroll = ttk.Separator(lf_etapa, orient="vertical") # o scrollbar normal
            tree_scroll = ttk.Scrollbar(lf_etapa, orient="vertical", command=tree.yview)
            tree.configure(yscrollcommand=tree_scroll.set)

            tree.grid(row=0, column=0, sticky="nsew")
            tree_scroll.grid(row=0, column=1, sticky="ns")

            # Estilo de filas alternadas y resaltado de óptimos
            tree.tag_configure('optimo_row', background='#E8F5E9') # Verde claro sutil para decisiones óptimas

            for fila in filas:
                s = fila["estado"]
                val_opt = fila["valor_optimo"]
                decisiones_optimas = fila["decisiones_optimas"]
                evaluaciones = fila["evaluaciones"]

                if not evaluaciones:
                    tree.insert("", "end", values=(s, "-", "-", "-", val_opt))
                else:
                    for ev in evaluaciones:
                        dec = ev["decision"]
                        s_sig = ev["estado_sig"] if ev["estado_sig"] is not None else "Infactible"
                        v_ac = ev["valor_acumulado"]
                        
                        # Comprobar si esta decisión exacta es óptima para este estado
                        es_optima_actual = (dec in decisiones_optimas) and (v_ac == val_opt)
                        
                        tag = ('optimo_row',) if es_optima_actual else ()
                        tree.insert("", "end", values=(s, dec, s_sig, v_ac, val_opt), tags=tag)