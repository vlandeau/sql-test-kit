import pandas as pd
from google.cloud.bigquery import Client

from sql_test_kit import (
    Column,
    replace_table_names_in_string_by_data_literals,
    InterpolationData,
)
from sql_test_kit.bigquery import BigqueryTable


def test_bigquery_query_interpolation():
    # Given
    sales_amount_col = "SALES_AMOUNT"
    sales_date_col = "SALES_DATE"
    sales_table = BigqueryTable(
        project="project",
        dataset="dataset",
        table="table",
        columns=[
            Column(sales_amount_col, "FLOAT64"),
            Column(sales_date_col, "STRING"),
        ],
    )
    current_year_sales_by_day_query = f"""
        SELECT {sales_date_col}, SUM({sales_amount_col}) as {sales_amount_col}
        FROM {sales_table}
        WHERE {sales_date_col} >= "2023-01-01"
        GROUP BY {sales_date_col}
    """
    sales_data = pd.DataFrame(
        {
            "SALES_ID": [1, 2, 3, 4],
            sales_date_col: ["2022-12-31", "2023-01-01", "2023-01-01", "2023-01-02"],
            sales_amount_col: [10, 20, 30, 40],
        }
    )

    # When
    interpolated_query = replace_table_names_in_string_by_data_literals(
        query=current_year_sales_by_day_query,
        interpolation_data_list=[
            InterpolationData(sales_table, sales_data),
        ],
    )
    current_year_sales_by_day_data = Client().query(interpolated_query).to_dataframe()

    # Then
    expected_current_year_sales_by_day_data = pd.DataFrame(
        {
            sales_date_col: ["2023-01-01", "2023-01-02"],
            sales_amount_col: [50, 40],
        }
    )

    pd.testing.assert_frame_equal(
        current_year_sales_by_day_data,
        expected_current_year_sales_by_day_data,
        check_dtype=False,
    )
