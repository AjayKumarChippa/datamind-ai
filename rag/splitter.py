from __future__ import annotations

from typing import List


CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
SEPARATORS = ["\n\n", "\n", ". ", ", ", " "]


def split_text(text: str) -> List[str]:
    """Split text into non-empty chunks using recursive splitting."""
    text = text.strip()
    if not text:
        return []

    if len(text) <= CHUNK_SIZE:
        return [text]

    for separator in SEPARATORS:
        if separator in text:
            parts = [part.strip() for part in text.split(separator) if part.strip()]
            chunks: List[str] = []
            current = ""

            for part in parts:
                if current:
                    candidate = current + separator + part
                else:
                    candidate = part

                if len(candidate) > CHUNK_SIZE:
                    if current:
                        chunks.extend(split_text(current.strip()))
                        current = part
                    else:
                        chunks.extend(split_text(part.strip()))
                        current = ""
                else:
                    current = candidate

            if current:
                chunks.append(current.strip())

            merged_chunks: List[str] = []
            for chunk in chunks:
                if not merged_chunks:
                    merged_chunks.append(chunk)
                    continue

                if len(merged_chunks[-1]) + len(chunk) - CHUNK_OVERLAP <= CHUNK_SIZE:
                    merged_chunks[-1] = (
                        merged_chunks[-1] + " " + chunk
                    ).strip()
                else:
                    overlap = merged_chunks[-1][-CHUNK_OVERLAP:]
                    if chunk.startswith(overlap):
                        merged_chunks.append(chunk)
                    else:
                        merged_chunks.append(chunk)

            return [chunk for chunk in merged_chunks if chunk]

    # Fallback hard split
    return [text[i:i + CHUNK_SIZE].strip() for i in range(0, len(text), CHUNK_SIZE) if text[i:i + CHUNK_SIZE].strip()]
