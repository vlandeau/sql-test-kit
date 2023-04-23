# sql-test-kit

This is a framework for testing SQL queries.
It works by directly running the queries against the targeted engine, thus being robust to any change in the
corresponding SQL dialect.
Moreover, it is currently focused on interpolating test data directly inside the SQL queries, making the test much
quicker than if it were creating temporary tables.

# Application example

You can find an example in applying the framework to bigquery in the [test_bigquery](tests/test_bigquery.py) file.
