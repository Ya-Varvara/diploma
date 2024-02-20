import networkx as nx
import matplotlib.pyplot as plt


def graph_from_dict(graph: dict) -> nx.DiGraph:
    """
    Функция преобразует словарь в граф.
    Получает на вход словарь, преобразует его в объект класса Graph
    :param g: граф в виде словаря
    :return: граф в виде объекта Граф
    """
    new_graph = nx.DiGraph()
    for key, value in graph.items():
        for x in value:
            new_graph.add_edge(key, x)
    return new_graph


def weight_graph_from_dict(graph: dict) -> nx.DiGraph:
    """
    Функция преобразует словарь в граф.
    Получает на вход словарь, преобразует его в объект класса Graph
    :param g: граф в виде словаря
    :return: граф в виде объекта Граф
    """
    new_graph = nx.DiGraph()
    for node in graph:
        for x in graph[node]:
            new_graph.add_edge(node, x, weight=graph[node][x])
    return new_graph


def draw_graph(graph, weighted=False):
    """
    Функция рисует граф,  на вход - объект класса Graph
    :param graph: граф в виде объекта Граф
    :return:
    """
    if isinstance(graph, dict):
        graph = weight_graph_from_dict(graph) if weighted else graph_from_dict(graph)
    nx.draw_networkx(graph, pos=nx.spring_layout(graph), arrows=True)  # networkx draw()
    plt.show()
