from google import genai

from config import api_key


EMBEDDING_MODEL = "gemini-embedding-2"

client = genai.Client(api_key=api_key)


def embed_text(text: str) -> list[float]:
    response = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=text
    )

    return response.embeddings[0].values


def embed_chunks(chunks: list[str]) -> list[list[float]]:
    embeddings = []

    for chunk in chunks:
        embedding = embed_text(chunk)
        embeddings.append(embedding)

    return embeddings