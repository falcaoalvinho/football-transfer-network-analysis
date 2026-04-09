import matplotlib.pyplot as plt
import networkx as nx
from networkx.algorithms import community

colors = [
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

def get_comunities(graph, method):
    """
    Recebe o grafo e um methodo do pacote "community" do networkx.algorithms e retorna as comunidades encontradas
    com ele. Para a nossa análise optamos por usar as comunidades encontradas com o método de Louvian

    OBS: Alguns métodos são heurísticos, portanto os resultados podem ter variações suaves, normalmente mantendo 
    uma média estável
    """
    communities = community.method(graph)
    return communities
