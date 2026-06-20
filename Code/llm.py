import google.generativeai as genai

from code.config import GEMINI_API_KEY
from code.prompts import SQL_GENERATION_PROMPT


# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel(
    model_name="gemini-2.5-flash"
)


def generate_sql(question: str, schema: str) -> str:
    """
    Convert natural language question into SQL.
    """

    prompt = SQL_GENERATION_PROMPT.format(
        schema=schema,
        question=question
    )

    response = model.generate_content(prompt)

    sql_query = response.text.strip()

    return sql_query