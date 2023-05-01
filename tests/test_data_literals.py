import pandas as pd
from assertpy import assert_that

from sql_test_kit import Table, Column
from sql_test_kit.data_literals import DataLiteralsBuilder
from sql_test_kit.interpolation_data import InterpolationData


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
    data_literals_query = DataLiteralsBuilder().get_data_literals_query(interpolation_data)

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
    data_literals_query = DataLiteralsBuilder().get_data_literals_query(interpolation_data)

    # Then
    assert_that(data_literals_query.replace("\n", "").replace("\t", "")).is_equal_to(
        "()"
    )
