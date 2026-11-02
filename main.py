# Punto de entrada principal de la aplicación
# Método Gráfico - Investigación de Operaciones
# Grupo 10
import sys
import os
import tkinter as tk

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Configurar rutas para acceder a los módulos del proyecto
sys.path.insert(0, os.path.join(BASE_DIR, "src", "grafico"))
sys.path.insert(0, os.path.join(BASE_DIR, "src", "dinamica"))
sys.path.insert(0, os.path.join(BASE_DIR, "src", "menu"))

from estilos import aplicar_estilos_globales
from menu import Menu
# Opción elegida en el menú de bienvenida
seleccion = {"tipo": None}


def iniciar_interfaz_principal(tipo_metodo):
    """Guarda la opción elegida; al cerrarse el menú se abre el panel."""
    seleccion["tipo"] = tipo_metodo


def abrir_panel(tipo_metodo):
    """Abre SOLO el panel que corresponde al botón elegido en el menú."""
    import importlib

    # Cada panel crea su propia ventana (root = Tk()) en el mismo instante en
    # que se importa. Por eso hay que importar únicamente el que se eligió:
    # si se importaran los dos, se abrirían dos ventanas a la vez.
    if tipo_metodo == "comprar":
        nombre_modulo = "panel_formulario"  # Programación dinámica
    else:
        nombre_modulo = "panel_entrada"  # Método gráfico

    # Al volver al menú, la ventana anterior de ese panel fue destruida.
    # Se descarta el módulo en memoria para que, al importarlo de nuevo,
    # se construya una ventana nueva.
    sys.modules.pop(nombre_modulo, None)
    panel = importlib.import_module(nombre_modulo)

    if tipo_metodo != "comprar":
        import logica_restricciones

        logica_restricciones.entradas_restricciones.clear()

    aplicar_estilos_globales()
    panel.root.mainloop()

    # True si el usuario pulsó "Volver al menú" en ESE panel.
    return getattr(panel.root, "volver_al_menu", False)


if __name__ == "__main__":
    while True:
        # Ventana de bienvenida
        seleccion["tipo"] = None
        root_bienvenida = tk.Tk()
        aplicar_estilos_globales()
        Menu(root_bienvenida, iniciar_interfaz_principal)
        root_bienvenida.mainloop()

        # Si cerró el menú sin elegir, terminar la aplicación
        if seleccion["tipo"] is None:
            break

        # Abrir el panel; si no pidió volver al menú, terminar
        if not abrir_panel(seleccion["tipo"]):
            break