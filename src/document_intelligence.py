#!/usr/bin/env python3
import json

from azure.ai.documentintelligence.models import AnalyzeResult
from src.clients import get_di_client

def ingest(pdf_path: str, out_path: str = "") -> AnalyzeResult:
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



def chunk(parsed_document, document_id, target_size=1000):
    chunks = []

    current = []
    current_size = 0
    chunk_idx = 0

    for paragraph in parsed_document.paragraphs:
        text = paragraph.content.strip()

        if not text:
            continue

        if current_size + len(text) > target_size and current:
            chunks.append(
                {
                    "chunkId": f"{document_id}_{chunk_idx}",
                    "documentId": document_id,
                    "content": "\n\n".join(current),
                }
            )

            chunk_idx += 1
            current = []
            current_size = 0

        current.append(text)
        current_size += len(text)

    if current:
        chunks.append(
            {
                "chunkId": f"{document_id}_{chunk_idx}",
                "documentId": document_id,
                "content": "\n\n".join(current),
            }
        )

    return chunks
