from random import random, randint, shuffle
from .algorithms import random_flow, FordFulkerson
from .graph_draw import draw_graph
from collections import deque


async def make_graph_data(graph: tuple) -> dict:
    net, nodes, cutA, cutB, cut, r_cut, max_flow = graph
    return {
        "description_data": "Найдите максимальный поток и минимальный разрез с помощью алгоритма Форда Фалкерсона",
        "condition_data": {"graph_net": net},
        "answer_data": {
            "nodes_number": nodes,
            "cut_A": cutA,
            "cut_B": cutB,
            "cut": cut,
            "reverse_cut": r_cut,
            "max_flow": max_flow,
        },
    }


async def generate_graph(**settings) -> tuple:
    #     nodes: int = 13, min_weight=10, max_weight=70, info=False, draw=False
    # ) -> tuple:
    """
    Функция генерации сети с одним источником и одним стоком. При этом при решении данного графа можно построить хотя бы один увеличивающий маршрут

    :param nodes: Кол-во вершин
    :param min_weight: Минимальный вес ребра
    :param max_weight: Максимальный вес ребра
    :return: Возвращает 1, если граф сгенерирован успешно
    """
    print(settings)
    nodes = settings.get("nodes_number", 13)
    min_weight = settings.get("min_weight", 10)
    max_weight = settings.get("max_weight", 70)
    info = settings.get("info", False)
    draw = settings.get("draw", False)
    # Высчитываем средний вес и 10% от диапазона для задания максимального потока
    k = (max_weight - min_weight) // 10
    avg = (max_weight - min_weight) // 2

    # Генерируем базу
    base = await generate_graph_base(nodes)
    if info:
        print(f"=========== Сгенерированная база графа ===========\n{base}\n")

    # Генерируем сильно связный граф
    await make_strongly_connected(base)
    if info:
        print(f"=========== Сильно связный граф ===========\n{base}\n")

    # Задаем разрез и определяем подмножества вершин и обратные ребра разреза
    cutA, cutB, cut, r_cut = await make_cut(base)

    if info:
        print(f"=========== Сильно связный граф с изменениями ===========\n{base}\n")

    # Задаем максимальный поток на графе
    net, max_flow = await make_flow(base, r_cut, avg, avg + 4 * k)
    if info:
        print(f"=========== Сильно связный граф с потоком ===========\n{net}\n")

    # Определяем пропускные способности
    await make_throughput(net, cut, min_weight, max_weight)
    if info:
        print(
            f"=========== Сильно связный граф с пропускными способностями ===========\n{net}\n"
        )

    # Рисуем граф
    if draw:
        draw_graph(net)

    # Проверяем по алгоритму Форда Фалкерсона
    ff_max_flow, ff_cutA, ff_cutB = FordFulkerson(net)
    if info:
        print(
            f"=========== Заданный нами разрез ===========\nМножество А = {cutA}\nМножество В = {cutB}\nМаксимальный "
            f"заданный поток = {max_flow}\nРебра = {cut}\nОбратные ребра = {r_cut}\n"
        )
        print(
            f"=========== По алгоритму Форда Фалкерсона ===========\nМножество А = {ff_cutA}\nМножество В = {ff_cutB}\n"
            f"Максимальный заданный поток = {ff_max_flow}\n"
        )
    if max_flow == ff_max_flow and cutA == ff_cutA and cutB == ff_cutB:
        return await make_graph_data((net, nodes, cutA, cutB, cut, r_cut, max_flow))
    else:
        return None


async def generate_graph_base(n: int) -> dict:
    """Генерирует слабо связную базу графа

    :param n: количество вершин
    :return: dict
    """
    graph = {i: [] for i in range(n)}
    while True:
        w = (n + 1) // 2 if n < 11 else n // 3
        window = [i for i in range(1, w + 1)]
        first = 1
        last = w
        for x in graph:
            if x == n - 1:
                break
            k = randint(1, 2)
            wx = window.copy()
            shuffle(wx)
            while k:
                if not wx:
                    break
                a = wx.pop(0)
                if a != x and (a not in graph[x]) and (x not in graph[a]):
                    graph[x].append(a)
                    k -= 1
            if x == first + (last - first + 1) // 3 and last < n - 1:
                window.remove(first)
                first += 1
                last += 1
                window.append(last)
        if await is_weakly_connected(graph):
            break
        graph = {i: [] for i in range(n)}
    return graph


