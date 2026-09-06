from google import genai
from google.genai import types

from config import api_key, model


client = genai.Client(api_key=api_key)


RAG_SYSTEM_PROMPT = """
You are DataMind AI, an enterprise AI assistant.

Answer the user's question using ONLY the provided context.

Rules:
- Do not use outside knowledge.
- Do not invent information.
- If the answer cannot be found in the context, clearly say:
  "I couldn't find that information in the provided document."
- Keep the answer concise and clear.
"""


def generate_answer(
    question: str,
    context: str
) -> str:

    response = client.models.generate_content(
        model=model,
        contents=(
            f"CONTEXT:\n{context}\n\n"
            f"QUESTION:\n{question}"
        ),
        config=types.GenerateContentConfig(
            system_instruction=RAG_SYSTEM_PROMPT
        )
    )

    return response.text