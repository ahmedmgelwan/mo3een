from src.utils.llm_client import embedding_client
from src.utils.vector_store import vector_store
from src.config import config

def retrive(query: str, top_k: int = config.TOP_K, scope: str=config.SCOPE) -> list[dict]:
    query_embedding = embedding_client.embed_texts([query])[0]
    results = vector_store.query(query_embedding=query_embedding, n_results=top_k, scope=scope)
    return results
