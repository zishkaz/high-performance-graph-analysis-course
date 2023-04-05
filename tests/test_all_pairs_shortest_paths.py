from math import inf

import pytest

from project.shortest_paths import all_pairs_shortest_paths
from tests.utils import load_float_adj_matrix


@pytest.mark.parametrize(
    "edges, ans",
    [
        (
            [(0, 1.0, 1), (1, 1.0, 2), (2, 1.0, 3)],
            [
                (0, [0.0, 1.0, 2.0, 3.0]),
                (1, [inf, 0.0, 1.0, 2.0]),
                (2, [inf, inf, 0.0, 1.0]),
                (3, [inf, inf, inf, 0.0]),
            ],
        ),
        (
            [(0, 1.0, 1), (1, 1.0, 2), (2, 1.0, 0)],
            [(0, [0.0, 1.0, 2.0]), (1, [2.0, 0.0, 1.0]), (2, [1.0, 2.0, 0.0])],
        ),
        (
            [(0, 1.0, 1), (0, 2.0, 2), (1, 1.0, 3), (2, 1.0, 3)],
            [
                (0, [0.0, 1.0, 2.0, 2.0]),
                (1, [inf, 0.0, inf, 1.0]),
                (2, [inf, inf, 0.0, 1.0]),
                (3, [inf, inf, inf, 0.0]),
            ],
        ),
    ],
)
def test_all_pairs_shortest_paths_correct(edges, ans):
    graph = load_float_adj_matrix(edges)
    assert all_pairs_shortest_paths(graph) == ans


def test_all_pairs_shortest_paths_error():
    edges = [(0, -1.0, 0)]
    graph = load_float_adj_matrix(edges)
    with pytest.raises(ValueError):
        all_pairs_shortest_paths(graph)
