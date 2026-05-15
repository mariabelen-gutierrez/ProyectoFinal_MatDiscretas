import argparse
from dataclasses import dataclass
from typing import Dict, Iterable, List, Set, Tuple

import matplotlib.pyplot as plt
import networkx as nx


@dataclass(frozen=True)
class Recommendation:
    user: str
    score: float
    mutual_friends: List[str]
    shared_interests: List[str]


USERS: Dict[str, Set[str]] = {
    "Ana": {"fotografia", "moda", "viajes"},
    "Bruno": {"musica", "tecnologia", "gaming"},
    "Camila": {"fotografia", "comida", "viajes"},
    "Diego": {"deportes", "gaming", "musica"},
    "Elena": {"moda", "arte", "fotografia"},
    "Felipe": {"tecnologia", "ciencia", "gaming"},
    "Gabriela": {"viajes", "comida", "arte"},
    "Hugo": {"deportes", "musica", "cine"},
    "Isabel": {"moda", "fitness", "viajes"},
    "Javier": {"tecnologia", "cine", "ciencia"},
    "Laura": {"fotografia", "arte", "comida"},
    "Mateo": {"deportes", "fitness", "gaming"},
    "Nora": {"musica", "cine", "arte"},
    "Oscar": {"tecnologia", "viajes", "ciencia"},
    "Paula": {"moda", "comida", "fitness"},
}


EDGES: List[Tuple[str, str, int, str]] = [
    ("Ana", "Camila", 5, "likes y comentarios"),
    ("Ana", "Elena", 4, "fotos compartidas"),
    ("Ana", "Isabel", 3, "seguimiento mutuo"),
    ("Ana", "Laura", 2, "comentarios"),
    ("Bruno", "Diego", 5, "gaming y mensajes"),
    ("Bruno", "Felipe", 4, "tecnologia"),
    ("Bruno", "Javier", 3, "cine y tecnologia"),
    ("Camila", "Gabriela", 4, "viajes"),
    ("Camila", "Laura", 5, "comida y fotografia"),
    ("Diego", "Hugo", 4, "deportes"),
    ("Diego", "Mateo", 5, "gaming"),
    ("Elena", "Laura", 4, "arte"),
    ("Elena", "Paula", 3, "moda"),
    ("Felipe", "Javier", 4, "ciencia"),
    ("Felipe", "Oscar", 3, "tecnologia"),
    ("Gabriela", "Laura", 4, "arte y comida"),
    ("Gabriela", "Oscar", 2, "viajes"),
    ("Hugo", "Nora", 4, "cine y musica"),
    ("Hugo", "Mateo", 3, "deportes"),
    ("Isabel", "Paula", 4, "fitness y moda"),
    ("Isabel", "Gabriela", 2, "viajes"),
    ("Javier", "Oscar", 5, "ciencia"),
    ("Nora", "Elena", 2, "arte"),
    ("Paula", "Laura", 3, "comida"),
]


def build_graph() -> nx.Graph:
    graph = nx.Graph()

    for user, interests in USERS.items():
        graph.add_node(user, interests=sorted(interests))

    for user_a, user_b, weight, interaction in EDGES:
        graph.add_edge(user_a, user_b, weight=weight, interaction=interaction)

    return graph


def recommend_users(graph: nx.Graph, target: str, limit: int = 3) -> List[Recommendation]:
    if target not in graph:
        raise ValueError(f"El usuario {target!r} no existe en la red.")

    direct_neighbors = set(graph.neighbors(target))
    target_interests = set(graph.nodes[target]["interests"])
    recommendations: List[Recommendation] = []

    for candidate in graph.nodes:
        if candidate == target or candidate in direct_neighbors:
            continue

        candidate_neighbors = set(graph.neighbors(candidate))
        mutual_friends = sorted(direct_neighbors & candidate_neighbors)
        shared_interests = sorted(target_interests & set(graph.nodes[candidate]["interests"]))

        score = (len(mutual_friends) * 2.0) + (len(shared_interests) * 1.0)
        if score > 0:
            recommendations.append(
                Recommendation(
                    user=candidate,
                    score=score,
                    mutual_friends=mutual_friends,
                    shared_interests=shared_interests,
                )
            )

    recommendations.sort(key=lambda item: (-item.score, item.user))
    return recommendations[:limit]


def print_network_summary(graph: nx.Graph, target: str, recommendations: Iterable[Recommendation]) -> None:
    print("\n=== Red social simulada ===")
    print(f"Usuarios: {graph.number_of_nodes()}")
    print(f"Relaciones/interacciones: {graph.number_of_edges()}")

    print(f"\nUsuario objetivo: {target}")
    print("Intereses:", ", ".join(graph.nodes[target]["interests"]))

    print("\nConexiones directas:")
    for neighbor in sorted(graph.neighbors(target)):
        edge = graph[target][neighbor]
        print(f"- {neighbor}: peso {edge['weight']} ({edge['interaction']})")

    print("\nRecomendaciones:")
    for index, rec in enumerate(recommendations, start=1):
        mutual = ", ".join(rec.mutual_friends) if rec.mutual_friends else "ninguno"
        interests = ", ".join(rec.shared_interests) if rec.shared_interests else "ninguno"
        print(f"{index}. {rec.user} | puntaje {rec.score:.1f}")
        print(f"   Amigos en comun: {mutual}")
        print(f"   Intereses en comun: {interests}")


