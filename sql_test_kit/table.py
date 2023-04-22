from dataclasses import dataclass

from sql_test_kit.schema import Schema


@dataclass
class Table:
    project: str
    dataset: str
    table: str
    schema: Schema = Schema([])

    @property
    def table_path(self):
        return f"`{self.project}.{self.dataset}.{self.table}`"

    def __str__(self):
        return self.table_path

    def __repr__(self):
        return self.table_path
