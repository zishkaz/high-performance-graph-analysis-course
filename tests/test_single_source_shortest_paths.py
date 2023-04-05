from math import inf

import pytest

from project.shortest_paths import single_source_shortest_paths
from tests.utils import load_float_adj_matrix


@pytest.mark.parametrize(
    "edges, source, ans",
    [
        (
            [(0, 1.0, 1), (1, 1.0, 2)],
            1,
            [inf, 0.0, 1.0],
        ),
        (
            [(0, 1.0, 1), (1, 1.0, 2), (2, 1.0, 0)],
            1,
            [2.0, 0.0, 1.0],
        ),
    ],
)
def test_sssp(edges, source, ans):
    graph = load_float_adj_matrix(edges)
    assert single_source_shortest_paths(graph, source) == ans
