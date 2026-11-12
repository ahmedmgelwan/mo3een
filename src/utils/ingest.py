from src.utils.doc_loaders import load_docs
from src.utils.chunking import chunk_text
from src.utils.llm_client import embedding_client
from src.utils.vector_store import vector_store
from src.config import config


def ingest_docs():
    docs = load_docs()
    if not docs:
        print('No documents found to ingest.')
        return

    chunks, metadatas, ids = [], [], []
    for doc in docs:
        print(f"Processing document: {doc['file_name']}")
        doc_chunks = chunk_text(doc["text "])
        for i, chunk in enumerate(doc_chunks):
            chunks.append(chunk)
            metadatas.append({"file_name": doc["file_name"], "chunk_index": i, "scope": config.SCOPE})
            ids.append(f"{doc['file_name']}_chunk_{i}")
    print(f'Embedding {len(chunks)} chunks...')
    embeddings = embedding_client.embed_texts(chunks)
    print('Adding embeddings to vector store...')
    vector_store.add_vectors(embeddings=embeddings, metadatas=metadatas, ids=ids, docs=chunks)
    print('Ingestion complete.\nNow vector store contains {} chunks.'.format(vector_store.count()))


if __name__ == "__main__":
    ingest_docs()