async def is_weakly_connected(graph: dict) -> bool:
    """Проверка на связность графа

    :param graph: граф в виде словаря
    :return: bool
    """
    done = set()
    buf = []
    for key, value in graph.items():
        if key in done or done & set(value) or not done:
            done.add(key)
            done |= set(value)
        else:
            s = set(value)
            s.add(key)
            buf.append(s)
    while buf:
        k = buf.pop()
        if done & set(k):
            done |= k
    return True if len(done) == len(graph) else False


async def is_strongly_connected(graph: dict) -> tuple:
    """
    Функция проверяет граф на сильную связность. Если граф не является сильно связным, то функция возвращает список
    вершин, которые являются сильно связными

    :param graph: Граф
    :return: True / False и список вершин
    """
    buf = []
    buf.extend(graph[0])
    done = set()
    done.add(0)
    while buf:
        node = buf.pop(0)
        if node not in done:
            done.add(node)
            buf.extend(graph[node])
    if len(done) == len(graph):
        return True, 0
    return False, done


async def make_strongly_connected(graph: dict) -> None:
    """На выходе получаем сильно связный граф

    :param graph: Граф слабой связности
    """

    def count_edges() -> tuple:
        """Считает у каждого узла кол-во входящих и исходящих ребер

        :return: 2 Массива - один с кол-вом входящих ребер, второй - с кол-вом исходящих ребер
        """
        res_in = [0] * len(graph)
        res_out = [len(graph[s]) for s in graph]
        for s in graph:
            for d in graph[s]:
                res_in[d] += 1
        return res_in, res_out

    def update_edges(source_node: int, destination_node: int) -> None:
        graph[source_node].append(destination_node)
        edges_out[source_node] += 1
        edges_in[destination_node] += 1

    edges_in, edges_out = count_edges()
    # print(f"Edges in = {edges_in} \n Edges out = {edges_out}")
    n = len(graph) - 1
    w = (n + 1) // 2
    if n <= 6:
        diff = n - 1
    elif n < 12:
        diff = w
    else:
        diff = (n + 1) // 3
    # print(f"Len = {n}, diff={diff}")
    zero_in = [i for i in range(n + 1) if edges_in[i] <= 1 and i]
    zero_out = [i for i in range(n + 1) if edges_out[i] <= 1 and i < w - 1]
    # print(f"Zero in = {zero_in}\nZero out = {zero_out}")
    if edges_out[0] < randint(2, 4):
        flag = False
        for node in zero_in:
            if node <= w and node not in graph[0]:
                update_edges(0, node)
                flag = True
                if edges_in[node] > 1:
                    zero_in.remove(node)
            if flag:
                break
        for x in range(1, w + 1):
            if flag:
                break
            if edges_in[x] < 3 and x not in graph[0]:
                update_edges(0, x)
                flag = True
    if edges_in[n] < randint(3, 4):
        flag = False
        for node in zero_out:
            if node >= w and n not in graph[node]:
                update_edges(node, n)
                flag = True
                if edges_out[node] > 1:
                    zero_out.remove(node)
            if flag:
                break
        for x in range(w, n):
            if flag:
                break
            if edges_out[x] < 3 and n not in graph[x]:
                update_edges(x, n)
                flag = True
    while zero_out:
        x = zero_out.pop(0)
        k = randint(1, 2)
        while k:
            for node in zero_in:
                if (
                    x != node
                    and abs(node - x) <= diff
                    and x not in graph[node]
                    and node not in graph[x]
                ):
                    update_edges(x, node)
                    if edges_in[node] > 1:
                        zero_in.remove(node)
                    k -= 1
                if not k:
                    break
            if not k:
                break
            for i in range(x + 1, n):
                if not k:
                    break
                if abs(i - x) <= diff and x not in graph[i] and i not in graph[x]:
                    update_edges(x, i)
                    k -= 1
            break
    while zero_in:
        x = zero_in.pop(0)
        k = randint(1, 2)
        while k:
            nodes = [x for x in range(1, n - 1)]
            shuffle(nodes)
            for i in nodes:
                if (
                    x != i
                    and abs(i - x) <= diff
                    and len(graph[i]) <= randint(2, 3)
                    and x not in graph[i]
                    and i not in graph[x]
                ):
                    update_edges(i, x)
                    k -= 1
                if not k:
                    break
            break
    flag, good_nodes = await is_strongly_connected(graph)
    while not flag:
        # print("Is not strongly connected after first round")
        bad_nodes = set(graph.keys()) - good_nodes
        # print(bad_nodes)
        last_nodes = [i for i in range(1, n - 1)]
        shuffle(last_nodes)
        # print(f"last nodes in strongly connected = {last_nodes}")
        while bad_nodes:
            x = bad_nodes.pop()
            for i in last_nodes:
                if (
                    x != i
                    and abs(i - x) <= diff
                    and x not in graph[i]
                    and i not in graph[x]
                    and len(graph[i]) < 3
                ):
                    update_edges(i, x)
                    break
        flag, good_nodes = await is_strongly_connected(graph)
    edges_in, edges_out = count_edges()
    # must_edges = check_ways(graph, diff)
    for node in graph:
        if node == n or node == 0:
            continue
        if (len(graph[node]) == 3 and random() > 0.4) or (len(graph[node]) > 3):
            node_list = list(graph[node])
            k = node_list.pop(0)
            while node_list and edges_in[k] < 2:
                # print(k)
                k = node_list.pop(0)
            graph[node].remove(k)
            # print(f"Edge ({node}, {k}) was removed")
    await check_ways(graph, diff)
    return


