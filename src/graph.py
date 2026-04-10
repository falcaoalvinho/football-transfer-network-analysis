from dotenv import load_dotenv
import networkx as nx
import requests
import os

load_dotenv()

def get_env_variable(variable_name) -> str:
    """
    Acessa os valores das variáveis de ambientes e se esse valores forem diferentes de None, os retorna,
    senão lança uma Exception 
    """
    variable_value = os.getenv(variable_name)

    if variable_value == None:
        raise Exception("O valor recebido pela variável é 'None', verifique se o parametro 'variable_name'" \
        " está recebendo uma String compatível com as variáveis do ambiente")
    else:
        return variable_value        



def get_api_page(api_url: str, page_name: str):
    """
    Acessa o banco de dados criado via Sheety, e retorna os dados de uma das páginas do arquivo do 
    Google Sheets original

    Obs: Essa função não tem retornos explicítos porque eles podem ser de tipos variados, para mais
    informações consulte a documentação da biblioteca "request"

    api_url   -> Recebe a URL do tipo get para acessar a API 
    page_name -> Recebe o nome da página de onde queremos os dados
    """
    response = requests.get(api_url)

    if response.status_code == 200:
        response_json = response.json()
        return response_json[page_name]

    

def build_di_graph(page: list, source_column: str, destiny_column: str) -> nx.DiGraph:
    """
    Recebe uma página da planilha na forma de uma lista de dicionários, itera entre cada um deles e atribuí a eles os devidos plots
    na construção do grafo direcional, considerando inclusive o sentido das relações.

    page     -> Lista de dicionários contendo os dados para construção do grafo

    PARA CONSTRUIR O SENTIDO DOS PLOTS
    source_column -> Nome do coluna na tabela em que estão dos dados de onde surgem as relações 
    destiny_column -> Nome do coluna na tabela em que estão dos dados de para onde seguem as relações 
    """
    graph = nx.DiGraph()

    for dict_obj in page:
        source, destiny = dict_obj[source_column], dict_obj[destiny_column]

        if not graph.has_edge(source, destiny):
            graph.add_edge(
                source,
                destiny,
                weight=1,
                edge_transfers=[dict_obj],
                transfers_quantity=1
                )
            
        else:
            # Quantidade de transferências na Aresta
            graph[source][destiny]["transfers_quantity"] += 1
            transfers_quantity = graph[source][destiny]["transfers_quantity"]

            # Transferências na Aresta
            graph[source][destiny]["edge_transfers"].append(dict_obj)

            # Peso associado à Aresta
            graph[source][destiny]["weight"] = 1 / transfers_quantity
        
    return graph
