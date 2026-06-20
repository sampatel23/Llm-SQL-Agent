from code.database import execute_query

result = execute_query("""
SELECT name, region
FROM customers
LIMIT 3
""")

print(result)