async def check_ways(graph: dict, diff: int) -> None:
    """
    Функция проверяет, что из каждой вершины выходит хотя бы 1 ребро, ведущее дальше, а не возвращающееся уже к пройденным вершинам

    :param graph: граф
    :param diff: максимально допустимая разница между вершинами для существования ребра между ними
    """
    way_len = [0] * len(graph)
    buf = [0]
    while buf:
        x = buf.pop()
        for y in graph[x]:
            if not way_len[y] or way_len[y] > way_len[x] + 1:
                way_len[y] = way_len[x] + 1
                if y not in buf:
                    buf.append(y)
    for node in graph:
        amount_back_nodes = 0
        cur_way = way_len[node]
        for y in graph[node]:
            if way_len[y] <= cur_way:
                amount_back_nodes += 1
        # print(f"For node {node} amount back nodes = {amount_back_nodes}, cur.way = {cur_way}, amount of nodes = {len(graph[node])}")
        if amount_back_nodes == len(graph[node]) and node != len(graph) - 1:
            flag = True
            last_nodes = [
                i
                for i in range(len(graph))
                if 1 <= way_len[i] - cur_way or i == len(graph) - 1
            ]
            shuffle(last_nodes)
            while len(graph[node]) >= 3:
                graph[node].remove(min(graph[node]))
                # print("1 Node was removed")
            # print(f"last nodes in check_ways = {last_nodes}")
            for x in last_nodes:
                if (
                    x not in graph[node]
                    and node not in graph[x]
                    and abs(node - x) <= diff
                ):
                    graph[node].append(x)
                    flag = False
                    # print(f"Edge ({node}, {x}) was added")
                    break
            if flag:
                first_nodes = [x for x in graph if way_len[x] < cur_way]
                for x in first_nodes:
                    if node not in graph[x] and abs(node - x) <= diff:
                        graph[x].append(node)
                        # print(f"Edge ({x}, {node}) was added")
                        break
    return


async def check_graph_flow(graph) -> bool:
    """
    Функция проверяет каждую вершину графа на баланс потока

    :param graph: граф
    :return: True/False
    """
    first = 0
    n = len(graph)
    flow_in = [0] * len(graph)
    flow_out = [sum(list(graph[node].values())) for node in graph]
    for node in graph:
        for x in graph[node]:
            flow_in[x] += graph[node][x]
    # print(flow_in)
    # print(flow_out)
    for node in range(first + 1, n - 1):
        if flow_out[node] != flow_in[node]:
            return False
    if flow_out[first] != flow_in[n - 1]:
        return False
    return True


