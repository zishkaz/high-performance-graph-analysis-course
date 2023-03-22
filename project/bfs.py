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
