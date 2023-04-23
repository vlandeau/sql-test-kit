from dataclasses import dataclass
from typing import List

from sql_test_kit.column import Column


@dataclass
class Table:
    table_path: str
    columns: List[Column]

    def __str__(self):
        return self.table_path

    def __repr__(self):
        return self.table_path
