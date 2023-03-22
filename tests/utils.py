import json
from pathlib import Path
from typing import List

from pygraphblas import Matrix


def load_test_cases_json(path: Path) -> List:
    matrix, source, ans = [], [], []

    with open(path, "r") as file:
        cases = json.load(file)["cases"]
        for case in cases:
            list1, list2 = case["matrix"]
            n = max(list1 + list2) + 1
            matrix.append(
                Matrix.from_lists(list1, list2, [True] * len(list1), nrows=n, ncols=n)
            )
            source.append(case["source"])
            ans.append(case["ans"])

    return list(zip(matrix, source, ans))
