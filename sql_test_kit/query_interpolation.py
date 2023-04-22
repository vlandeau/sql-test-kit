from dataclasses import dataclass
from typing import List

import pandas as pd

from sql_test_kit.table import Table


@dataclass
class InterpolationData:
    table: Table
    data: pd.DataFrame


def replace_table_names_in_string_by_data_literals(query: str,
                                                   interpolation_data_list: List[InterpolationData]) -> str:
    interpolated_query = query
    for interpolation_data in interpolation_data_list:
        interpolated_query = interpolated_query.replace(interpolation_data.table.table_path,
                                                        get_data_literals_query(interpolation_data))
    return interpolated_query


def get_data_literals_query(interpolation_data: InterpolationData) -> str:
    data_dict_list = interpolation_data.data.to_dict(orient="records")
    columns = interpolation_data.table.schema.columns

    return "(\n\t\t\t" + "\n\t\tUNION ALL\n\t\t\t".join([
        "SELECT " + ", ".join([
            f"CAST(\"{record[column.name]}\" AS {column.type}) AS {column.name}"
            for column in columns
        ])
        for record in data_dict_list
    ]) + "\n\t\t)"
