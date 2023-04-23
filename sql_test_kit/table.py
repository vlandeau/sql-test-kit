from abc import ABC
from dataclasses import dataclass
from typing import List, Protocol

from sql_test_kit.column import Column


class AbstractTable(ABC):
    table_path: str
    columns: List[Column]

    def get_table_path(self) -> str:
        return self.table_path

    def __str__(self):
        return self.get_table_path()

    def __repr__(self):
        return self.get_table_path()


@dataclass
class Table(AbstractTable):
    table_path: str
    columns: List[Column]
