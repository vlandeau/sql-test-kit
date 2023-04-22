from dataclasses import dataclass
from typing import List

from sql_test_kit.column import Column


@dataclass
class Schema:
    columns: List[Column]
