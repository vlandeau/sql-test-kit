from dataclasses import dataclass
from typing import List

from sql_test_kit import Column
from sql_test_kit.table import AbstractTable


@dataclass
class BigqueryTable(AbstractTable):
    project: str
    dataset: str
    table: str
    columns: List[Column]

    @property
    def table_path(self) -> str:
        return f"`{self.project}.{self.dataset}.{self.table}`"
