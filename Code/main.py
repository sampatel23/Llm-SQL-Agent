from fastapi import FastAPI, Depends, HTTPException

from code.models import QuestionRequest
from code.auth import verify_api_key

from code.database import (
    get_schema,
    execute_query
)

from code.llm import generate_sql

from code.validator import (
    validate_sql,
    add_limit_if_missing
)

from code.answer_generator import generate_answer


app = FastAPI(
    title="Sparkline AI SQL Assistant"
)


BLOCKED_KEYWORDS = [
    "delete",
    "drop",
    "remove",
    "update",
    "insert",
    "truncate",
    "alter",
    "create"
]


@app.get("/")
def root():
    return {
        "message": "Sparkline AI SQL Assistant Running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.post("/ask")
def ask_question(
    request: QuestionRequest,
    _: str = Depends(verify_api_key)
):

    try:

        # Reject modification requests
        question_lower = request.question.lower()

        for keyword in BLOCKED_KEYWORDS:

            if keyword in question_lower:

                return {
                    "question": request.question,
                    "sql": None,
                    "tables_used": [],
                    "result": [],
                    "answer": (
                        "Only read-only analytical questions "
                        "are supported."
                    )
                }

        # Step 1: Extract schema
        schema = get_schema()

        # Step 2: Generate SQL
        generated_sql = generate_sql(
            request.question,
            schema
        )

        # Step 3: Add LIMIT if missing
        generated_sql = add_limit_if_missing(
            generated_sql
        )

        # Step 4: Validate SQL and extract tables
        tables_used = validate_sql(
            generated_sql
        )

        # Step 5: Execute query
        result = execute_query(
            generated_sql
        )

        # Step 6: Generate business-friendly answer
        answer = generate_answer(
            request.question,
            result
        )

        return {
            "question": request.question,
            "sql": generated_sql,
            "tables_used": tables_used,
            "result": result,
            "answer": answer
        }

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Internal Server Error: {str(e)}"
        )