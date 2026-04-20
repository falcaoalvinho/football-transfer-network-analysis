from matplotlib import pyplot
import networkx as nx
import pandas as pd
from pandas.plotting import table
from IPython.display import display
import matplotlib.colors as mcolors

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



def draw_di_graph(plot: pyplot, graph: nx.DiGraph, layout: dict ) -> None:
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
    
    plot.show()



def draw_graph_communities(plot: pyplot, graph: nx.DiGraph, layout: dict, communities: list) -> None:
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

    plot.show()



def dict_to_histogram(plot: pyplot, data_set: dict, bins: int, title: str, xlabel: str, ylabel: str) -> None:
    """
    Usando um conjunto de dados (dict), número de "bins" (caixas), título, e labels (para eixo x e y)
    e faz a plotagem de um histograma com essas informações dentro de um objeto plotable (pyplot).
    
    OBS: O objeto plotável deve ser DADO COMO PARÂMETRO! Isso acontece porque dentro de um jupyter notebook
    o histograma pode não ser exibido se não estiver dentro do escopo da célula.
    """
    data_values = [value for key, value in data_set.items()]

    values, columns, bars = plot.hist(data_values, bins=bins, edgecolor="black")
    
    plot.bar_label(bars, fontsize=10, color="black")
    plot.title(title)
    plot.xlabel(xlabel)
    plot.ylabel(ylabel)

    plot.show()



def list_to_histogram(plot: pyplot, data_values: list, bins: int, title: str, xlabel: str, ylabel: str) -> None:
    """
    Muito semelhante a dict_to_histogram, a única grande diferencça é que constroí o histograma a partir de uma lista
    de valores e não de um dicionário
    """
    values, columns, bars = plot.hist(data_values, bins=bins, edgecolor="black")
    
    plot.bar_label(bars, fontsize=10, color="black")
    plot.title(title)
    plot.xlabel(xlabel)
    plot.ylabel(ylabel)

    plot.show()



def draw_base_table(plot: pyplot, sorted_data: dict, column: str, index_name: str, min_value: float = 0) -> None:
    """
    Função que constroí as tabelas basícas (usadas no paper final) usando a estilização padrão do projeto. Ela recebe
    um plot (tela onde vamos plotar os dados), os dados na forma de dicionários, o nome da coluna, o nome do index, e 
    um valor mínimo que por padrão é = 0

    OBS: A função gera uma tabela básica com 2 colunas para dados, uma para índices - no caso o nome dos times - e 
    o dado associado - sejam valores do pagerank, outras centralidades etc.
    """
    filtered_data = dict((key, value) for key, value in sorted_data.items() if sorted_data[key] >= min_value)

    data_frame = pd.DataFrame.from_dict(filtered_data, orient='index', columns=[column])
    data_frame.index.name = index_name

    figure, axis = plot.subplots(figsize=(8, 2))
    axis.axis('off')
    table(axis, data_frame, loc='center')

    plot.show()



def draw_styled_table(sorted_data: dict, column: str, index_name: str, min_value: float = 0) -> None:
    """
    Constroí uma tabela no mesmo formato de "draw_base_table" porém não depende de uma tela/objeto plotavél, e também
    contém elementos de estilização tornando esse retorno melhor para leitura/consulta dos dados.

    OBS: Diferente da primeira função que gerava tabelas "base" em PNG, essa as constrí em HTML e CSS bruto, tenha isso em
    mente, se precisar converte-las consulte o arquivo "export.py" neste mesmo diretório
    """
    HEADER_COLOR = "#2D6A4F"
    HEADER_TEXT  = "#FFFFFF"
    INDEX_COLOR  = "#3A7D5E"
    INDEX_TEXT   = "#FFFFFF"

    filtered = {key: value for key, value in sorted_data.items() if value >= min_value}

    data_frame = pd.DataFrame(
        [(key, value) for key, value in filtered.items()],
        columns=[index_name, column]
    )
    data_frame[column] = pd.to_numeric(data_frame[column])

    cmap = pyplot.get_cmap("YlGn")
    values = data_frame[column].values
    normalize = mcolors.Normalize(vmin=values.min(), vmax=values.max())

    def text_color_for_column(series):
        colors = []
        for value in series:
            red, green, blue, _ = cmap(normalize(value))
            luminance = 0.299 * red + 0.587 * green + 0.114 * blue
            colors.append("color: #1a1a1a" if luminance > 0.45 else "color: #ffffff")
        return colors

    styled = (
        data_frame.style
        .format({column: lambda v: f"{v:.5g}"})
        .background_gradient(cmap="YlGn", subset=[column])
        .apply(text_color_for_column, subset=[column])
        .apply(lambda s: [f"background-color: {INDEX_COLOR}; color: {INDEX_TEXT}; font-weight: 600; white-space: nowrap"] * len(s), subset=[index_name])
        .apply_index(
            lambda s: [
                f"background-color: {HEADER_COLOR}; color: {HEADER_TEXT}; font-weight: 600; text-align: center"
                if i % 2 == 0
                else f"background-color: {INDEX_COLOR}; color: {INDEX_TEXT}; font-weight: 600; text-align: center"
                for i in range(len(s))
            ],
            axis="index"
        )
        .set_properties(**{
            "font-size": "13px",
            "padding": "6px 14px",
            "text-align": "center",
        })
        .set_properties(**{
            "text-align": "left",
        }, subset=[index_name])
        .set_table_styles([
            {
                "selector": "thead th.col_heading.level0",
                "props": [
                    ("background-color", HEADER_COLOR),
                    ("color", HEADER_TEXT),
                    ("font-size", "13px"),
                    ("font-weight", "bold"),
                    ("padding", "8px 14px"),
                    ("text-align", "center"),
                    ("border-bottom", f"2px solid {HEADER_COLOR}"),
                ]
            },
            {
                "selector": "table",
                "props": [
                    ("border-collapse", "collapse"),
                    ("width", "auto"),
                    ("margin", "12px 0"),
                ]
            },
        ])
    )

    display(styled)