# Punto de entrada principal de la aplicación
# Método Gráfico - Investigación de Operaciones
# Grupo 10
import sys
import os

# Configurar ruta para acceder al módulo gráfico
grafico_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "src", "grafico")
sys.path.insert(0, grafico_dir)

# Importar estilos globales y módulo de interfaz
from estilos import aplicar_estilos_globales
import panel_entrada

if __name__ == "__main__":
    # Aplicar estilos globales a la interfaz
    aplicar_estilos_globales()
    # Iniciar bucle principal de la aplicación
    panel_entrada.root.mainloop()
