# Elementos visuales adicionales del plano
# Método Gráfico - Investigación de Operaciones
#
# Leyenda de colores de restricciones y sombreado de la región factible.
# No modifica la lógica ni el dibujo existente.

import plano_cartesiano

COLORES_RESTRICCIONES = ["green", "blue", "orange", "purple", "brown", "magenta"]
COLOR_REGION = "#15FF00"
OPERADORES = {"<=": "≤", ">=": "≥", "=": "="}


def _numero(valor):
    redondeado = round(valor, 4)
    if abs(redondeado - round(redondeado)) < 1e-9:
        return str(int(round(redondeado)))
    return f"{redondeado:g}"


def _ecuacion(a, b, op, c):
    """Formatea una restricción, por ejemplo: 2X1 - 3X2 ≥ 0."""
    partes = []
    for coeficiente, variable in ((a, "X1"), (b, "X2")):
        if abs(coeficiente) < 1e-9:
            continue
        valor = abs(coeficiente)
        cuerpo = variable if abs(valor - 1) < 1e-9 else f"{_numero(valor)}{variable}"
        if not partes:
            partes.append(("-" if coeficiente < 0 else "") + cuerpo)
        else:
            partes.append(f"{'-' if coeficiente < 0 else '+'} {cuerpo}")
    if not partes:
        partes.append("0")
    return f"{' '.join(partes)} {OPERADORES.get(op, op)} {_numero(c)}"


def _recortar(poligono, a, b, op, c, tolerancia=1e-9):
    """Recorta un polígono convexo contra una restricción (Sutherland-Hodgman)."""
    if op == ">=":
        a, b, c = -a, -b, -c

    salida = []
    total = len(poligono)
    for i in range(total):
        p = poligono[i]
        q = poligono[(i + 1) % total]
        vp = a * p[0] + b * p[1] - c
        vq = a * q[0] + b * q[1] - c
        dentro_p = vp <= tolerancia
        dentro_q = vq <= tolerancia

        if dentro_p:
            salida.append(p)
        if dentro_p != dentro_q:
            denominador = vp - vq
            t = vp / denominador if abs(denominador) > 1e-12 else 0.0
            salida.append((p[0] + t * (q[0] - p[0]), p[1] + t * (q[1] - p[1])))
    return salida


def sombrear_region_factible(canvas, restricciones, puntos_factibles):
    """Sombrea la intersección visible de todas las restricciones."""
    ancho, alto = plano_cartesiano.obtener_limites_canvas(canvas)
    escala, origen_x, origen_y = plano_cartesiano.calcular_escala_y_origen(
        restricciones, puntos_factibles, ancho, alto
    )
    if escala <= 0:
        return

    x_max = max(0.0, (ancho - origen_x) / escala)
    y_max = max(0.0, origen_y / escala)
    if x_max <= 0 or y_max <= 0:
        return

    poligono = [(0.0, 0.0), (x_max, 0.0), (x_max, y_max), (0.0, y_max)]
    for a, b, op, c in list(restricciones) + [(1, 0, ">=", 0), (0, 1, ">=", 0)]:
        if op == "=":
            continue
        poligono = _recortar(poligono, a, b, op, c)
        if not poligono:
            return

    coordenadas = []
    for x, y in poligono:
        px, py = plano_cartesiano.convertir_coordenadas(x, y, origen_x, origen_y, escala)
        coordenadas.extend((px, py))

    if len(coordenadas) >= 6:
        item = canvas.create_polygon(
            coordenadas,
            fill=COLOR_REGION,
            stipple="gray50",
            outline="",
            tags="region_factible",
        )
        canvas.tag_lower(item)


def dibujar_leyenda(canvas, restricciones):
    """Dibuja una leyenda con el color y la ecuación de cada restricción."""
    if not restricciones:
        return

    ancho, _alto = plano_cartesiano.obtener_limites_canvas(canvas)
    textos = [
        f"R{i + 1}: {_ecuacion(a, b, op, c)}"
        for i, (a, b, op, c) in enumerate(restricciones)
    ]
    textos.append("Región factible")

    x0 = 60
    y0 = 10
    ancho_texto = max(len(texto) for texto in textos) * 6 + 50
    ancho_caja = min(max(ancho_texto, 170), max(170, ancho - x0 - 12))
    alto_caja = 30 + 16 * len(textos) + 8

    canvas.create_rectangle(
        x0, y0, x0 + ancho_caja, y0 + alto_caja,
        fill="white", outline="#c9c9c9", tags="leyenda",
    )
    canvas.create_text(
        x0 + 8, y0 + 8,
        text="Restricciones y región", anchor="nw",
        font=("Arial", 8, "bold"), tags="leyenda",
    )

    fila_y = y0 + 28
    for i, texto in enumerate(textos):
        if i < len(restricciones):
            color = COLORES_RESTRICCIONES[i % len(COLORES_RESTRICCIONES)]
            canvas.create_line(
                x0 + 8, fila_y + 6, x0 + 28, fila_y + 6,
                fill=color, width=3, tags="leyenda",
            )
        else:
            canvas.create_rectangle(
                x0 + 8, fila_y, x0 + 28, fila_y + 12,
                fill=COLOR_REGION, stipple="gray50", outline="#7fbf86", tags="leyenda",
            )
        canvas.create_text(
            x0 + 34, fila_y + 6,
            text=texto, anchor="w",
            font=("Arial", 8), tags="leyenda",
        )
        fila_y += 16
