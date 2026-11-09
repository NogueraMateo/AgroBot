# AgroBot

AgroBot es un proyecto de Inteligencia Artificial de la Universidad del Valle. Un robot debe fertilizar todos los cultivos secos de un tablero de 10 × 10. Se desplaza en cuatro direcciones, puede cargar hasta dos unidades de fertilizante y recarga en el depósito. Cada paso cuesta 1, o 0,5 si el robot ya abordó la avioneta y todavía tiene combustible.

La interfaz permite cargar un tablero, elegir un algoritmo y animar la ruta obtenida. Las búsquedas no informadas son Amplitud, Costo uniforme y Profundidad evitando ciclos. Las informadas son Avara y A*.

## Ejecutar en Linux

AgroBot usa Pygame para la interfaz y Tkinter para el selector de archivos. Usa Python 3.12 para instalar la versión precompilada de Pygame 2.6.1.

Si aún no tienes el repositorio, clónalo con una cuenta que tenga acceso por SSH:

```bash
git clone git@github.com:NogueraMateo/AgroBot.git
cd AgroBot
```

Desde la raíz del repositorio, crea un entorno con Python 3.12. Si tienes ese intérprete instalado, ejecuta:

```bash
python3.12 -m venv .venv312
.venv312/bin/python -m pip install --only-binary=pygame -r requirements.txt
```

Si `python3.12` no está disponible, [instala uv](https://docs.astral.sh/uv/getting-started/installation/) y usa estos comandos para crear el entorno e instalar las dependencias:

```bash
uv python install 3.12
uv venv --python 3.12 .venv312
uv pip install --python .venv312/bin/python --only-binary=pygame -r requirements.txt
```

Comprueba las importaciones y abre la aplicación desde la misma carpeta:

```bash
.venv312/bin/python -c "import pygame, tkinter" &&
.venv312/bin/python -m interface.app
```

Si `pip` intenta compilar Pygame o muestra un error de SDL, comprueba que estás usando el intérprete de `.venv312` con `.venv312/bin/python --version`. Pygame 2.6.1 no publica un paquete precompilado para Python 3.14. Si falta `tkinter`, instala el soporte de Tk para la distribución de Python que elegiste. El paquete `tk` de PyPI es independiente de ese módulo.

## Probar los algoritmos

1. Abre la aplicación. El tablero inicial es [Prueba1.txt](test_files/Prueba1.txt).
2. Selecciona **Informada → Avara** y pulsa **Iniciar búsqueda**.
3. Repite con **Informada → A***. En este tablero, los costos de referencia son **38** para Avara y **25** para A*, que coincide con Costo uniforme.

Para probar otro tablero, usa **Cargar archivo TXT**. El archivo debe contener 10 filas de 10 números separados por espacios.

| Valor | Casilla |
| --- | --- |
| 0 | Libre |
| 1 | Obstáculo |
| 2 | AgroBot |
| 3 | Cultivo seco |
| 4 | Depósito de fertilizante |
| 5 | Avioneta |

Incluye exactamente un AgroBot, un depósito y una avioneta.

## Heurística

La [heurística compartida](search/informed.py) multiplica por 0,5 el máximo entre la distancia Manhattan al cultivo pendiente más lejano y el número de cultivos pendientes. Ambas cantidades son cotas inferiores del número de movimientos necesarios. Cada movimiento cuesta al menos 0,5, por lo que la estimación es admisible. Avara prioriza esta estimación y A* le suma el costo acumulado.
