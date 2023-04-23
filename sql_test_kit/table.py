from abc import ABC
from dataclasses import dataclass
from typing import List

from sql_test_kit.column import Column


class AbstractTable(ABC):
    table_path: str
    columns: List[Column]

    def __str__(self):
        return self.table_path

    def __repr__(self):
        return self.table_path


@dataclass
class Table(AbstractTable):
    table_path: str
    columns: List[Column]
