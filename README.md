# Proyecto Final IO

Aplicación educativa para resolver problemas de Investigación de Operaciones (IO) mediante el **método gráfico** y con estructura preparada para **programación dinámica**. Implementada en Python con interfaz gráfica en Tkinter.

## Características

- **Método gráfico**: Captura de modelo matemático (variables, función objetivo, restricciones), graficado de restricciones en plano cartesiano, identificación de región factible, cálculo de vértices y obtención de solución óptima.
- **Interfaz intuitiva**: Formulario para definir variables, número de restricciones, tipo de optimización (Maximizar/Minimizar), visualización en canvas interactivo.
- **Validación de restricciones**: Soporta desigualdades `<=`, `>=`, `=`. Añade automáticamente restricciones de no-negatividad (`X1>=0`, `X2>=0`).
- **Visualización completa**: Dibuja ejes, malla, líneas de restricción, puntos factibles y punto óptimo resaltado con su valor Z.
- **Preparado para expansión**: Módulos separados (`src/grafico/`, `src/dinamica/`) para agregar programación dinámica próximamente.

## Requerimientos

### Software
- Python 3.10+ (probado con Python 3.14.3)
- pip (gestor de paquetes)
- Git (opcional, para clonar)

### Dependencias
Ver `requirements.txt`:
```
matplotlib==3.11.2
numpy==2.5.4
pytest==9.1.1
```

## Estructura de archivos

```
Proyecto-Final-IO/
├── .gitignore
├── main.py                    # Punto de entrada desde raíz
├── README.md
├── requirements.txt
├── data/                      # Datos de entrada/ejemplos
│   └── ejemplos/
├── docs/                      # Documentación
│   └── especificaciones-grafico.md
├── src/
│   ├── dinamica/              # Módulo para programación dinámica (en desarrollo)
│   └── grafico/               # Módulo método gráfico
│       ├── logica_metodo_grafico.py  # Lógica de resolución y búsqueda de óptimo
│       ├── logica_restricciones.py   # Generación dinámica de entradas de restricciones
│       └── panel_entrada.py          # Interfaz gráfica Tkinter
│       └── plano_cartesiano.py       # Dibujo y visualización en canvas
└── tests/                     # Pruebas unitarias (pytest)
```

## Instalación

### 1. Clonar el repositorio
```bash
git clone https://github.com/bryandelfin/Proyecto-Final-IO.git
cd "Proyecto-Final-IO"
```

### 2. Crear y activar entorno virtual

**Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Si hay error de políticas de ejecución:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

**Linux/MacOS:**
```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

## Ejecución

### Desde la raíz (recomendado)
```bash
python main.py
```

### Desde el módulo gráfico
```bash
cd src/grafico
python panel_entrada.py
```

## Uso de la aplicación

1. **Definir función objetivo**: Selecciona `Maximizar` o `Minimizar`. Ingresa nombres y coeficientes de `X1` y `X2`.
2. **Definir restricciones**: Selecciona número de restricciones (1-8) y pulsa `Generar`. Completa coeficientes, operador (`<=`, `>=`, `=`) y lado derecho.
3. **Resolver**: Pulsa `Resolver`. La aplicación graficará las restricciones, mostrará la región factible, puntos vértices y el punto óptimo con valor Z.
4. **Limpiar/Cargar ejemplo**: Usa los botones correspondientes según necesidad.

## Buenas prácticas

- **Entorno aislado**: Usar `.venv/` para evitar conflictos de dependencias.
- **Control de versiones**: Seguir convención de commits (`feat:`, `fix:`, `docs:`, `chore:`). No subir archivos generados (`__pycache__/`, `.venv/`).
- **Modularidad**: Lógica separada de interfaz (`logica_metodo_grafico.py`) facilita pruebas y mantenimiento.
- **Validación**: Se validan entradas numéricas, región factible y restricciones.
- **Ramas**: Desarrollo en ramas feature (ej. `interfaz-grafico`) con merges a `main` vía PR/revisión.
- **Testing**: Ejecutar pruebas con `pytest` antes de hacer commit/push.
- **Documentación**: Mantener `README.md` y `docs/` actualizados.

## Pruebas

```bash
pytest
```

## Contribución

1. Crear rama desde `main`: `git checkout -b feature/nombre-feature`
2. Realizar cambios y commits descriptivos
3. Subir rama: `git push -u origin feature/nombre-feature`
4. Abrir Pull Request en GitHub

## Tecnologías

- [Python](https://www.python.org/) - Lenguaje base
- [Tkinter](https://docs.python.org/3/library/tkinter.html) - Interfaz gráfica
- [NumPy](https://numpy.org/), [Matplotlib](https://matplotlib.org/) - Soporte numérico/gráfico
- [pytest](https://docs.pytest.org/) - Framework de pruebas
