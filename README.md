# pandas-time-series

Aplicación de terminal (TUI) construida con [Textual](https://textual.textualize.io/) para analizar la serie histórica de ventas de vehículos livianos en EE. UU. (**LTOTALNSA**). Muestra tablas con los datos originales y sus indicadores derivados, junto con gráficos que se generan como imágenes dentro de la propia terminal.

Proyecto basado en el reto [Pandas Time Series](https://roadmap.sh/projects/pandas-time-series) de [roadmap.sh](https://roadmap.sh/), que busca aprender cómo Pandas maneja fechas y series de tiempo.

# Demo
![Demo de la aplicación](https://github.com/LW-Homeless/Panda-Time-Series/blob/main/time-series.gif?raw=true)

## Sobre el reto de roadmap.sh

El reto propone trabajar con el dataset de ventas de vehículos livianos de FRED para entender `DatetimeIndex` y las herramientas de Pandas para series de tiempo (`.resample()`, `.shift()`, `.rolling()` y `.diff()`), sin construir ningún modelo. Sus requisitos y su estado en este proyecto:

<!-- TODO: revisa y ajusta los checks según lo que realmente implementaste en ProcessData. -->

- [x] Cargar el archivo Excel de FRED en un DataFrame de Pandas
- [x] Convertir la columna de fecha y usarla como índice
- [ ] Crear un rango de fechas con `pd.date_range()` y entender las frecuencias (`D`, `W`, `M`)
- [ ] Remuestrear los datos a totales mensuales y trimestrales
- [x] Desplazar la serie un período y calcular las diferencias entre períodos
- [x] Graficar la serie original y su media móvil en el mismo gráfico

A diferencia de la propuesta original (que sugiere Jupyter Notebook y Matplotlib), este proyecto presenta los resultados en una interfaz de terminal con Textual, mostrando los gráficos de Matplotlib como imágenes dentro de la propia terminal.

## Características

- Pantalla principal con dos zonas: un panel izquierdo con cuatro tablas y una grilla derecha con cinco gráficos.
- Tablas con los datos originales y tres indicadores derivados:
  - Datos originales (`TOTAL VTAs. NSA`)
  - Diferencia de ventas por año (`Diferencia x Año`)
  - Diferencia porcentual por año (`% de Cambio Anual`)
  - Media móvil (`Media Movil`)
- Carga progresiva: cada panel muestra un indicador de carga y las tablas aparecen una tras otra.
- Gráficos de `TOTAL VTAs. NSA` frente a su media móvil, con una línea de referencia en el promedio del período.
- Los 51 años de la serie (1976–2026) se reparten en cinco gráficos consecutivos, cada uno con su rango de años en el título.
- Los gráficos se generan con `matplotlib` y se muestran como imágenes reales en la terminal mediante `textual-image`.
- Estilos personalizados en un archivo `.tcss`.

## Fuente de datos

Los datos provienen de la serie **Light Weight Vehicle Sales (LTOTALNSA)** de FRED:

- **Fuente original:** U.S. Bureau of Economic Analysis (BEA)
- **Distribuida por:** FRED, Federal Reserve Bank of St. Louis
- **Unidades:** miles de unidades, sin ajuste estacional (NSA)
- **Frecuencia original:** mensual, desde enero de 1976
- **Enlace:** <https://fred.stlouisfed.org/series/LTOTALNSA>

<!-- TODO: explica cómo obtiene los datos ProcessData (CSV descargado a mano, API de FRED, etc.)
     y dónde debe ubicarse el archivo si aplica. -->

### Nota sobre el año 2026

<!-- TODO: confirma que ProcessData agrupa los datos mensuales por año. Si es así, deja esta nota. -->
La serie publicada llega hasta agosto de 2026, por lo que el año 2026 contiene solo datos parciales (enero a agosto). Sus valores anuales, y las diferencias calculadas respecto al año anterior, no son comparables con los de un año completo.

## Indicadores calculados

<!-- TODO: completa con la fórmula real que usa ProcessData. -->

| Indicador | Columna | Descripción |
|---|---|---|
| Ventas | `LTOTALNSA` | Ventas de vehículos livianos (miles de unidades) |
| Diferencia anual | `Anual Difference` | Diferencia respecto al año anterior |
| Variación porcentual anual | `Annual PCT Change` | Cambio porcentual respecto al año anterior |
| Media móvil | `Media Movil` | Media móvil de `LTOTALNSA` (ventana: _por definir_) |

## Requisitos

- Python <!-- TODO: versión, por ejemplo 3.11 o superior -->
- Dependencias principales:
  - [`textual`](https://pypi.org/project/textual/)
  - [`pandas`](https://pypi.org/project/pandas/)
  - [`matplotlib`](https://pypi.org/project/matplotlib/)
  - [`textual-image`](https://pypi.org/project/textual-image/)

### Terminal recomendada

Los gráficos se muestran como imágenes mediante `textual-image`, que elige automáticamente el mejor protocolo que soporte tu terminal (protocolo gráfico de Kitty o Sixel). Si la terminal no soporta ninguno, la librería recurre a una representación con caracteres Unicode, con menor calidad visual pero funcional.

- **Linux:** Kitty, WezTerm, foot o Konsole ofrecen buena calidad de imagen. GNOME Terminal usará el modo de respaldo.
- **Windows:** Windows Terminal (versión 1.22 o superior, con soporte Sixel) o WezTerm. La consola clásica (`cmd.exe`) usará el modo de respaldo.

## Instalación

```bash
git clone https://github.com/LW-Homeless/Panda-Time-Series.git
cd Time_Series

python -m venv .venv

# Windows
.venv\Scripts\activate
# Linux / macOS
source .venv/bin/activate

pip install -r requirements.txt
```

<!-- TODO: si no tienes requirements.txt, créalo con: pip freeze > requirements.txt
     o reemplaza el último comando por:
     pip install textual pandas matplotlib "textual-image[textual]" -->

## Uso

```bash
python app.py
```

<!-- TODO: reemplaza <archivo_de_entrada> por el archivo real (por ejemplo main.py). -->

Atajos de teclado:

| Tecla | Acción |
|---|---|
| `q` | Cerrar la aplicación |

## Estructura del proyecto

<!-- TODO: reemplaza por la salida real de `tree /F` (ignorando __pycache__ y .venv). -->

```text
Time_Series/
└── src/
    ├── app/
    │   ├── screens/
    │   │   └── main_screen.py          # Pantalla principal (MainScreen)
    │   └── widgets/
    │       ├── custom_info_panel.py    # Panel con título y contenido dinámico
    │       ├── custom_data_table.py    # Tabla de datos
    │       ├── custom_panel_chart.py   # Panel que muestra un gráfico como imagen
    │       └── custom_loading_indicator.py
    └── core/
        └── process_data.py             # Carga y procesamiento de datos (ProcessData)
```

## Tecnologías

- [Textual](https://textual.textualize.io/): interfaz de terminal
- [pandas](https://pandas.pydata.org/): procesamiento de la serie de tiempo
- [Matplotlib](https://matplotlib.org/): generación de los gráficos
- [textual-image](https://pypi.org/project/textual-image/): renderizado de imágenes en la terminal

## Créditos y licencia

Datos: U.S. Bureau of Economic Analysis, *Light Weight Vehicle Sales* [LTOTALNSA], obtenidos de FRED, Federal Reserve Bank of St. Louis: <https://fred.stlouisfed.org/series/LTOTALNSA>. FRED solicita citar la fuente al compartir los datos o gráficos derivados.

<!-- TODO: agrega tu licencia (por ejemplo MIT) y tu nombre / enlace a tu GitHub. -->