async def make_flow(base: dict, reversed_cut: list, min_flow=20, max_flow=40) -> tuple:
    """Расставляет поток в графе

    :param max_flow: Верхняя граница максимального потока
    :param min_flow: Нижняя граница максимального потока
    :param base: граф, в котором нужно провести поток
    :param reversed_cut: ребра, входящие в обратный разрез
    :return: граф с потоком, максимальный поток
    """
    graph = {x: {y: 0 for y in base[x]} for x in base}
    done = []
    buf = deque()
    n = len(graph) - 1
    flow = randint(min_flow, max_flow)
    input_flow = [0] * len(graph)

    def update_flow(node: int, fl: int) -> bool:
        # print(f"In upgrade flow for node {node}")
        nodes = set(graph[node]) - set(done)
        if nodes:
            f = random_flow(len(nodes), fl)
            for x in nodes:
                k = f.pop()
                graph[node][x] += k
                input_flow[x] += k
            return True
        return False

    def add_flow(node):
        if node == n:
            return
        done.append(node)
        if node == 0:
            f = random_flow(len(graph[node]), flow)
        else:
            z = list(
                filter(lambda y: (node, y) in reversed_cut, list(graph[node].keys()))
            )
            f = random_flow(len(graph[node]) - len(z), input_flow[node])
        new_nodes = [
            x for x in graph[node] if x not in done and (node, x) not in reversed_cut
        ]
        done_nodes = [
            x for x in graph[node] if x in done and (node, x) not in reversed_cut
        ]
        already_added = []
        while done_nodes:
            x = done_nodes.pop(0)
            added_flow = f.pop()
            if update_flow(x, added_flow):
                graph[node][x] += added_flow
                input_flow[x] += added_flow
            else:
                if new_nodes or done_nodes:
                    f[0] += added_flow
                else:
                    if already_added and update_flow(already_added[0], added_flow):
                        # print("Update flow to already added")
                        graph[node][already_added[0]] += added_flow
                        input_flow[already_added[0]] += added_flow
            already_added.append(x)
        while new_nodes:
            x = new_nodes.pop(0)
            added_flow = f.pop()
            if x not in buf:
                buf.append(x)
            graph[node][x] += added_flow
            input_flow[x] += added_flow
        while buf:
            add_flow(buf.popleft())
        return

    add_flow(0)
    return graph, flow


async def make_cut(graph: dict) -> tuple:
    """Делает разрез в графе

    :param graph: граф
    :return: Граф изменяется, если потребуется. Возвращаются вершины, входящие в А и В, прямые ребра, обратные ребра
    """
    source = 0
    sink = len(graph) - 1
    A = [0]
    B = [i for i in range(1, sink + 1)]
    cut = [(0, i) for i in graph[0]]
    r_cut = []
    r_cutbest, Abest, Bbest, cutbest = r_cut.copy(), A.copy(), B.copy(), cut.copy()
    # print("first", A, B, cut, r_cut)
    while len(A) <= len(B):
        node = 0
        for x, y in cut:
            if y != sink:
                node = y
                break
        if node == 0:
            break
        A.append(node)
        B.remove(node)
        cut = list(filter(lambda s: s[1] not in A, cut))
        cut.extend([(node, i) for i in graph[node] if i in B])
        r_cut = [(s, d) for s in graph for d in graph[s] if s in B and d in A]
        # print("in cycle", A, B, cut, r_cut)
        if (len(r_cutbest) == 0 and (len(r_cut) > 0 or len(Abest) <= 4)) or (
            len(r_cutbest) <= 2
            and (
                len(r_cut) < 4
                and len(A) <= sink // 2
                and (len(cut) <= len(cutbest) or len(Abest) <= 3)
            )
        ):
            r_cutbest, Abest, Bbest, cutbest = (
                r_cut.copy(),
                A.copy(),
                B.copy(),
                cut.copy(),
            )
        # else:
        #     if 0 < len(r_cut) < len(r_cutbest):
        #         r_cutbest, Abest, Bbest, cutbest = r_cut.copy(), A.copy(), B.copy(), cut.copy()
        # print("Best is new", Abest, Bbest, cutbest, r_cutbest)
    if len(r_cutbest) == 0:
        x = A[len(A) - 1]
        for node in B:
            if node != sink and x not in graph[node] and node not in graph[x]:
                graph[node].append(x)
                r_cutbest.append((node, x))
                # print("Add extra reverse edge")
                break
    await check_reversed_cut(graph, sorted(Abest), sorted(Bbest), r_cutbest)
    return sorted(Abest), sorted(Bbest), cutbest, r_cutbest


async def check_reversed_cut(graph: dict, A: list, B: list, r_cut: list) -> None:
    """
    Функция проверяет, чтобы из каждой вершины, из которой идет обратное ребро, шло не только обратное ребро.
    Иначе добавляет ребро

    :param graph: граф
    :param A: вершины, входящие в подмножество А
    :param B: вершины, входящие в подмножество В
    :param r_cut: Обратные ребра разреза
    """
    nodes_of_r_cut = list({x[0] for x in r_cut})
    for node in nodes_of_r_cut:
        dest_nodes = [x for x in graph[node] if x in A]
        if len(dest_nodes) == len(graph[node]):
            for x in B:
                if node not in graph[x] and x != node:
                    graph[node].append(x)
                    break
    return


