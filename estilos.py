# Módulo de estilos globales para la interfaz Tkinter
# Método Gráfico - Investigación de Operaciones

from tkinter import ttk

def aplicar_estilos_globales():
    """
    Aplica estilos globales personalizados a todos los widgets ttk de la aplicación.
    Configura tema, colores, fuentes y efectos hover para mejorar la apariencia.
    """
    style = ttk.Style()
    
    # Forzar el tema 'clam' para permitir personalización completa de colores
    style.theme_use("clam")
    
    # Paleta de colores
    COLOR_BG_DARK = "#1D3557"      # Azul oscuro profesional para botones
    COLOR_BG_HOVER = "#457B9D"     # Azul más claro para efecto hover
    COLOR_TEXTO_BLANCO = "#FFFFFF" # Texto blanco
    COLOR_FONDO_PANEL = "#F1FAEE"  # Fondo suave para paneles
    COLOR_BORDE = "#A8DADC"        # Color de bordes
    
    # Configuración global de botones ttk.Button
    style.configure(
        "TButton",
        background=COLOR_BG_DARK,
        foreground=COLOR_TEXTO_BLANCO,
        font=("Segoe UI", 8, "bold"),
        padding=(6, 4),
        relief="flat",
        borderwidth=0,
    )
    
    # Efecto hover y pressed para botones
    style.map(
        "TButton",
        background=[("active", COLOR_BG_HOVER), ("pressed", "#1d2d44")],
        foreground=[("active", COLOR_TEXTO_BLANCO)],
    )
    
    # Configuración de etiquetas ttk.Label
    style.configure(
        "TLabel", 
        font=("Segoe UI", 8), 
        background=COLOR_FONDO_PANEL, 
        foreground="#2B2D42"
    )
    
    # Configuración de marcos y etiquetas de marco LabelFrame
    style.configure(
        "TLabelframe", 
        background=COLOR_FONDO_PANEL, 
        bordercolor=COLOR_BORDE
    )
    style.configure(
        "TLabelframe.Label",
        font=("Segoe UI", 9, "bold"),
        background=COLOR_FONDO_PANEL,
        foreground="#1D3557",
    )
    
    # Configuración de Combobox
    style.configure(
        "TCombobox", 
        padding=2, 
        fieldbackground="white",
        background="white"
    )
    
    # Configuración de Separator
    style.configure(
        "TSeparator",
        background=COLOR_BORDE
    )
