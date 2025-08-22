# Python
import os
from typing import List, Optional

def chunk_text(
    text: str,
    chunk_size: int = 1000,
    overlap: int = 100,
    prefer_boundaries: bool = True,
) -> List[str]:
    """
    Split text into overlapping chunks of at most `chunk_size` characters.
    If `prefer_boundaries` is True, try to cut at paragraph/newline/sentence/space boundaries.

    Args:
        text: Input text (any length).
        chunk_size: Max characters per chunk (must be > overlap).
        overlap: Characters to overlap between consecutive chunks (0 <= overlap < chunk_size).
        prefer_boundaries: If True, attempt to cut at nicer boundaries.

    Returns:
        List of chunk strings (in order).
    """
    if chunk_size <= 0:
        raise ValueError("chunk_size must be > 0")
    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap must satisfy 0 <= overlap < chunk_size")

    text = text.replace("\r\n", "\n")  # normalize newlines
    n = len(text)
    if n == 0:
        return []

    def find_best_break(s: str, start: int, hard_end: int) -> Optional[int]:
        """
        Try to find a natural break point at or before hard_end.
        Returns index where to cut (end-exclusive), or None if not found.
        """
        window = s[start:hard_end]
        # Order matters: try stronger boundaries first
        separators = ["\n\n", "\n", ". ", "? ", "! ", " "]
        best = None
        for sep in separators:
            pos = window.rfind(sep)
            if pos != -1:
                candidate = start + pos + len(sep)
                # Prefer breaks that are reasonably close to the hard_end
                if best is None or candidate > best:
                    best = candidate
        return best

    chunks: List[str] = []
    start = 0

    while start < n:
        hard_end = min(start + chunk_size, n)

        end = hard_end
        if prefer_boundaries and hard_end < n:
            best = find_best_break(text, start, hard_end)
            # Only use the best break if it's not too early; otherwise just hard cut
            if best is not None and best > start + chunk_size // 2:
                end = best

        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)

        if end >= n:
            break

        # Advance with overlap
        start = max(end - overlap, 0)
        if start >= n:
            break

    return chunks


def chunk_file(
    path: str,
    chunk_size: int = 1000,
    overlap: int = 100,
    prefer_boundaries: bool = True,
    encoding: str = "utf-8",
) -> List[str]:
    """
    Read a .txt file and split it into chunks.

    Args:
        path: Path to a text file.
        chunk_size: Max characters per chunk.
        overlap: Characters to overlap between chunks.
        prefer_boundaries: Try to cut at natural boundaries if True.
        encoding: File encoding.

    Returns:
        List of chunk strings.
    """
    if not os.path.exists(path) or not path.endswith(".txt"):
        raise FileNotFoundError(f"Invalid .txt file path: {path}")

    with open(path, "r", encoding=encoding) as f:
        content = f.read()

    return chunk_text(
        content,
        chunk_size=chunk_size,
        overlap=overlap,
        prefer_boundaries=prefer_boundaries,
    )


if __name__ == "__main__":
    # Example usage:
    file_path = "../documents/harry.txt"
    chunks = chunk_file(file_path, chunk_size=200, overlap=150, prefer_boundaries=True)
    print(f"Created {len(chunks)} chunks")
    for i, c in enumerate(chunks[:3]):
        print(f"\n--- Chunk {i} ({len(c)} chars) ---\n{c[:300]}{'...' if len(c) > 300 else ''}")