def draw_graph(
    graph: nx.Graph,
    target: str,
    recommendations: List[Recommendation],
    save_path: str = "",
) -> None:
    position = nx.spring_layout(graph, seed=8, k=0.68)
    direct_neighbors = set(graph.neighbors(target))
    recommended_users = {rec.user for rec in recommendations}

    node_colors = []
    node_sizes = []
    for node in graph.nodes:
        if node == target:
            node_colors.append("#ff595e")
            node_sizes.append(1450)
        elif node in recommended_users:
            node_colors.append("#8ac926")
            node_sizes.append(1250)
        elif node in direct_neighbors:
            node_colors.append("#1982c4")
            node_sizes.append(1050)
        else:
            node_colors.append("#d9d9d9")
            node_sizes.append(850)

    edge_widths = [graph[u][v]["weight"] * 0.65 for u, v in graph.edges]
    edge_labels = {(u, v): graph[u][v]["weight"] for u, v in graph.edges}

    fig, ax = plt.subplots(figsize=(12, 8))
    ax.set_title(
        f"Sistema de recomendacion de usuarios - usuario objetivo: {target}",
        fontsize=15,
        pad=16,
    )

    nx.draw_networkx_edges(
        graph,
        position,
        width=edge_widths,
        edge_color="#9aa0a6",
        alpha=0.65,
        ax=ax,
    )
    nx.draw_networkx_edge_labels(
        graph,
        position,
        edge_labels=edge_labels,
        font_size=8,
        font_color="#4a4a4a",
        ax=ax,
    )
    nx.draw_networkx_nodes(
        graph,
        position,
        node_color=node_colors,
        node_size=node_sizes,
        linewidths=1.8,
        edgecolors="#222222",
        ax=ax,
    )
    nx.draw_networkx_labels(graph, position, font_size=9, font_weight="bold", ax=ax)

    for rec in recommendations:
        x1, y1 = position[target]
        x2, y2 = position[rec.user]
        ax.plot(
            [x1, x2],
            [y1, y2],
            color="#ffca3a",
            linewidth=2.3,
            linestyle="--",
            alpha=0.9,
        )
        mid_x = (x1 + x2) / 2
        mid_y = (y1 + y2) / 2
        ax.text(
            mid_x,
            mid_y,
            f"rec {rec.score:.0f}",
            fontsize=8,
            color="#7a4f00",
            bbox={"boxstyle": "round,pad=0.2", "fc": "#fff3bf", "ec": "#ffca3a"},
        )

    legend_handles = [
        plt.Line2D([0], [0], marker="o", color="w", label="Usuario objetivo", markerfacecolor="#ff595e", markersize=12),
        plt.Line2D([0], [0], marker="o", color="w", label="Conexiones directas", markerfacecolor="#1982c4", markersize=12),
        plt.Line2D([0], [0], marker="o", color="w", label="Recomendados", markerfacecolor="#8ac926", markersize=12),
        plt.Line2D([0], [0], color="#ffca3a", lw=2, linestyle="--", label="Arista sugerida"),
    ]
    ax.legend(handles=legend_handles, loc="lower left", frameon=True)

    ax.text(
        0.01,
        0.98,
        "Peso de arista = intensidad de interaccion\nPuntaje = 2 x amigos en comun + intereses compartidos",
        transform=ax.transAxes,
        fontsize=9,
        verticalalignment="top",
        bbox={"boxstyle": "round,pad=0.4", "fc": "#ffffff", "ec": "#cccccc"},
    )

    ax.axis("off")
    fig.tight_layout()

    if save_path:
        fig.savefig(save_path, dpi=180, bbox_inches="tight")
        print(f"\nImagen guardada en: {save_path}")

    plt.show()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Visualiza un grafo pequeno de recomendacion de usuarios."
    )
    parser.add_argument(
        "--usuario",
        help="Usuario objetivo. Ejemplo: Ana",
        default="",
    )
    parser.add_argument(
        "--guardar",
        help="Ruta opcional para guardar la imagen. Ejemplo: grafo.png",
        default="",
    )
    parser.add_argument(
        "--top",
        help="Cantidad de recomendaciones a mostrar.",
        type=int,
        default=3,
    )
    return parser.parse_args()


def choose_user(graph: nx.Graph) -> str:
    users = sorted(graph.nodes)
    print("Usuarios disponibles:")
    print(", ".join(users))

    while True:
        selected = input("\nEscribe el usuario objetivo: ").strip()
        if selected in graph:
            return selected
        print("Ese usuario no existe. Intenta de nuevo respetando mayusculas.")


def run_app() -> None:
    args = parse_args()
    graph = build_graph()
    target = args.usuario if args.usuario else choose_user(graph)

    if target not in graph:
        valid_users = ", ".join(sorted(graph.nodes))
        raise SystemExit(f"Usuario invalido. Opciones validas: {valid_users}")

    recommendations = recommend_users(graph, target, limit=args.top)
    print_network_summary(graph, target, recommendations)
    draw_graph(graph, target, recommendations, save_path=args.guardar)
