# Panel visual del análisis de sensibilidad del método gráfico.
# Muestra precios sombra, rangos y una interpretación breve para la decisión.

import tkinter as tk
from tkinter import ttk

from analisis_sensibilidad import analizar_sensibilidad


def _formatear(valor, decimales=4):
    if valor is None:
        return "sin límite"
    redondeado = round(valor, decimales)
    if abs(redondeado) < 10 ** (-decimales):
        redondeado = 0.0
    return f"{redondeado:g}"


def _nombre_variable(nombre, indice):
    limpio = (nombre or "").strip()
    if not limpio or limpio.upper() in ("X1", "X2"):
        return f"Variable {indice}"
    return limpio


class PanelSensibilidad:
    """Muestra el análisis de sensibilidad junto a la tabla de resultados."""

    def __init__(self, parent):
        self.frame = ttk.LabelFrame(parent, text=" Análisis de sensibilidad ", padding=4)
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)

        self.texto = tk.Text(
            self.frame,
            height=13,
            width=58,
            wrap="word",
            font=("Segoe UI", 9),
            background="#F7F5EF",
            relief="flat",
            state="disabled",
        )
        scroll = ttk.Scrollbar(self.frame, orient="vertical", command=self.texto.yview)
        self.texto.configure(yscrollcommand=scroll.set)

        self.texto.grid(row=0, column=0, sticky="nsew")
        scroll.grid(row=0, column=1, sticky="ns")

        self.texto.tag_configure("titulo", font=("Segoe UI", 9, "bold"),
                                 foreground="#1D3557")
        self.texto.tag_configure("seccion", font=("Segoe UI", 9, "bold"),
                                 foreground="#B8912F")
        self.texto.tag_configure("nota", font=("Segoe UI", 8, "italic"),
                                 foreground="#6B6B6B")
        self.texto.tag_configure("alerta", font=("Segoe UI", 9, "bold"),
                                 foreground="#B00020")
        self.limpiar()

    def _escribir(self, texto, etiqueta=None):
        self.texto.insert("end", texto, etiqueta or ())

    def limpiar(self):
        self.texto.configure(state="normal")
        self.texto.delete("1.0", "end")
        self.texto.insert(
            "end",
            "Resuelva el modelo para ver precios sombra, rangos e interpretación.",
            "nota",
        )
        self.texto.configure(state="disabled")

    def actualizar(self, resultado, c1, c2):
        tipo_opt = resultado.get("tipo_opt", "")
        restricciones = resultado.get("restricciones", [])

        if c1 is None or c2 is None or not restricciones:
            self.limpiar()
            return

        analisis = analizar_sensibilidad(c1, c2, tipo_opt, restricciones)

        self.texto.configure(state="normal")
        self.texto.delete("1.0", "end")

        self._escribir("Análisis de sensibilidad\n", "titulo")

        if not analisis.get("disponible"):
            self._escribir(analisis.get("mensaje", "No disponible."), "alerta")
            self._escribir(
                "\n\nEl análisis de sensibilidad requiere una solución óptima única.",
                "nota",
            )
            self.texto.configure(state="disabled")
            return

        base = analisis["resultado"]
        punto = base["puntos_optimos"][0]
        nombre_v1 = _nombre_variable(resultado.get("nombre_v1"), 1)
        nombre_v2 = _nombre_variable(resultado.get("nombre_v2"), 2)

        self._escribir(
            f"Solución óptima: {nombre_v1} = {_formatear(punto[0])}, "
            f"{nombre_v2} = {_formatear(punto[1])}  |  "
            f"Z = {_formatear(base['mejor_z'])} ({tipo_opt})\n"
        )

        activas = [f"R{item['indice']}" for item in analisis["precios_sombra"]
                   if item["activa"]]
        if activas:
            self._escribir(f"Restricciones activas: {', '.join(activas)}\n\n")
        else:
            self._escribir("Restricciones activas: ninguna\n\n")

        self._escribir("Precios sombra\n",
                       "seccion")
        for item in analisis["precios_sombra"]:
            self._escribir(
                f"• R{item['indice']} ({item['operador']} {_formatear(item['lado_derecho'])}): "
                f"{_formatear(item['precio'])}\n"
                f"  {item['frase']}\n"
            )

        self._escribir("\nRangos de coeficientes de la función objetivo\n",
                       "seccion")
        nombres_coeficientes = [nombre_v1, nombre_v2]
        for item in analisis["rangos_coeficientes"]:
            nombre = nombres_coeficientes[item["indice"] - 1]
            self._escribir(
                f"• c{item['indice']} ({nombre}): "
                f"[{_formatear(item['min'])}, {_formatear(item['max'])}] "
                f"(actual {_formatear(item['actual'])})\n"
                f"  "
                f"{self._frase_rango_coeficiente(nombre, item['min'], item['max'])}\n"
            )

        self._escribir("\nRangos de las restricciones\n",
                       "seccion")
        for item in analisis["rangos_lado_derecho"]:
            self._escribir(
                f"• R{item['indice']}: "
                f"[{_formatear(item['min'])}, {_formatear(item['max'])}] "
                f"(actual {_formatear(item['actual'])})\n"
                f"  {self._frase_rango_lado_derecho(item['indice'], item['min'], item['max'])}\n"
            )

        palancas = [f"R{item['indice']}" for item in analisis["precios_sombra"]
                    if item["precio"] is not None and abs(item["precio"]) > 1e-7]
        self._escribir("\nResultado para la decisión\n", "seccion")
        if palancas:
            self._escribir(
                f"Las restricciones {', '.join(palancas)} son las que cambian Z si se "
                f"modifican; son las palancas para mejorar el resultado. Las demás no "
                f"limitan la decisión actual.\n"
            )
        else:
            self._escribir(
                "Ninguna restricción limita Z de forma marginal: modificar sus lados "
                "derechos no cambia la decisión actual.\n"
            )

        self.texto.configure(state="disabled")

    @staticmethod
    def _frase_rango_coeficiente(nombre, minimo, maximo):
        if minimo is None and maximo is None:
            return f"El plan óptimo no cambia para ningún valor de {nombre}."
        if minimo is None:
            return (f"El plan óptimo se mantiene si {nombre} es menor que "
                    f"{_formatear(maximo)}; si sube más, conviene revisar la decisión.")
        if maximo is None:
            return (f"El plan óptimo se mantiene si {nombre} es mayor que "
                    f"{_formatear(minimo)}; si baja más, conviene revisar la decisión.")
        return (f"El plan óptimo se mantiene mientras {nombre} esté entre "
                f"{_formatear(minimo)} y {_formatear(maximo)}; fuera de ese rango "
                f"conviene revisar la decisión.")

    @staticmethod
    def _frase_rango_lado_derecho(indice, minimo, maximo):
        if minimo is None and maximo is None:
            return f"El lado derecho de R{indice} no altera la base óptima actual."
        if minimo is None:
            return (f"El precio sombra de R{indice} es válido mientras su lado "
                    f"derecho sea menor que {_formatear(maximo)}.")
        if maximo is None:
            return (f"El precio sombra de R{indice} es válido mientras su lado "
                    f"derecho sea mayor que {_formatear(minimo)}.")
        return (f"El precio sombra de R{indice} es válido mientras su lado derecho "
                f"esté entre {_formatear(minimo)} y {_formatear(maximo)}.")
