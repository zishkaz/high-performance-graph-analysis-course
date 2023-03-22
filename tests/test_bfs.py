import pathlib

import pytest

from project.bfs import bfs
from tests.utils import load_test_cases_json

test_bfs_path = pathlib.Path(__file__).parent / "resources" / "test_bfs.json"


@pytest.mark.parametrize("case", load_test_cases_json(test_bfs_path))
def test_bfs(case):
    matrix, source, ans = case
    assert bfs(matrix, source) == ans
