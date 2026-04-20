from matplotlib import pyplot
import matplotlib.colors as mcolors
import pandas as pd

"""
Esse arquivo foi criado para converter para PNG e exportar as tabelas estilizadas criadas com a biblioteca "pandas"
em html e css bruto para consultas rápidas do materia gerado, independentes da instalação do projeto localmente.
"""

def export_styled_table(sorted_data: dict, column: str, index_name: str, min_value: float = 0) -> object:
    """
    Essa função é muito similar a "draw_styled_table", a única grande diferença entre as duas é que esta retorna
    o objeto gerado em vez de aplica-lo na função display.
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

    return styled

"""
O código abaixo foi usado para transformar algumas das tabelas estilizadas em arquivos PNG's e consta como referência
de como aplicar o método com o material já produzido para resultados semelhantes em outros projetos

```
import dataframe_image as dfi
import networkx as nx

from graph import get_env_variable, get_api_page, build_di_graph
from metrics import get_sorted_centralities

DIRECTORY_PATH = "outputs/tables/centralities/styled/"

api_url = get_env_variable("API_URL")
page = get_api_page(api_url, "transfers")
graph, layout = build_di_graph(page, "from", "to")

absolute_degree = get_sorted_centralities(graph, nx.degree_centrality)
in_degree = get_sorted_centralities(graph, nx.in_degree_centrality)
out_degree = get_sorted_centralities(graph, nx.out_degree_centrality)

closeness = get_sorted_centralities(graph, nx.closeness_centrality)
betweenness = get_sorted_centralities(graph, nx.betweenness_centrality)
eigenvector = get_sorted_centralities(graph, nx.eigenvector_centrality)
pagerank = get_sorted_centralities(graph, nx.pagerank)


styled = export_styled_table(absolute_degree, "Grau (Absoluto)", "Clubes", min_value=0)
dfi.export(styled, f"{DIRECTORY_PATH}Degree_absolute.png", max_rows=-1)

styled = export_styled_table(in_degree, "Grau (Entrada)", "Clubes", min_value=0)
dfi.export(styled, f"{DIRECTORY_PATH}Degree_in.png", max_rows=-1)

styled = export_styled_table(out_degree, "Grau (Saída)", "Clubes", min_value=0)
dfi.export(styled, f"{DIRECTORY_PATH}Degree_out.png", max_rows=-1)

styled = export_styled_table(closeness, "Closeness", "Clubes", min_value=0)
dfi.export(styled, f"{DIRECTORY_PATH}Closeness.png", max_rows=-1)

styled = export_styled_table(betweenness, "Betweenness", "Clubes", min_value=0)
dfi.export(styled, f"{DIRECTORY_PATH}Betweenness.png", max_rows=-1)

styled = export_styled_table(eigenvector, "Autovetor", "Clubes", min_value=0)
dfi.export(styled, f"{DIRECTORY_PATH}Eigenvector.png", max_rows=-1)

styled = export_styled_table(pagerank, "Pagerank", "Clubes", min_value=0)
dfi.export(styled, f"{DIRECTORY_PATH}Pagerank.png", max_rows=-1)
```
"""