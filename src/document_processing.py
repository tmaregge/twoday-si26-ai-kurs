import json
from src.clients import get_di_client



def ingest(pdf_path: str, out_path: str = "") -> str:
    client = get_di_client()

    with open(pdf_path, "rb") as f:
        poller = client.begin_analyze_document(model_id="prebuilt-layout", body=f)

    result = poller.result()

    if out_path:
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(
                result.as_dict(),
                f,
                ensure_ascii=False,
                indent=2,
        )

    return result


# Returnerer en liste med chunks (JSON) som kan indekseres i Azure AI Search
def chunk(parsed_document: dict, document_id: str, chunk_size: int = 100) -> list:
    chunks = []
    for paragraph in parsed_document.paragraphs:
        content = paragraph.content
        for i in range(0, len(content), chunk_size):
            chunk = {
                "chunkId": f"{document_id}_{i}",
                "documentId": document_id,
                "content": content[i:i+chunk_size]
            }
            chunks.append(chunk)
    return chunks
