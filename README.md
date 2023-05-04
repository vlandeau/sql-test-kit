# sql-test-kit

This is a framework for testing SQL queries.
It works by directly running the queries against the targeted engine, thus being robust to any change in the
corresponding SQL dialect.
Moreover, it is currently focused on interpolating test data directly inside the SQL queries, making the test much
quicker than if it were creating temporary tables.

# Application example

Using the Table and Column class, you can generate variablized SQL queries such as this :

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

You can then test it this way :

    def test_current_year_sales_by_day_query():
        # Given
        sales_data = pd.DataFrame(
            {
                "SALES_ID": [1, 2, 3, 4],
                sales_date_col: ["2022-12-31", "2023-01-01", "2023-01-01", "2023-01-02"],
                sales_amount_col: [10, 20, 30, 40],
            }
        )
    
        # When
        interpolated_query = QueryInterpolator() \
            .add_input_table(sales_table, sales_data) \
            .interpolate_query(current_year_sales_by_day_query)
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
