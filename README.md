# Grafo pedagogico de recomendacion de usuarios

Proyecto Python para visualizar, de forma sencilla, como una red social podria recomendar usuarios usando un grafo.

La idea es representar:

- Vertices: usuarios de una red social.
- Aristas: relaciones o interacciones entre usuarios.
- Peso de arista: intensidad de la interaccion, de 1 a 5.
- Aristas sugeridas: recomendaciones calculadas para el usuario objetivo.

## Requisitos

- Python 3.9 o superior.
- VS Code.
- Extension de Python para VS Code.

## Instalacion en VS Code

Abre esta carpeta en VS Code y ejecuta en la terminal:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

En Windows, la activacion seria:

```bash
.venv\Scripts\activate
python -m pip install -r requirements.txt
```

## Como ejecutar

Modo interactivo:

```bash
python main.py
```

Elegir usuario desde la terminal:

```bash
python main.py --usuario Ana
```

Guardar la visualizacion como imagen:

```bash
python main.py --usuario Ana --guardar grafo_ana.png
```

Cambiar cantidad de recomendaciones:

```bash
python main.py --usuario Bruno --top 4
```

## Como funciona la recomendacion

El programa descarta usuarios que ya estan conectados con el usuario objetivo. Luego evalua posibles recomendaciones con esta formula:

```text
puntaje = 2 x amigos_en_comun + intereses_compartidos
```

Por ejemplo, si Ana no sigue a Gabriela, pero tienen amistades en comun e intereses parecidos, Gabriela puede aparecer como recomendacion.

## Como leer el grafo

- Rojo: usuario objetivo.
- Azul: conexiones directas del usuario objetivo.
- Verde: usuarios recomendados.
- Gris: otros usuarios de la red.
- Lineas grises: interacciones reales.
- Lineas amarillas punteadas: recomendaciones sugeridas.
- Numero sobre la arista: intensidad de interaccion.

## Estructura del proyecto

```text
.
├── main.py
├── requirements.txt
├── README.md
└── src
    └── recommender_graph.py
```

## Ideas para ampliar

- Agregar mas usuarios y categorias de intereses.
- Cambiar la formula de recomendacion.
- Simular likes, comentarios, mensajes y seguidores por separado.
- Crear una version web con Streamlit.
- Comparar recomendaciones por amigos en comun contra recomendaciones por intereses.
