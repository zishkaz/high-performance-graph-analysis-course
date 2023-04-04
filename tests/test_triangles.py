import pathlib

import pytest

from project.triangles import (
    triangles_by_vertex__count,
    cohen_triangles_count,
    sandia_triangles_count,
)
from tests.utils import load_test_cases_json_triangles

test_triangles_total_path = (
    pathlib.Path(__file__).parent / "resources" / "test_triangles_total.json"
)
test_triangles_per_vertex__path = (
    pathlib.Path(__file__).parent / "resources" / "test_triangles_per_vertex.json"
)


@pytest.mark.parametrize(
    "case", load_test_cases_json_triangles(test_triangles_total_path)
)
def test_triangles_total(case):
    matrix, ans = case
    assert (
        cohen_triangles_count(matrix) == ans and sandia_triangles_count(matrix) == ans
    )


@pytest.mark.parametrize(
    "case", load_test_cases_json_triangles(test_triangles_per_vertex__path)
)
def test_triangles_per_vertex(case):
    matrix, ans = case
    assert triangles_by_vertex__count(matrix) == ans
