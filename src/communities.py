import matplotlib.pyplot as plt
import networkx as nx
from networkx.algorithms import community

def get_comunities(graph, method, seed=13):
    """
    Recebe o grafo e um methodo do pacote "community" do networkx.algorithms e retorna as comunidades encontradas
    com ele. Para a nossa análise optamos por usar as comunidades encontradas com o método de Louvian

    OBS: Alguns métodos são heurísticos, portanto os resultados podem ter variações suaves, normalmente mantendo 
    uma média estável

    OBS: No nosso projeto usamos o método de Louvain ele pode ser acessado pelo pacote "netowrkx.algorithms" no 
    objeto "community"
    """
    communities = method(graph, seed=seed)
    return communities
