import sys, os
grafico_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "src", "grafico")
sys.path.insert(0, grafico_dir)
import panel_entrada
if __name__ == "__main__":
    panel_entrada.root.mainloop()