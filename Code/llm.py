import google.generativeai as genai

from code.config import GEMINI_API_KEY
from code.prompts import SQL_GENERATION_PROMPT

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel(
    model_name="gemini-2.5-flash"
)


def clean_sql(sql_query: str) -> str:
    """
    Remove markdown formatting if Gemini returns it.
    """

    sql_query = sql_query.replace("```sql", "")
    sql_query = sql_query.replace("```", "")

    return sql_query.strip()


def generate_sql(question: str, schema: str) -> str:

    prompt = SQL_GENERATION_PROMPT.format(
        schema=schema,
        question=question
    )

    response = model.generate_content(prompt)

    sql_query = response.text.strip()

    # Clean Gemini output
    sql_query = clean_sql(sql_query)

    return sql_query