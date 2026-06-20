from code.validator import validate_sql


query = """
SELECT
    c.name,
    SUM(s.amount) AS revenue
FROM customers c
JOIN sales s
    ON c.id = s.customer_id
GROUP BY c.name
"""


tables = validate_sql(query)

print(tables)