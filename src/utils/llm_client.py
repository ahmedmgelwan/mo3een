import os
import time

from dotenv import load_dotenv

from openai import OpenAI
from fastembed import TextEmbedding

load_dotenv()

base_url = os.getenv("BASE_URL")
timeout = int(os.getenv("REQUEST_TIMEOUT"))
max_generated_tokens = int(os.getenv("MAX_GENERATED_TOKENS"))


class GenerationClient:
    def __init__(
        self,
        client: OpenAI = None,
        base_url: str = base_url,
        timeout: int = timeout,
    ):
        self.client = client or OpenAI(
            api_key=os.getenv("OPEN_AI_API_KEY"), base_url=base_url, timeout=timeout
        )

    def generate_answer(
        self,
        messages: list,
        model: str,
        temperature: float = 0.2,
        max_output_tokens: int = max_generated_tokens,
    ) -> dict:
        start_time = time.perf_counter()
        response = self.client.responses.create(
            input=messages,
            model=model,
            temperature=temperature,
            max_output_tokens=max_output_tokens,
        )
        latency_ms = int((time.perf_counter() - start_time) * 1000)
        usage = {
            "input_tokens": response.usage.input_tokens,
            "output_tokens": response.usage.output_tokens,
            "total_tokens": response.usage.total_tokens,
        }

        reason_text = None
        if response.status == "incomplete" and response.incomplete_details:
            reason_text = response.incomplete_details.reason

        return {
            "answer": response.output_text.strip(),
            "latency_ms": latency_ms,
            "usage": usage,
            "status": response.status,
            "incomplete_reason": reason_text,
        }


class EmbeddingClient:
    def __init__(self, model_id: str | None = None):
        self.model = model_id
        if model_id is None:
            self.embeder = TextEmbedding()
        else:
            self.embeder = TextEmbedding(model_name=model_id)

    def embed_text(self, texts: list[str]) -> list[list[float]]:
        embeddings = list(self.embeder.embed(texts))
        return embeddings
