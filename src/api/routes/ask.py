from fastapi import APIRouter
from src.utils.retrival import retrive
from src.utils.prompts import get_answer
from src.config import config
from src.api.schema import AskRequest, AskResponse

router = APIRouter()

@router.post("/api/v1/ask", response_model=AskResponse)
def ask_question(request: AskRequest):
    
    response = get_answer(request.question, retrive(request.question, top_k=config.TOP_K, scope=config.SCOPE))
    answer = response["answer"]
    if response["status"] == "incomplete":
        reason = response["incomplete_reason"]
        if reason in ["max_output_tokens", "max_tokens"]:
            answer += "\n\n[Note: The answer may be incomplete due to reaching the maximum output token limit.]"

        else:
            answer += f"\n\n[Note: The answer may be incomplete. Reason: {response['incomplete_reason']}]"

    return AskResponse(**{**response, "answer": answer, 'session_id': request.session_id})