async def make_throughput(
    graph: dict, cut_edges: list, min_weight=1, max_weight=60
) -> None:
    """Функция расставляет пропускные способности ребер

    :param graph: граф
    :param cut_edges: ребра, входящие в разрез
    :param min_weight: минимальный вес ребра
    :param max_weight: максимальный вес ребра
    :return: Граф изменяется, ничего не возвращается
    """
    for x in graph:
        for y in graph[x]:
            if (x, y) in cut_edges:
                continue
            f = graph[x][y]
            add = (
                randint(1, max_weight - f + 1)
                if min_weight <= f < max_weight
                else randint(min_weight - f + 1, max_weight - f + 1)
            )
            graph[x][y] += add
    return


# ======================================= НЕ ИСПОЛЬЗУЕТСЯ ====================================================
async def make_cut_2(graph: dict) -> tuple:
    """Делает разрез в графе

    :param graph: граф
    :return: Граф изменяется, если потребуется. Возвращаются вершины, входящие в А и В, прямые ребра, обратные ребра
    """

    def number_of_input_edges(node) -> int:
        l = 0
        for x in graph:
            for y in graph[x]:
                if y == node:
                    l += 1
        return l

    source = 0
    sink = len(graph) - 1
    buf = []
    cut = []
    A = [source, graph[source][0]]
    buf.extend(list(set(graph[0]) - set(A)))
    buf.extend(graph[A[1]])
    B = list(set(graph.keys()) - set(A))
    for node in A:
        for x in graph[node]:
            if x in B:
                cut.append((node, x))
    if len(graph[source]) > 3:
        for x in graph[source]:
            if random() > 0.3:
                A.append(x)
                buf.extend(graph[x])
    else:
        for x in graph[source]:
            A.append(x)
            buf.extend(graph[x])
    while buf:
        x = buf.pop()
        if random() > 0.5 and x not in A and x <= sink // 2:
            A.append(x)
    cutA = set(A)
    cutB = set(graph.keys()) - cutA
    cut = []
    reverse_cut = []
    flag = False
    k = 0
    for node in cutA:
        for x in graph[node]:
            if x in cutB:
                cut.append((node, x))
    if not cut:
        flag = True
        k = randint(2, 4)
    for node in cutB:
        for x in graph[node]:
            if x in cutA:
                if flag:
                    k -= 1
                    cut.append((x, node))
                    graph[x].append(node)
                    graph[node].remove(x)
                    if not k:
                        flag = False
                else:
                    reverse_cut.append((node, x))
                if not set(graph[node]) - cutA:
                    nodes = list(cutB)
                    nodes.remove(node)
                    while nodes:
                        x = nodes.pop()
                        if node not in graph[x]:
                            graph[node].append(x)
                            break
    if len(reverse_cut) >= len(cut):
        for x, y in reverse_cut:
            if set(graph[x]) - cutA and number_of_input_edges(y) > 1:
                graph[y].append(x)
                graph[x].remove(y)
    if not reverse_cut:
        k = randint(1, 2) if sink > 6 else 1
        A = sorted(list(cutA))
        B = sorted(list(cutB))
        while k and A and B:
            xa = A.pop()
            xb = B.pop(0)
            if xa not in graph[xb] and xb not in graph[xa]:
                graph[xb].append(xa)
                reverse_cut.append((xb, xa))
                k -= 1
    return sorted(list(cutA)), sorted(list(cutB)), cut, reverse_cut


async def generate_graph_with_p(n: int, p: float) -> dict:
    """Генерирует рандомный орграф в виде словаря с некоторой вероятностью p

    :param n: количество вершин
    :param p: вероятность существования ребра между этими двумя вершинами
    :return: dict
    """
    graph = {i: [] for i in range(n)}
    while True:
        # print(is_weakly_connected(graph))
        # print(graph)
        for i in range(n - 1):
            for j in range(i + 1, n):
                if round(random(), 3) <= p:
                    graph[i].append(j)
        flag = await is_weakly_connected(graph)
        if flag:
            break
        else:
            graph = {i: [] for i in range(n)}
    return graph
