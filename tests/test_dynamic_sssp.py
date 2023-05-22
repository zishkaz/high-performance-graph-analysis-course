from math import inf

import pytest
from networkx import DiGraph

from project.sssp_dynamic import dijkstra_sssp, DynamicSSSP
from tests.utils import load_di_graph_unweighted


@pytest.mark.parametrize(
    "edges, source, expected",
    [
        (
            [(0, 1.0, 1), (1, 1.0, 2)],
            1,
            {0: inf, 1: 0, 2: 1},
        ),
        (
            [(0, 1.0, 1), (1, 1.0, 2), (2, 1.0, 0)],
            1,
            {0: 2, 1: 0, 2: 1},
        ),
    ],
)
def test_dijkstra_sssp(edges, source, expected):
    graph = load_di_graph_unweighted(edges)
    assert dijkstra_sssp(graph, source) == expected


def test_dijkstra_sssp_throws_exception():
    graph = DiGraph()
    with pytest.raises(Exception) as _:
        dijkstra_sssp(graph, 10)


@pytest.mark.parametrize(
    "edges, edges_to_add, edges_to_del, source, expected",
    [
        (
            [(0, 1.0, 1), (1, 1.0, 2)],
            [],
            [],
            1,
            {0: inf, 1: 0, 2: 1},
        ),
        (
            [(0, 1.0, 1), (1, 1.0, 2), (2, 1.0, 0)],
            [],
            [(2, 0)],
            1,
            {0: inf, 1: 0, 2: 1},
        ),
        (
            [(0, 1.0, 1), (1, 1.0, 2), (2, 1.0, 3)],
            [(0, 3)],
            [],
            0,
            {0: 0, 1: 1, 2: 2, 3: 1},
        ),
    ],
)
def test_dynamic_sssp(edges, edges_to_add, edges_to_del, source, expected):
    graph = load_di_graph_unweighted(edges)
    init = DynamicSSSP(graph, source)

    for u, v in edges_to_add:
        init.add_edge(u, v)
    for u, v in edges_to_del:
        init.remove_edge(u, v)

    assert init.get_dists() == expected
