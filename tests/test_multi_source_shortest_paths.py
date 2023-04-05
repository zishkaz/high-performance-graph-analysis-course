import pytest

from project.shortest_paths import multi_source_shortest_paths
from tests.utils import load_float_adj_matrix


@pytest.mark.parametrize(
    "edges, source, ans",
    [
        (
            [(0, 1.0, 1), (1, 1.0, 2)],
            [0],
            [(0, [0.0, 1.0, 2.0])],
        ),
        (
            [(0, 1.0, 1), (1, 1.0, 2), (2, 1.0, 0)],
            [0, 2],
            [(0, [0.0, 1.0, 2.0]), (2, [1.0, 2.0, 0.0])],
        ),
        (
            [(0, 1.0, 1), (0, 5.0, 2), (1, 2.0, 2)],
            [0],
            [(0, [0.0, 1.0, 3.0])],
        ),
    ],
)
def test_multi_source_shortest_paths_correct(edges, source, ans):
    graph = load_float_adj_matrix(edges)
    assert multi_source_shortest_paths(graph, source) == ans


def test_multi_source_shortest_paths_error():
    edges = [(0, -1.0, 0)]
    graph = load_float_adj_matrix(edges)
    with pytest.raises(ValueError):
        multi_source_shortest_paths(graph, [0])
