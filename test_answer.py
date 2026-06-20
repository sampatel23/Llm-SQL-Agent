from code.answer_generator import generate_answer

question = "Who are the top customers by revenue?"

result = [
    {
        "name": "Reliance Digital",
        "total_revenue": 350000
    }
]

answer = generate_answer(
    question=question,
    result=result
)

print(answer)