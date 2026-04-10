import networkx as nx
from networkx.algorithms import community

def get_graph_metrics(graph: nx.DiGraph) -> dict:
    """
    Essa função recebe o grafo direcional e retorna um dicionário com as métricas específicas do grafo e não de 
    suas entidades

    As metrícas que a função retorna são: "size" (tamanho), "order" (ordem), "density" (densidade), 
    "clustering" (clusterização *média) e "diameter" (diametro)
    """
    metrics = {
        "size": int(),
        "order": int(),
        "density": float(),
        "clustering": float(),
        "diameter": None # Essa métrica pode receber valores nulos caso o grafo não seja fortemente conectado
    }

    metrics["size"]       = graph.number_of_edges()
    metrics["order"]      = graph.number_of_nodes()
    metrics["density"]    = nx.density(graph)
    metrics["clustering"] = nx.average_clustering(graph)

    try:
        metrics["diameter"] = nx.diameter(graph)

    except nx.NetworkXError:
        metrics["diameter"] = "O grafo possuí diametro infinito (possivelmente é fracamente conectado)"
            
    return metrics



def get_sorted_centralities(graph: nx.DiGraph, centrality_method) -> dict:
    """
    Essa função recebe um grafo direcional e uma das funções calculadoras de centralidades e retorna um dicionário
    contendo as centralidades do tipo escolhido, para cada um dos vértices, com valores ordenados do maior para o
    menor.

    As centralidades que a função poder retornar são: "degree" (grau), "in_degree" (grau de entrada)
    "out_degree" (grau de saída), "closeness" (proximidade), "betweenness" (intermediação)
    e "eigenvector" (autovetor)
    """
    centralities = centrality_method(graph)
    ordened_centralities = dict(sorted(centralities.items(), key=lambda item: item[1], reverse=True))
    return ordened_centralities



def get_communities_metrics(graph: nx.DiGraph, communities) -> dict:
    """
    Recebe um grafo direcional e o um conjunto de comunidades e retorna algumas das métricas usadas no projeto
    sendo elas: "number_of_clusters" (número de clusters), "communities_modularity" (modularidade das comunidades)
    "assortativity" (assertividade)
    """
    metrics = {
        "number_of_clusters": len(communities),
        "communities_modularity": nx.community.modularity(graph, communities),
        "assortativity": nx.degree_assortativity_coefficient(graph)
    }
    return metrics


