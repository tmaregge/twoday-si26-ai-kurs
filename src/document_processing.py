import json
from pypdf import PdfReader


def ingest_pypdf(pdf_path: str, out_path: str = ""):
    reader = PdfReader(pdf_path)

    pages = []
    all_text = []

    for page_num, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        text = text.strip()

        pages.append(
            {
                "pageNumber": page_num,
                "content": text,
            }
        )
        if text:
            all_text.append(text)

    result = {
        "content": "\n\n".join(all_text),
        "pages": pages,
    }

    if out_path:
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

    return result


def chunk(
    text: str,
    document_id: str,
    size: int = 1200,
    overlap: int = 200,
) -> list[dict]:
    if not text:
        return []

    chunks = []
    start = 0
    step = max(1, size - overlap)
    chunk_idx = 0

    while start < len(text):
        end = start + size
        current = text[start:end].strip()

        if current:
            chunks.append(
                {
                    "chunkId": f"{document_id}_{chunk_idx}",
                    "documentId": document_id,
                    "content": current,
                }
            )
            chunk_idx += 1

        if end >= len(text):
            break
        start += step

    return chunks
