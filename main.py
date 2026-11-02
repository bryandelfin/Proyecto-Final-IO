# Punto de entrada principal de la aplicación
# Método Gráfico - Investigación de Operaciones
# Grupo 10
import sys
import os
import tkinter as tk

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Configurar rutas para acceder a los módulos del proyecto
sys.path.insert(0, os.path.join(BASE_DIR, "src", "grafico"))
sys.path.insert(0, os.path.join(BASE_DIR, "src", "menu"))

from estilos import aplicar_estilos_globales
from menu import Menu

# Opción elegida en el menú de bienvenida
seleccion = {"tipo": None}


def iniciar_interfaz_principal(tipo_metodo):
    """Guarda la opción elegida; al cerrarse el menú se abre el panel."""
    seleccion["tipo"] = tipo_metodo


def abrir_panel(tipo_metodo):
    """Abre la interfaz del método gráfico con la opción seleccionada."""
    import importlib

    import logica_restricciones
    import panel_entrada

    # Al volver al menú, el panel anterior fue destruido: se reconstruye.
    if getattr(panel_entrada, "_iniciado", False):
        importlib.reload(panel_entrada)
    panel_entrada._iniciado = True
    logica_restricciones.entradas_restricciones.clear()

    aplicar_estilos_globales()

    if tipo_metodo == "comprar":
        def cargar_ejemplo_compra():
            panel_entrada.combo_ejemplos.current(0)
            panel_entrada.cargar_ejemplo_seleccionado(
                panel_entrada.canvas,
                panel_entrada.frame_contenedor_restricciones,
            )

        panel_entrada.root.after(200, cargar_ejemplo_compra)

    panel_entrada.root.mainloop()

    # True si el usuario pulsó "Volver al menú".
    return getattr(panel_entrada.root, "volver_al_menu", False)


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
