from random import shuffle, randint, sample


def dict_to_list(gr: dict) -> list:
    """
    Преобразует граф типа словарь в тип двумерный массив

    :param gr: граф типа словарь
    :return: двумерный массив
    """
    new = []
    for x in gr:
        new.append([0] * len(gr))
        for y in gr[x]:
            new[x][y] = gr[x][y]
    return new


def FordFulkerson(gr: dict) -> tuple:
    """
    Алгоритм находит максимальный поток и минимальный разрез

    :param gr:
    :return: Максимальный поток, список вершин, входящих в левую часть, список вершин, входящих в правую часть
    """
    graph = dict_to_list(gr) if isinstance(gr, dict) else gr
    source = 0
    sink = len(graph) - 1
    # print(graph)

    def BFS(graph, s, t):
        # Return True if there is node that has not iterated.
        visited = [False] * len(graph)
        queue = [s]
        visited[s] = True
        while queue:
            u = queue.pop(0)
            for ind in range(len(graph[u])):
                if visited[ind] is False and graph[u][ind] > 0:
                    queue.append(ind)
                    visited[ind] = True
                    parent[ind] = u
        return True if visited[t] else False

    parent = [-1] * (len(graph))
    max_flow = 0
    while BFS(graph, source, sink):
        path_flow = float("Inf")
        s = sink
        while s != source:
            path_flow = min(path_flow, graph[parent[s]][s])
            s = parent[s]
        max_flow += path_flow
        v = sink
        while v != source:
            u = parent[v]
            graph[u][v] -= path_flow
            graph[v][u] += path_flow
            v = parent[v]
        parent = [-1] * (len(graph))
    parent[0] = 0
    A = [i for i in range(len(parent)) if parent[i] != -1]
    B = [i for i in range(len(parent)) if parent[i] == -1]
    return max_flow, A, B


def random_sum(n, total) -> list:
    """Return a randomly chosen list of n positive integers summing more than total.
    Each such list is equally likely to occur."""
    if not n:
        return []
    if n < 3:
        res = []
        for _ in range(n):
            res.append((total + randint(total // 10, total // 3)) * 4 // 5)
        return res
    div1 = sorted(sample(range(total * 2 // 3, total), n))
    div2 = div1.copy()
    shuffle(div2)
    return [(a + b) * 2 // 3 + 1 for a, b in zip(div1, div2)]


def random_flow(n, total) -> list:
    """Return a randomly chosen list of n positive integers summing to total.
    Each such list is equally likely to occur."""
    if n == 1:
        return [total]
    res = []
    if total // n < 6:
        res = [total // n] * n
        res[0] += total - sum(res)
        return res
    try:
        while True:
            dividers = sorted(sample(range(1, total), n - 1))
            res = [a - b for a, b in zip(dividers, [0] + dividers[:-1])]
            res.append(total - sum(res))
            if len(list(filter(lambda x: x > 0, res))) == len(res):
                break
            if min(res) <= 2:
                res.sort()
                k = res[n - 1] // 2
                res[n - 1] -= k
                res[0] += k
    except ValueError:
        print("!!!", n, total)
    return res
