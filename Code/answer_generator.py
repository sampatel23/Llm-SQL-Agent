import google.generativeai as genai

from code.config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel(
    model_name="gemini-2.5-flash"
)


def generate_answer(question: str, result: list):
    """
    Convert SQL results into a natural language answer.
    """

    if not result:
        return "No matching records were found."

    prompt = f"""
You are a business analyst.

User Question:
{question}

SQL Result:
{result}

Write a concise answer in 1-2 sentences.

Do not mention SQL.
Do not mention databases.
Be direct and professional.
"""

    response = model.generate_content(prompt)

    return response.text.strip()