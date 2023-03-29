import pathlib

import pytest

from project.bfs import bfs, ms_bfs
from tests.utils import load_test_cases_json_bfs

test_bfs_path = pathlib.Path(__file__).parent / "resources" / "test_bfs.json"
test_ms_bfs_path = pathlib.Path(__file__).parent / "resources" / "test_ms_bfs.json"


@pytest.mark.parametrize("case", load_test_cases_json_bfs(test_bfs_path))
def test_bfs(case):
    matrix, source, ans = case
    assert bfs(matrix, source) == ans


@pytest.mark.parametrize("case", load_test_cases_json_bfs(test_ms_bfs_path))
def test_ms_bfs(case):
    matrix, sources, ans = case
    assert ms_bfs(matrix, sources) == ans
