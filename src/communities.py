import matplotlib.pyplot as plt
import networkx as nx
from networkx.algorithms import community

def get_comunities(graph, method):
    """
    Recebe o grafo e um methodo do pacote "community" do networkx.algorithms e retorna as comunidades encontradas
    com ele. Para a nossa análise optamos por usar as comunidades encontradas com o método de Louvian

    OBS: Alguns métodos são heurísticos, portanto os resultados podem ter variações suaves, normalmente mantendo 
    uma média estável
    """
    communities = method(graph)
    return communities
