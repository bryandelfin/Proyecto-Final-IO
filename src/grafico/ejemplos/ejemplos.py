# Ejemplos para el método gráfico
# Método Gráfico - Investigación de Operaciones

# Ejemplo 1: Editable/Fácil (factible con solución única)
EJEMPLO_REAL = {
    "nombre": "Ejemplo 1 (Coffee Holding Co.)",
    "tipo_opt": "Minimizar",
    "x1_nombre": "Miles de libras de café Arábica a comprar",
    "x1_valor": 3.157,
    "x2_nombre": "Miles de libras de café Robusta a comprar",
    "x2_valor": 1.5803,
    "restricciones": [
        (1, 1, ">=", 44),
        (2, -3, ">=", 0),
        (-1, 4, ">=", 0),
        (1, 0, "<=", 36)
    ]
}

# Ejemplo 2: Infactible (sin región factible)
EJEMPLO_INFACTIBLE = {
    "nombre": "Ejemplo 2 (Infactible)",
    "tipo_opt": "Maximizar",
    "x1_nombre": "X1",
    "x1_valor": 2,
    "x2_nombre": "X2",
    "x2_valor": 3,
    "restricciones": [
        (1, 1, "<=", 2),
        (1, 1, ">=", 5),
    ]
}

# Ejemplo 3: Óptimos alternativos (función objetivo paralela a restricción activa)
EJEMPLO_OPTIMOS_ALTERNATIVOS = {
    "nombre": "Ejemplo 3 (Óptimos alternativos)",
    "tipo_opt": "Maximizar",
    "x1_nombre": "X1",
    "x1_valor": 4,
    "x2_nombre": "X2",
    "x2_valor": 6,
    "restricciones": [
        (2, 3, "<=", 12),
        (1, 0, "<=", 4),
        (0, 1, "<=", 3),
    ]
}

# Lista de todos los ejemplos
EJEMPLOS = [
    EJEMPLO_REAL,
    EJEMPLO_INFACTIBLE,
    EJEMPLO_OPTIMOS_ALTERNATIVOS,
]
