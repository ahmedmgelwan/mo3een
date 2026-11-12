import time

from dotenv import load_dotenv
from fastembed import TextEmbedding
from openai import OpenAI

from src.config import config

load_dotenv()

base_url = config.BASE_URL
timeout = config.REQUEST_TIMEOUT
max_generated_tokens = int(config.MAX_GENERATED_TOKENS)
generation_model_name = config.GENERATION_MODEL_NAME
embedding_model_name = config.EMBEDDING_MODEL_NAME


class GenerationClient:
    def __init__(
        self,
        client: OpenAI | None = None,
        base_url: str = base_url,
        timeout: int = timeout,
    ):
        self.client = client or OpenAI(
            api_key=config.OPEN_AI_KEY, base_url=base_url, timeout=timeout
        )

    def generate_answer(
        self,
        messages: list,
        model: str = generation_model_name,
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
            self.embeder = TextEmbedding(model_name=embedding_model_name)
        else:
            self.embeder = TextEmbedding(model_name=model_id)

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        embeddings = list(self.embeder.embed(texts))
        return embeddings

generation_client = GenerationClient()
embedding_client = EmbeddingClient(model_id=embedding_model_name)