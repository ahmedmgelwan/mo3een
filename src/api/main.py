import time
from openai import OpenAI
from fastapi import FastAPI

from src.config import config
from src.api.schema import AskRequest, AskResponse

openai_client = OpenAI(api_key=config.OPEN_AI_KEY, 
                       base_url=config.BASE_URL,
                       timeout=config.REQUEST_TIMEOUT)

INSTRUCTIONS = '\n'.join(
    ['You are a helpful assistant.', 'You always respond in a concise and accurate manner.', 'You never make up information.',
     'You always provide references for your answers.', 'You always respond in the language of the question.',
     'if the question is not clear, you ask for clarification.', 
     'if you do not know the answer, you say so.']
)


app = FastAPI(title=config.APP_NAME, version=config.APP_VERSION)

@app.get('/health')
def health_check():
    return {
        'App Name': config.APP_NAME,
        'App Version': config.APP_VERSION,
        'Status': 'ok',
        'Model Name': config.MODEL_NAME,
    }




@app.post('/api/v1/ask', response_model=AskResponse)
def ask_question(request: AskRequest):
    messages = [
        {"role": "system", "content": INSTRUCTIONS},
        {"role": "user", "content": request.question}
    ]
    start_time = time.perf_counter()

    response = openai_client.responses.create(
        input=messages,
        model=config.MODEL_NAME,
        temperature=0.2,
        max_output_tokens=500
    )
    answer = response.output_text.strip()
    latency_ms = int((time.perf_counter() - start_time) * 1000)
    if response.status == 'incomplete':
        if response.incomplete_details == 'max_output_tokens':
            answer += "\n\n[Note: The answer may be incomplete due to reaching the maximum output token limit.]"

        else:
            answer += f"\n\n[Note: The answer may be incomplete. Reason: {response.incomplete_details.reason}]"

    usage = {
        'input_tokens': response.usage.input_tokens,
        'output_tokens': response.usage.output_tokens,
        'total_tokens': response.usage.total_tokens
    }

    return AskResponse(answer=answer,
                       latency_ms=latency_ms,
                       usage=usage)


