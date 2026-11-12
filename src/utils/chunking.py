import tiktoken
from src.config import config

_tokenizer = tiktoken.get_encoding('o200k_base')



def chunk_text(text: str, chunk_size: int=config.CHUNK_SIZE, chunk_overlap: int=config.CHUNK_OVERLAP) -> list[str]:
    tokens = _tokenizer.encode(text)
    
    chunks = []
    start = 0
    while start < len(tokens):
        chunk_tokens = tokens[start:start + chunk_size]
        chunk_text = _tokenizer.decode(chunk_tokens)
        chunks.append(chunk_text)
        start += chunk_size - chunk_overlap
    return chunks
