from math import inf
from typing import List

from pygraphblas import Matrix, FP64


def single_source_shortest_paths(graph: Matrix, source: int) -> List:
    """Calculates shortest paths in a graph from a single source vertex to each vertex

    :param graph: graph as Matrix
    :param source: source vertex as int
    :return: list of distances from the source vertex
    """
    return multi_source_shortest_paths(graph, [source])[0][1]


def multi_source_shortest_paths(graph: Matrix, source: List) -> List:
    """Calculates shortest paths in a graph from multiple source vertices to each vertex

    :param graph: graph as Matrix
    :param source: source vertices as list of ints
    :return: list of tuples, where each tuple is (source, distances from the source)
    """
    m = len(source)
    n = graph.ncols
    __checks(graph)
    for vertex in source:
        assert vertex in range(n)

    graph = graph.eadd(Matrix.identity(FP64, n, 0.0), FP64.MIN)
    dists = Matrix.sparse(FP64, nrows=m, ncols=n)
    for i, start in enumerate(source):
        dists[i, start] = 0

    for _ in range(n - 1):
        dists.mxm(graph, FP64.MIN_PLUS, out=dists)

    if dists.diag().reduce_float(FP64.min_monoid) < 0:
        raise ValueError("Negative cycle detected")

    res = []
    for i, start in enumerate(source):
        temp = []
        for j in range(n):
            temp.append(dists.get(i, j, default=inf))
        res.append((start, temp))
    return res


def all_pairs_shortest_paths(graph: Matrix) -> List:
    """Calculates shortest paths in a graph between all vertices

    :param graph: graph as Matrix
    :return: list of tuples, where each tuple is (source, distances from the source)
    """
    n = graph.ncols
    __checks(graph)
    graph = graph.eadd(Matrix.identity(FP64, n, 0.0), FP64.MIN)

    dists = graph

    for k in range(n):
        col, row = dists.extract_matrix(col_index=k), dists.extract_matrix(row_index=k)
        dists.eadd(
            col.mxm(row, FP64.MIN_PLUS),
            FP64.MIN,
            out=dists,
        )

    if dists.diag().reduce_float(FP64.min_monoid) < 0:
        raise ValueError("Negative cycle detected")

    res = []
    for i in range(n):
        temp = []
        for j in range(n):
            temp.append(dists.get(i, j, default=inf))
        res.append((i, temp))
    return res


def __checks(matrix: Matrix):
    assert matrix.type == FP64
    assert matrix.square
