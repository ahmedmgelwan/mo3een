from src.utils.llm_client import generation_client
from src.config import config


SYSTEM_PROMPT =('You are Mo3een, an AI assistant that helps users find information in their documents.' 
                ' You have access to a collection of documents and can answer questions based on the content of those documents.' 
                ' Your goal is to provide accurate and helpful answers to user queries by retrieving relevant information from the documents.'
                ' You should always respond in a concise and accurate manner, providing references for your answers.'
                ' If the question is not clear, you should ask for clarification.'
                ' If the question is genric and you are sure about the answer, you can provide a general answer based on your knowledge.'
                ' If you do not know the answer, you should say so.'
                ' You should always respond in the language of the question.')


def build_user_prompt(question: str, context: str) -> str:
    return f"Question: {question}\nContext: {context}"


def build_context(chunks: list[dict]) -> str:
    if not chunks:
        return "No relevant information found in the documents."
    chunks = [
        f"<Source: {chunk['metadata']['file_name']}>\n{chunk['document']}"
        for chunk in chunks
    ]
    return "\n\n-----\n\n".join(chunks)




def get_answer(question: str, chunks: list[dict]) -> str:
    context = build_context(chunks)
    user_prompt = build_user_prompt(question, context)
    result = generation_client.generate_answer(
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        model=config.GENERATION_MODEL_NAME,
    )
    return result