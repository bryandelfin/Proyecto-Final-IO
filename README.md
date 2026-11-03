# Proyecto Final IO

Aplicación educativa de Investigación de Operaciones (IO) con interfaz gráfica en
**Tkinter** para resolver dos tipos de problemas:

- **Método gráfico** (programación lineal de 2 variables).
- **Programación dinámica** (modelo de inventarios de café, procedimiento hacia atrás).

Al iniciar, la aplicación muestra un menú de bienvenida con dos opciones:
**"Cuánto comprar - (Programación Dinámica)"** y
**"Cuánto producir - (Método Gráfico)"**.

## Inicio rápido

Requisitos: Python 3.11 o superior, Tkinter y Git. En Windows, abre PowerShell;
en macOS o Linux, abre una terminal:

```bash
git clone https://github.com/bryandelfin/Proyecto-Final-IO.git
cd Proyecto-Final-IO
python -m venv .venv
```

Activa el entorno e instala las dependencias:

```powershell
# Windows (PowerShell)
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

```bash
# macOS o Linux
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Inicia la aplicación desde la carpeta del proyecto:

```bash
python main.py
```

En Windows también puedes usar `py` en lugar de `python`. Si PowerShell bloquea
la activación del entorno, ejecuta
`Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` y vuelve a activar.
Consulta [Instalación](#instalación) para detalles de Tkinter y solución de
problemas.

## Características

### Método gráfico (`Cuánto producir - (Método Gráfico)`)
- Captura de variables, función objetivo y restricciones.
- Soporta operadores `<=`, `>=`, `=` y agrega automáticamente la no-negatividad.
- Dibuja ejes, malla, restricciones, región factible, vértices y punto óptimo.
- Detecta óptimo único, óptimos alternativos, infactible y no acotado.
- Incluye 3 ejemplos precargados: editable, infactible y con óptimos alternativos.
- Calcula el valor óptimo `Z`, clasifica el problema y muestra el detalle en un
  panel de resultados.
- Para soluciones óptimas únicas, presenta análisis de sensibilidad: precios
  sombra, rangos de coeficientes y rangos de los lados derechos.
- Contrasta los resultados con SciPy cuando está instalado.

### Programación dinámica (`Cuánto comprar - (Programación Dinámica)`)
- Modelo de inventarios de café con 1 a 8 etapas.
- Parámetros globales: inventario inicial, inventario final, capacidad y paso de discretización.
- Parámetros por etapa: demanda, precio de compra, costo de almacenamiento y compra máxima.
- Resuelve con procedimiento hacia atrás y muestra las tablas paso a paso por etapa.
- Presenta la ruta de decisiones y el valor óptimo global del modelo.
- Contrasta el resultado con una verificación independiente basada en SciPy.

## Especificación de métodos

### Método gráfico
- **Entrada:** coeficientes de la función objetivo, tipo de optimización
  (maximizar o minimizar) y de 1 a 8 restricciones con coeficientes, operador
  (`<=`, `>=`, `=`) y lado derecho. Se asume `X1, X2 >= 0`.
- **Proceso:** calcula las intersecciones entre rectas, filtra los vértices
  factibles y evalúa `Z` en cada uno.
- **Salida:** gráfico con restricciones, región factible y vértices; tabla de
  puntos evaluados; solución óptima y clasificación del caso (único, alternativo,
  infactible o no acotado). El análisis de sensibilidad está disponible cuando
  existe un óptimo único.

### Programación dinámica
- **Entrada:** inventario inicial y final, capacidad máxima, paso de
  discretización, número de etapas (1 a 8) y, por etapa, demanda, precio de
  compra, costo de almacenamiento y compra máxima.
- **Proceso:** procedimiento hacia atrás sobre los estados de inventario.
- **Salida:** tablas paso a paso por etapa, ruta de decisiones y valor óptimo.
  El resultado se contrasta con una verificación cruzada basada en SciPy. Los
  parámetros deben permitir estados y decisiones dentro de los límites de
  inventario configurados; si no existe un plan factible, se informa ese estado.

## Requerimientos

- **Python 3.11 o superior**. El proyecto se ha ejecutado con Python 3.14.5.
- **Tkinter/Tcl-Tk** para la interfaz gráfica. Normalmente se incluye con Python
  en Windows y macOS. En Debian o Ubuntu puedes instalarlo con:
  ```bash
  sudo apt-get install python3-tk
  ```
- **Dependencias de Python:** instala `requirements.txt` para habilitar SciPy,
  NumPy y las demás dependencias incluidas. La aplicación puede abrirse sin ellas,
  pero las verificaciones cruzadas requieren NumPy y SciPy.
- **Entorno gráfico:** se requiere una sesión de escritorio activa para abrir las
  ventanas de Tkinter; no se puede mostrar la interfaz en una terminal headless.

La lógica principal de ambos métodos usa la biblioteca estándar (`math`). La
verificación cruzada utiliza SciPy y NumPy. Las dependencias y sus versiones
exactas están declaradas en `requirements.txt`.

## Estructura del proyecto

```
Proyecto-Final-IO/
├── main.py                          # Punto de entrada (menú + paneles)
├── estilos.py                       # Estilos globales de la interfaz
├── requirements.txt                 # Dependencias del proyecto
├── README.md
├── docs/
│   └── especificaciones-grafico.md   # Especificación del método gráfico
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
    │   ├── panel_sensibilidad.py    # Presentación del análisis de sensibilidad
    │   ├── analisis_sensibilidad.py # Cálculo de rangos y precios sombra
    │   ├── plano_cartesiano.py      # Dibujo del plano y restricciones
    │   ├── verificador.py           # Verificación cruzada de resultados
    │   └── visual_extra.py          # Sombreo de región factible y leyenda
    ├── dinamica/                    # Programación dinámica
    │   ├── ejemplos_dinamica.py     # Ejemplos de inventario
    │   ├── logica_programacion_dinamica.py  # Algoritmo hacia atrás
    │   ├── panel_formulario.py              # Ventana principal de PD
    │   └── panel_tablas.py                  # Tablas paso a paso
    └── test/                        # Pruebas automatizadas (sin abrir la GUI)
        ├── test_sensibilidad.py
        └── test_verificador.py
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
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Si PowerShell bloquea la activación:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

**Linux/macOS:**
```powershell
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar dependencias

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

En Windows, si el comando `python` no está asociado a Python, utiliza `py -m`
para los comandos de Python. El entorno virtual evita modificar paquetes
globales del sistema.

> Asegúrate de tener Tkinter disponible (ver [Requerimientos](#requerimientos)).

## Ejecución

Desde la raíz del proyecto y con el entorno virtual activado:

```bash
python main.py
```

Si no creaste un entorno virtual, usa el lanzador disponible en tu sistema. Por
ejemplo, en Linux/macOS:

```bash
python3 main.py
```

Se abrirá el **menú de bienvenida**. Desde allí puedes elegir:

1. **"Cuánto producir - (Método Gráfico)"** para abrir el método gráfico.
2. **"Cuánto comprar - (Programación Dinámica)"** para abrir programación dinámica.
3. En cada panel, **"Volver al menú"** regresa a la bienvenida.

> Ejecuta siempre `main.py` desde la raíz. Los módulos internos se cargan
> agregando `src/` al `sys.path` automáticamente; no es necesario mover archivos.

## Uso de la aplicación

### Método gráfico ("Cuánto producir - (Método Gráfico)")

1. Selecciona **Maximizar** o **Minimizar** e ingresa los nombres y coeficientes de `X1` y `X2`.
2. Indica el número de restricciones (1-8), pulsa **Generar** y completa coeficientes, operador y lado derecho.
3. Opcionalmente, carga un ejemplo desde el combobox **Ejemplos**.
4. Pulsa **Resolver** para graficar restricciones, región factible, vértices y solución óptima.
5. Pulsa **Limpiar** para reiniciar los campos y el plano.

### Programación dinámica ("Cuánto comprar - (Programación Dinámica)")

1. Completa los datos generales y los parámetros globales de inventario.
2. Define el número de etapas (1-8) y pulsa **Generar Campos por Etapa**.
3. Ingresa demanda, precio de compra, costo de almacenamiento y compra máxima por etapa.
4. Pulsa **Resolver DP** para ver las tablas paso a paso en el panel derecho.
5. Pulsa **Limpiar** para restaurar los valores por defecto.

## Pruebas

Las pruebas automáticas validan el método gráfico, la programación dinámica, la
verificación cruzada y el análisis de sensibilidad. No necesitan mostrar la
interfaz gráfica. Ejecuta desde la raíz del proyecto con las dependencias
instaladas:

```bash
python -m pytest src/test -v
```

Requieren `pytest`, `numpy` y `scipy` (incluidos en `requirements.txt`).

## Solución de problemas

- **`ModuleNotFoundError` al ejecutar un módulo interno**: ejecuta `python main.py`
  desde la raíz del proyecto, no desde dentro de `src/`.
- **`No module named tkinter` en Linux**: instala el paquete del sistema
  (`sudo apt-get install python3-tk` en Debian/Ubuntu) y vuelve a intentar.
- **`No module named tkinter` en Windows**: instala o modifica Python desde
  python.org y asegúrate de incluir Tcl/Tk.
- **Error al instalar SciPy/NumPy**: confirma que estás usando Python 3.11 o
  superior y actualiza `pip` dentro del entorno virtual.
- **Interfaz no visible en servidor remoto/terminal headless**: Tkinter necesita
  un escritorio gráfico; ejecuta la aplicación en una sesión local con GUI.
- **PowerShell no permite activar el entorno**: usa el comando de
  `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` mostrado arriba.
- **La aplicación no abre**: verifica que estés usando Python 3.10 o superior con
  `python --version`.

## Tecnologías

- [Python](https://www.python.org/) 3.10+
- [Tkinter](https://docs.python.org/3/library/tkinter.html) (interfaz gráfica)
- `math` (biblioteca estándar para los cálculos)
- [NumPy](https://numpy.org/) y [SciPy](https://scipy.org/) (verificación cruzada)
- [pytest](https://pytest.org/) (pruebas automáticas)
