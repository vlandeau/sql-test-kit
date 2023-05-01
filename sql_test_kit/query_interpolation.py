from __future__ import annotations

from typing import List

import pandas as pd

from sql_test_kit.data_literals import DataLiteralsBuilder
from sql_test_kit.interpolation_data import InterpolationData
from sql_test_kit.table import AbstractTable


class QueryInterpolator:
    interpolation_data: List[InterpolationData]
    data_literals_builder: DataLiteralsBuilder = DataLiteralsBuilder()

    def __init__(self):
        self.interpolation_data = []

    def add_input_table(
        self, table: AbstractTable, data: pd.DataFrame
    ) -> QueryInterpolator:
        self.interpolation_data.append(InterpolationData(table, data))
        return self

    def interpolate_query(self, query: str, check_tables_in_query: bool = True) -> str:
        interpolated_query = query
        for interpolation_data in self.interpolation_data:
            table_path = interpolation_data.table.table_path
            if check_tables_in_query and table_path not in interpolated_query:
                raise ValueError(
                    f"You are trying to interpolate {table_path} data, "
                    f"but this table is not used in the query."
                )
            interpolated_query = interpolated_query.replace(
                table_path,
                self.data_literals_builder.get_data_literals_query(interpolation_data),
            )
        return interpolated_query
