import matplotlib.pyplot as plt
import networkx as nx

COLORS = [
"#FF0000",
"#FF4D00",
"#FF9900",
"#FFE600",
"#CCFF00",
"#80FF00",
"#33FF00",
"#00FF1A",
"#00FF66",
"#00FFB3",
"#00FFFF",
"#00B3FF",
"#0066FF",
"#001AFF",
"#3300FF",
"#8000FF",
"#CC00FF",
"#FF00E6",
"#FF0099"
]

def draw_di_graph(graph: nx.DiGraph, layout: dict) -> None:
    """
    Recebe o grafo e o layout. Faz o plot padrão do nosso grafo direcional
    """
    nx.draw(
        graph,
        layout,
        node_size=20,
        node_color="navy",
        edge_color="skyblue",
        arrowsize=10
        )
    
    plt.show()



def draw_graph_communities(graph: nx.DiGraph, layout: dict, communities: list) -> None:
    """
    Recebe o grafo, o layout usado e as comunidades para construir uma visualização do 
    grafo para exibir as comunidades encontradas.
    """
    if len(communities) > len(COLORS):
        raise ValueError(f"Número de comunidades ({len(communities)}) excede o número de cores disponíveis ({len(COLORS)}))")
 
    color_map = dict()
    for i, community in enumerate(communities):
        for node in community:
            color_map[node] = COLORS[i]

    node_colors = [color_map[node] for node in graph.nodes()]

    nx.draw_networkx(
        graph,
        pos=layout,
        arrowsize=10,
        node_size=20,
        edge_color='gray',
        node_color=node_colors,
        with_labels=False
    )

    plt.show()



def dict_to_histogram(data_set: dict, bins: int, title: str, xlabel: str, ylabel: str) -> None:
    """
    Usando um conjunto de dados (dict), número de "bins" (caixas), título, e labels (para eixo x e y)
    e faz a plotagem de um histograma com essas informações.
    """
    data_list = [(key, value) for key, value in data_set.items()]
    data_values = list(data_list.values())

    values, columns, bars = plt.hist(data_values, bins=bins, edgecolor="black")
    
    plt.bar_label(bars, fontsize=10, color="black")
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()