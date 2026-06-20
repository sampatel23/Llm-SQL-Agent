from code.database import get_schema
from code.llm import generate_sql


schema = get_schema()

question = "Delete all customers"

sql = generate_sql(
    question=question,
    schema=schema
)

print(sql)