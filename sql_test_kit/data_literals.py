from sql_test_kit.interpolation_data import InterpolationData


class DataLiteralsBuilder:
    CAST_OPERATOR: str = "CAST"
    UNION_OPERATOR: str = "UNION ALL"

    def get_data_literals_query(self, interpolation_data: InterpolationData) -> str:
        records = interpolation_data.data.to_dict(orient="records")
        columns = interpolation_data.table.columns

        return (
            "(\n\t\t\t"
            + f"\n\t\t\t{self.UNION_OPERATOR}\n\t\t\t".join(
                [
                    "SELECT "
                    + ", ".join(
                        [
                            f'{self.CAST_OPERATOR}("{record[column.name]}" AS {column.type}) AS {column.name}'
                            for column in columns
                        ]
                    )
                    for record in records
                ]
            )
            + "\n\t\t)"
        )
