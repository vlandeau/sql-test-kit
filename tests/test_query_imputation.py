import pandas as pd
from assertpy import assert_that

from sql_test_kit.column import Column
from sql_test_kit.query_interpolation import (
    replace_table_names_in_string_by_data_literals,
    InterpolationData,
    get_data_literals_query,
)
from sql_test_kit.table import Table


def test_get_data_literals_query():
    # Given
    sales_amount_col = "SALES_AMOUNT"
    sales_date_col = "SALES_DATE"

    sales_table = Table(
        table_path="table",
        columns=[
            Column(sales_amount_col, "INT64"),
            Column(sales_date_col, "DATE"),
        ],
    )

    table_data = pd.DataFrame(
        {
            sales_amount_col: [1, 2, 3],
            sales_date_col: ["2022-01-01", "2022-01-02", "2022-01-03"],
        }
    )

    interpolation_data = InterpolationData(
        table=sales_table,
        data=table_data,
    )

    # When
    data_literals_query = get_data_literals_query(interpolation_data)

    # Then
    expected_data_literals_query = """(
            SELECT CAST("1" AS INT64) AS SALES_AMOUNT, CAST("2022-01-01" AS DATE) AS SALES_DATE
        UNION ALL
            SELECT CAST("2" AS INT64) AS SALES_AMOUNT, CAST("2022-01-02" AS DATE) AS SALES_DATE
        UNION ALL
            SELECT CAST("3" AS INT64) AS SALES_AMOUNT, CAST("2022-01-03" AS DATE) AS SALES_DATE
        )"""

    assert_that(
        data_literals_query.replace("\n", "").replace("\t", "    ").rstrip()
    ).is_equal_to(
        expected_data_literals_query.replace("\n", "").replace("\t", "    ").rstrip()
    )


def test_get_data_literals_query_with_no_data():
    # Given
    sales_table = Table(table_path="table", columns=[])

    table_data = pd.DataFrame()

    interpolation_data = InterpolationData(
        table=sales_table,
        data=table_data,
    )

    # When
    data_literals_query = get_data_literals_query(interpolation_data)

    # Then
    assert_that(data_literals_query.replace("\n", "").replace("\t", "")).is_equal_to(
        "()"
    )


def test_replace_table_names_in_string_by_data_literals():
    # Given
    sales_amount_col = "SALES_AMOUNT"

    sales_table = Table(
        table_path="table_path",
        columns=[
            Column(sales_amount_col, "INT64"),
        ],
    )

    table_data = pd.DataFrame(
        {
            sales_amount_col: [1],
        }
    )

    interpolation_data = InterpolationData(
        table=sales_table,
        data=table_data,
    )

    query = f"""
        SELECT * 
        FROM {sales_table}
    """

    # When
    interpolated_query = replace_table_names_in_string_by_data_literals(
        query, [interpolation_data]
    )

    # Then
    expected_query = f"""
        SELECT * 
        FROM (
            SELECT CAST("1" AS INT64) AS {sales_amount_col}
        )
    """
    assert_that(interpolated_query.replace("\t", "    ").strip()).is_equal_to(
        expected_query.replace("\t", "    ").strip()
    )
