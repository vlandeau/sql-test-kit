from dataclasses import dataclass
from typing import List

from sql_test_kit import Column
from sql_test_kit.data_literals import DataLiteralsBuilder
from sql_test_kit.query_interpolation import QueryInterpolator
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


class BigQueryDataLiteralsBuilder(DataLiteralsBuilder):
    CAST_OPERATOR: str = "SAFE_CAST"


class BigQueryInterpolator(QueryInterpolator):
    data_literals_builder = BigQueryDataLiteralsBuilder()
