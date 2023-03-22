from typing import List

from pygraphblas import Vector, Matrix, INT64, BOOL
from pygraphblas.descriptor import RSC, S, C


def bfs(graph: Matrix, source: int) -> List[int]:
    """
    Performs BFS of a directed graph as matrix starting from the source vertex

    :param graph: graph as Matrix
    :param source: source vertex as int
    :return: list of distances as ints from the source vertex
    """
    size = graph.nrows
    front = Vector.sparse(BOOL, size)
    front[source] = True
    res = Vector.sparse(INT64, size)
    curr_depth = 0

    while front.nvals:
        res[front] = curr_depth
        front.vxm(graph, out=front, mask=res, desc=RSC)
        curr_depth += 1

    res.assign_scalar(-1, mask=res, desc=S & C)

    return list(res.vals)


def ms_bfs(graph: Matrix, sources: List) -> List:
    """
    Performs BFS of a directed graph as matrix starting from the multiple source vertices

    :param graph: graph as Matrix
    :param sources: source vertices as ints
    :return: list: source, list of parents for the shortest path of each node; source = -1, unreachable nodes = -2
    """
    n = graph.ncols
    m = len(sources)

    parents = Matrix.sparse(INT64, nrows=m, ncols=n)
    front = Matrix.sparse(INT64, nrows=m, ncols=n)

    for r, s in enumerate(sources):
        front[r, s] = -1

    while front.nvals:
        parents.assign_matrix(value=front, mask=front, desc=S)
        front.apply(INT64.POSITIONJ, out=front)
        front.mxm(
            other=graph, semiring=INT64.MIN_FIRST, out=front, mask=parents, desc=RSC
        )

    return [
        [v, [parents.get(i, j, default=-2) for j in range(n)]]
        for i, v in enumerate(sources)
    ]
