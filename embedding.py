# pyrefly: ignore [missing-import]
import ollama


def create_embedding(text):

    response = ollama.embeddings(
        model="nomic-embed-text",
        prompt=text
    )

    return response["embedding"]