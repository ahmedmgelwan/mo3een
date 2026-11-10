import time

from fastapi import FastAPI
from openai import OpenAI

from src.api.schema import AskRequest, AskResponse
from utils.llm_client import GenerationClient
from src.config import config

openai_client = OpenAI(
    api_key=config.OPEN_AI_KEY, base_url=config.BASE_URL, timeout=config.REQUEST_TIMEOUT
)

INSTRUCTIONS = "You are a helpful assistant.\nYou always respond in a concise and accurate manner.\nYou never make up information.\nYou always provide references for your answers.\nYou always respond in the language of the question.\nif the question is not clear, you ask for clarification.\nif you do not know the answer, you say so."


app = FastAPI(title=config.APP_NAME, version=config.APP_VERSION)


@app.get("/health")
def health_check():
    return {
        "App Name": config.APP_NAME,
        "App Version": config.APP_VERSION,
        "Status": "ok",
        "Model Name": config.MODEL_NAME,
    }


@app.post("/api/v1/ask", response_model=AskResponse)
def ask_question(request: AskRequest):
    messages = [
        {"role": "system", "content": INSTRUCTIONS},
        {"role": "user", "content": request.question},
    ]

    generation_client = GenerationClient(client=openai_client)
    response = generation_client.generate_answer(
        messages=messages,
        model=config.MODEL_NAME,
        temperature=0.2,
        max_output_tokens=config.MAX_GENERATED_TOKENS
    )
    answer = response["answer"]
    if response["status"] == "incomplete":
        reason = response["incomplete_reason"]
        if reason in ["max_output_tokens", "max_tokens"]:
            answer += "\n\n[Note: The answer may be incomplete due to reaching the maximum output token limit.]"

        else:
            answer += f"\n\n[Note: The answer may be incomplete. Reason: {response['incomplete_reason']}]"



    return AskResponse(**{**response, 'answer': answer})
