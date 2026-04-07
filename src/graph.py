from dotenv import load_dotenv
import networkx as nx
import requests

load_dotenv()

def get_api_page(api_url: str, page_name: str):
    """
    Acessa o banco de dados criado via Sheety, e retorna os dados de uma das páginas do arquivo do 
    Google Sheets original

    api_url   -> Recebe a URL do tipo get para acessar a API 
    page_name -> Recebe o nome da página de onde queremos os dados
    """
    response = requests.get(api_url)

    if response.status_code == 200:
        response = response.json()
        return response[page_name]

    

def build_di_graph(page: list, from_str: str, to_str: str) -> nx.DiGraph:
    """
    Recebe uma página da planilha na forma de uma lista de dicionários, itera entre cada um deles e atribuí a eles os devidos plots
    na construção do grafo direcional, considerando inclusive o sentido das relações.

    page     -> Lista de dicionários contendo os dados para construção do grafo

    PARA CONSTRUIR O SENTIDO DOS PLOTS
    from_str -> Nome do coluna na tabela em que estão dos dados de onde surgem as relações 
    to_str -> Nome do coluna na tabela em que estão dos dados de para onde seguem as relações 
    """
    graph = nx.DiGraph()

    start_nodes = [node[from_str] for node in page]
    end_nodes = [node[to_str] for node in page]

    for i in range(len(page)):
        if not graph.has_edge(from_str, to_str):
            graph.add_edge(
                start_nodes[i],
                end_nodes[i],
                weight=1,
                edge_transfers=[],
                transfers_quantity=0
                )
            
        else:
            # Quantidade de transferências na Aresta
            graph[start_nodes[i]][end_nodes[i]]["transfers_quantity"] += 1
            transfers_quantity = graph[start_nodes[i]][end_nodes[i]]["transfers_quantity"]

            # Transferências na Aresta
            graph[start_nodes[i]][end_nodes[i]]["edge_transfers"].append(page[i])

            # Peso associado à Aresta
            graph[start_nodes[i]][end_nodes[i]]["weight"] = 1 / transfers_quantity
        
    return graph
