# Proyecto Final IO

Aplicación educativa de Investigación de Operaciones (IO) con interfaz gráfica en
**Tkinter** para resolver dos tipos de problemas:

- **Método gráfico** (programación lineal de 2 variables).
- **Programación dinámica** (modelo de inventarios de café, procedimiento hacia atrás).

Al iniciar, la aplicación muestra un menú de bienvenida donde se elige qué calcular.

## Características

### Método gráfico (`Cuánto producir`)
- Captura de variables, función objetivo y restricciones.
- Soporta operadores `<=`, `>=`, `=` y agrega automáticamente la no-negatividad.
- Dibuja ejes, malla, restricciones, región factible, vértices y punto óptimo.
- Incluye 3 ejemplos precargados: editable, infactible y con óptimos alternativos.
- Calcula el valor óptimo `Z` y muestra el detalle en un panel de resultados.

### Programación dinámica (`Cuánto comprar`)
- Modelo de inventarios de café con 1 a 8 etapas.
- Parámetros globales: inventario inicial, inventario final, capacidad y paso de discretización.
- Parámetros por etapa: demanda, precio de compra, costo de almacenamiento y compra máxima.
- Resuelve con procedimiento hacia atrás y muestra las tablas paso a paso por etapa.

## Requerimientos

- **Python 3.10 o superior** (probado con Python 3.14.3).
- **Tkinter** (incluido en la instalación oficial de Python en Windows/macOS).
  En Linux puede requerir el paquete del sistema:
  ```bash
  sudo apt install python3-tk
  ```

El proyecto **no usa dependencias externas de Python**: todo se implementa con la
biblioteca estándar (`tkinter`, `math`). Por eso `requirements.txt` solo contiene
comentarios y `pip install -r requirements.txt` no instala paquetes adicionales.

## Estructura del proyecto

```
Proyecto Final IO/
├── main.py                          # Punto de entrada (menú + paneles)
├── estilos.py                       # Estilos globales de la interfaz
├── requirements.txt                 # Sin dependencias externas
├── README.md
├── docs/
│   └── especificaciones-grafico.md
└── src/
    ├── menu/
    │   ├── __init__.py
    │   └── menu.py                  # Menú de bienvenida
    ├── grafico/                     # Método gráfico
    │   ├── ejemplos/
    │   │   ├── __init__.py
    │   │   └── ejemplos.py          # Ejemplos precargados
    │   ├── logica_metodo_grafico.py # Resolución y búsqueda del óptimo
    │   ├── logica_restricciones.py  # Entradas dinámicas de restricciones
    │   ├── panel_entrada.py         # Ventana principal del método gráfico
    │   ├── panel_resultados.py      # Tabla de resultados
    │   ├── plano_cartesiano.py      # Dibujo del plano y restricciones
    │   └── visual_extra.py          # Sombreo de región factible y leyenda
    └── dinamica/                    # Programación dinámica
        ├── logica_programacion_dinamica.py  # Algoritmo hacia atrás
        ├── panel_formulario.py              # Ventana principal de PD
        └── panel_tablas.py                  # Tablas paso a paso
```

## Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/bryandelfin/Proyecto-Final-IO.git
cd Proyecto-Final-IO
```

### 2. Crear y activar un entorno virtual (recomendado)

**Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Si PowerShell bloquea la activación:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

**Linux/macOS:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

> No se instalan paquetes externos porque el proyecto solo usa la biblioteca
> estándar. Asegúrate de tener Tkinter disponible (ver Requerimientos).

## Ejecución

Desde la raíz del proyecto:

```bash
python main.py
```

En Linux/macOS, si usaste `python3` para crear el entorno, ejecuta:

```bash
python3 main.py
```

Se abrirá el **menú de bienvenida**:

1. Elige **"Cuánto producir"** para abrir el método gráfico.
2. Elige **"Cuánto comprar"** para abrir programación dinámica.
3. Dentro de cada panel puedes usar **"Volver al menú"** para regresar.

> Ejecuta siempre `main.py` desde la raíz. Los módulos internos se cargan
> agregando `src/` al `sys.path` automáticamente; no es necesario mover archivos.

## Uso de la aplicación

### Método gráfico ("Cuánto producir")

1. Selecciona **Maximizar** o **Minimizar** e ingresa los nombres y coeficientes de `X1` y `X2`.
2. Indica el número de restricciones (1-8), pulsa **Generar** y completa coeficientes, operador y lado derecho.
3. Opcionalmente, carga un ejemplo desde el combobox **Ejemplos**.
4. Pulsa **Resolver** para graficar restricciones, región factible, vértices y solución óptima.
5. Pulsa **Limpiar** para reiniciar los campos y el plano.

### Programación dinámica ("Cuánto comprar")

1. Completa los datos generales y los parámetros globales de inventario.
2. Define el número de etapas (1-8) y pulsa **Generar Campos por Etapa**.
3. Ingresa demanda, precio de compra, costo de almacenamiento y compra máxima por etapa.
4. Pulsa **Resolver DP** para ver las tablas paso a paso en el panel derecho.
5. Pulsa **Limpiar** para restaurar los valores por defecto.

## Solución de problemas

- **`ModuleNotFoundError` al ejecutar un módulo interno**: ejecuta `python main.py`
  desde la raíz del proyecto, no desde dentro de `src/`.
- **`No module named tkinter` en Linux**: instala el paquete del sistema
  (`sudo apt install python3-tk`) y vuelve a intentar.
- **PowerShell no permite activar el entorno**: usa el comando de
  `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` mostrado arriba.
- **La aplicación no abre**: verifica que estés usando Python 3.10 o superior con
  `python --version`.

## Tecnologías

- [Python](https://www.python.org/) 3.10+
- [Tkinter](https://docs.python.org/3/library/tkinter.html) (interfaz gráfica)
- `math` (biblioteca estándar para los cálculos)
