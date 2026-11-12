import chromadb
from src.config import config

class VectorStore:
    def __init__(self, db_dir: str = config.CHROMA_DB_DIR, collection_name: str = config.COLLECTION_NAME):
        self.db_dir = db_dir
        self.collection_name = collection_name
        self._client = chromadb.PersistentClient(path=self.db_dir)
        self._collection = self._client.get_or_create_collection(name=self.collection_name)

    def add_vectors(self, embeddings: list[list[float]], metadatas: list[dict], ids: list[str], docs: list[str]) -> None:
        self._collection.add(
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids,
            documents=docs
        )
        

    def query(self, query_embedding: list[float], n_results: int = config.TOP_K, scope: str | None   = None) -> list[dict]:
        where = {"scope": scope} if scope else None
        results = self._collection.query(
            query_embeddings=query_embedding,
            n_results=n_results,
            where=where
        )

        chunks = []
        ids = results.get("ids", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]
        docs = results.get("documents", [[]])[0]
        distances = results.get("distances", [[]])[0]

        for i in range(len(ids)):
            chunks.append({
                "id": ids[i],
                "metadata": metadatas[i],
                "document": docs[i],
                "distance": distances[i]
            })

        return chunks

    def count(self) -> int:
        return self._collection.count()


vector_store = VectorStore()
