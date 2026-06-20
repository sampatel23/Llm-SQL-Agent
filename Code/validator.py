import sqlglot
from sqlglot import expressions as exp


ALLOWED_TABLES = {
    "customers",
    "products",
    "sales",
    "employees"
}


def validate_sql(sql_query: str):
    """
    Validate SQL and extract tables used.
    """

    try:
        parsed_queries = sqlglot.parse(sql_query)

        if len(parsed_queries) != 1:
            raise ValueError(
                "Multiple SQL statements are not allowed."
            )

        query = parsed_queries[0]

        if not isinstance(query, exp.Select):
            raise ValueError(
                "Only SELECT queries are allowed."
            )

        tables_used = []

        for table in query.find_all(exp.Table):
            table_name = table.name

            tables_used.append(table_name)

            if table_name not in ALLOWED_TABLES:
                raise ValueError(
                    f"Unauthorized table: {table_name}"
                )

        return list(set(tables_used))

    except Exception as e:
        raise ValueError(
            f"SQL Validation Failed: {str(e)}"
        )
    
def add_limit_if_missing(sql_query):
    
    if "LIMIT" not in sql_query.upper():
        sql_query = sql_query.rstrip(";")
        sql_query += " LIMIT 100"

    return sql_query