import pandas as pd
import pytest
from assertpy import assert_that

from sql_test_kit.column import Column
from sql_test_kit.query_interpolation import (
    QueryInterpolator,
)
from sql_test_kit.table import Table


def test_query_interpolator_should_replace_table_names_in_string_by_data_literals():
    # Given
    sales_amount_col = "SALES_AMOUNT"

    sales_table = Table(
        table_path="sales_table_path",
        columns=[
            Column(sales_amount_col, "INT64"),
        ],
    )

    sales_table_data = pd.DataFrame(
        {
            sales_amount_col: [1],
        }
    )

    query = f"""
        SELECT * 
        FROM {sales_table}
    """

    # When
    interpolated_query = QueryInterpolator() \
        .add_input_table(table=sales_table, data=sales_table_data) \
        .interpolate_query(query)

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


def test_query_interpolator_data_interpolation_should_fail_if_some_tables_are_absent_from_query():
    # Given
    sales_amount_col = "SALES_AMOUNT"
    sales_table = Table(
        table_path="sales_table_path",
        columns=[
            Column(sales_amount_col, "INT64"),
        ],
    )
    sales_table_data = pd.DataFrame(
        {
            sales_amount_col: [1],
        }
    )

    other_table = Table(
        table_path="other_table_path",
        columns=[],
    )
    other_table_data = pd.DataFrame()

    query = f"""
        SELECT * 
        FROM {sales_table}
    """

    # When / Then
    with pytest.raises(ValueError):
        QueryInterpolator() \
            .add_input_table(table=sales_table, data=sales_table_data) \
            .add_input_table(table=other_table, data=other_table_data) \
            .interpolate_query(query)


def test_query_interpolator_data_interpolation_should_not_fail_if_some_tables_are_absent_from_query_but_no_check():
    # Given
    sales_amount_col = "SALES_AMOUNT"
    sales_table = Table(
        table_path="sales_table_path",
        columns=[
            Column(sales_amount_col, "INT64"),
        ],
    )
    sales_table_data = pd.DataFrame(
        {
            sales_amount_col: [1],
        }
    )

    other_table = Table(
        table_path="other_table_path",
        columns=[],
    )
    other_table_data = pd.DataFrame()

    query = f"""
        SELECT * 
        FROM {sales_table}
    """

    # When
    try:
        QueryInterpolator() \
            .add_input_table(table=sales_table, data=sales_table_data) \
            .add_input_table(table=other_table, data=other_table_data) \
            .interpolate_query(query, check_tables_in_query=False)

    # Then
    except ValueError:
        pytest.fail(
            "Interpolation tables should not be checked if check_tables_in_query parameter is False"
        )
