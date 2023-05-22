import json
from pathlib import Path
from typing import List

from networkx import DiGraph
from pygraphblas import Matrix


def load_test_cases_json_bfs(path: Path) -> List:
    matrix, source, ans = [], [], []

    with open(path, "r") as file:
        cases = json.load(file)["cases"]
        for case in cases:
            list1, list2 = case["matrix"]
            n = max(list1 + list2) + 1
            matrix.append(
                Matrix.from_lists(list1, list2, [True] * len(list1), nrows=n, ncols=n)
            )
            source.append(case["source"])
            ans.append(case["ans"])

    return list(zip(matrix, source, ans))


# TODO: implement duplicated code better if another function like this emerges
def load_test_cases_json_triangles(path: Path) -> List:
    matrix, ans = [], []

    with open(path, "r") as file:
        cases = json.load(file)["cases"]
        for case in cases:
            list1, list2 = case["matrix"]
            n = max(list1 + list2) + 1
            m = Matrix.from_lists(list1, list2, [True] * len(list1), nrows=n, ncols=n)
            m += m.transpose()
            matrix.append(m)
            ans.append(case["ans"])

    return list(zip(matrix, ans))


def load_float_adj_matrix(edge_list: List, directed=True) -> Matrix:
    if not directed:
        edge_list += [(j, w, i) for i, w, j in edge_list]
    u, w, v = zip(*edge_list)
    n = max(u + v) + 1
    return Matrix.from_lists(u, v, w, nrows=n, ncols=n)


def load_di_graph_unweighted(edge_list: List) -> DiGraph:
    graph = DiGraph()
    for u, _, v in edge_list:
        graph.add_node(u)
        graph.add_node(v)
        graph.add_edge(u, v)

    return graph
