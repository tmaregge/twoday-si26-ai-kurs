#!/usr/bin/env python3
import json
import sys
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from azure.ai.documentintelligence.models import AnalyzeResult
from azure.search.documents.indexes.models import (
    CorsOptions,
    SearchableField,
    SearchFieldDataType,
    SearchIndex,
    SimpleField,
)
from clients import search_idx_client as client, search_idx_client, search_client, oai_client, di_client


def ingest_pypdf(pdf_path: str, out_path: str = "") -> str:
    from pypdf import PdfReader
    reader = PdfReader(pdf_path)
    text = "\n".join(page.extract_text() or "" for page in reader.pages)
    if out_path:
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(text)
    return text


def ingest_di(pdf_path: str, out_path: str = "") -> AnalyzeResult:
    with open(pdf_path, "rb") as f:
        poller = di_client.begin_analyze_document("prebuilt-read", f)
    result = poller.result()
    if out_path:
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(result.as_dict(), f, ensure_ascii=False, indent=2)
    return result


def chunk(document):
    chunks = []
    if isinstance(document, str):
        # Simple fixed-size chunking for plain text
        chunk_size = 500
        words = document.split()
        for i in range(0, len(words), chunk_size):
            text = " ".join(words[i : i + chunk_size])
            chunks.append({
                "chunk_id": str(uuid.uuid4()),
                "document_id": "doc",
                "content": text,
            })
    else:
        # AnalyzeResult: one chunk per paragraph
        doc_id = "doc"
        for idx, para in enumerate(document.paragraphs or []):
            chunks.append({
                "chunk_id": str(uuid.uuid4()),
                "document_id": doc_id,
                "content": para.content,
            })
    return chunks


def create_index(index_name: str):
    name = index_name
    fields = [
        SimpleField(name="chunk_id", type=SearchFieldDataType.String, key=True),
        SimpleField(name="document_id", type=SearchFieldDataType.String, filterable=True),
        SearchableField(name="content", type=SearchFieldDataType.String),
    ]
    cors_options = CorsOptions(allowed_origins=["*"], max_age_in_seconds=60)
    index = SearchIndex(
        name=name,
        fields=fields,
        scoring_profiles=[],
        cors_options=cors_options,
    )
    return client.create_or_update_index(index)


def upload_chunks(chunks: list[dict], index_name: str):
    result = search_client.upload_documents(documents=chunks)
    return result


def recreate_index(index_name: str):
    try:
        search_idx_client.delete_index(index_name)
    except Exception:
        pass
    return create_index(index_name)


def search(search_text: str, document_id: str = "", top: int = 5):
    filter_expr = f"document_id eq '{document_id}'" if document_id else None
    results = search_client.search(search_text=search_text, filter=filter_expr, top=top)
    return list(results)


def generate_answer(question: str, context: str):
    response = oai_client.responses.create(
        model="gpt-5.4-mini",
        instructions="You are a helpful assistant. Answer using only the provided context.",
        input=f"Context:\n{context}\n\nQuestion: {question}",
    )
    return response.output_text


def ask(question: str, document_id: str = ""):
    results = search(question, document_id=document_id)
    print(results)
    context = "\n\n".join(r["content"] for r in results)
    return generate_answer(question, context)


def embed(text):
    response = oai_client.embeddings.create(
        input=text,
        model="text-embedding-3-large",
    )
    return response.data[0].embedding

    
