import heapq
import itertools
from typing import Dict

import networkx as nx
from boltons.queueutils import HeapPriorityQueue


def dijkstra_sssp(graph: nx.DiGraph, source) -> Dict:
    """Calculates shortest paths in a graph from a single source vertex to each vertex using Dijkstra algorithm.

    :param graph: directed graph
    :param source: source vertex as int
    :return: list of distances from the source vertex or inf if a vertex is unreachable
    """
    if source not in graph.nodes:
        raise Exception("Graph doesn't contain given source vertex")

    dists = {node: float("inf") for node in graph.nodes}
    dists[source] = 0
    queue = [(0, source)]

    while queue:
        dist, node = heapq.heappop(queue)

        for succ in graph.successors(node):
            if dists[node] + 1 < dists[succ]:
                dists[succ] = dists[node] + 1
                heapq.heappush(queue, (dists[succ], succ))

    return dists


class DynamicSSSP:
    """Implementation of https://doi.org/10.1006/jagm.1996.0046."""

    def __init__(self, graph: nx.DiGraph, source: int):
        self._graph: nx.DiGraph = graph
        self._source = source
        self._modified_vertices = set()
        self._dists = dijkstra_sssp(graph, source)

    def get_dists(self) -> Dict:
        self._update()
        return self._dists

    def remove_edge(self, u, v):
        self._graph.remove_edge(u, v)
        self._modified_vertices.add(v)

    def add_edge(self, u, v):
        self._graph.add_edge(u, v)
        self._modified_vertices.add(v)

    def _update(self):
        hpq = HeapPriorityQueue(priority_key=lambda x: x)
        rhs = {}
        for node in self._modified_vertices:
            rhs[node] = self._calculate_rhs(node)
            if rhs[node] != self._dists[node]:
                hpq.add(node, priority=min(rhs[node], self._dists[node]))

        while len(hpq) > 0:
            node = hpq.pop()
            if rhs[node] < self._dists[node]:
                self._dists[node] = rhs[node]
                to_update_rhs = self._graph.successors(node)
            else:
                self._dists[node] = float("inf")
                to_update_rhs = itertools.chain(self._graph.successors(node), [node])

            for v in to_update_rhs:
                rhs[v] = self._calculate_rhs(v)
                if rhs[v] != self._dists[v]:
                    hpq.add(v, priority=min(rhs[v], self._dists[v]))
                else:
                    if v in hpq._entry_map:
                        hpq.remove(v)

    def _calculate_rhs(self, node):
        if node == self._source:
            return 0

        return (
            min(
                (self._dists[u] for u in self._graph.predecessors(node)),
                default=float("inf"),
            )
            + 1
        )
